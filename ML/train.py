import os
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from ML.tokenizer import BilingualSubwordTokenizer
from ML.model import KavachNet1M

BASE_DIR = Path(__file__).resolve().parent
WEIGHTS_DIR = BASE_DIR / "weights"
WEIGHTS_DIR.mkdir(exist_ok=True)

class CyberDataset(Dataset):
    def __init__(self, samples, tokenizer, max_len=64):
        self.samples = samples
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        item = self.samples[idx]
        ids, mask = self.tokenizer.encode(item["text"], max_length=self.max_len)
        return {
            "input_ids": torch.tensor(ids, dtype=torch.long),
            "attention_mask": torch.tensor(mask, dtype=torch.long),
            "label": torch.tensor(item["label"], dtype=torch.long),
            "risk": torch.tensor(item["risk"], dtype=torch.float32)
        }

def prepare_data():
    dataset_path = BASE_DIR.parent / "dataset" / "unified_cyber_dataset.json"
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    intents = data.get("intents", [])
    tag_to_id = {item["tag"]: idx for idx, item in enumerate(intents)}
    id_to_tag = {idx: item["tag"] for idx, item in enumerate(intents)}

    corpus = []
    samples = []

    for item in intents:
        tag = item["tag"]
        label = tag_to_id[tag]
        risk = item.get("default_risk", 0.3)

        # English patterns
        for p in item.get("patterns_en", []):
            if p.strip():
                corpus.append(p)
                samples.append({"text": p, "label": label, "risk": risk, "lang": "en"})
        
        # Hindi patterns
        for p in item.get("patterns_hi", []):
            if p.strip():
                corpus.append(p)
                samples.append({"text": p, "label": label, "risk": risk, "lang": "hi"})

        # Summaries and responses
        for resp in item.get("responses_en", []):
            if resp.strip():
                corpus.append(resp)
        for resp in item.get("responses_hi", []):
            if resp.strip():
                corpus.append(resp)

    # Add Kavach quiz questions
    for cat in data.get("kavach_assessments", []):
        cat_tag = f"kavach_{cat['id'].replace('-', '_')}"
        label = tag_to_id.get(cat_tag, 0)
        for q in cat.get("questions", []):
            q_en = q["question"]["en"]
            q_hi = q["question"]["hi"]
            corpus.extend([q_en, q_hi])
            samples.append({"text": q_en, "label": label, "risk": 0.5, "lang": "en"})
            samples.append({"text": q_hi, "label": label, "risk": 0.5, "lang": "hi"})

    # Save intent mapping
    with open(WEIGHTS_DIR / "tag_map.json", "w", encoding="utf-8") as f:
        json.dump({"tag_to_id": tag_to_id, "id_to_tag": id_to_tag}, f, indent=2)

    return corpus, samples, len(tag_to_id)

def train_model(epochs=25, batch_size=16, lr=1e-3):
    print("Step 1: Preparing dataset and training tokenizer...")
    corpus, samples, num_classes = prepare_data()
    print(f"Total training corpus entries: {len(corpus)}")
    print(f"Total labeled training samples: {len(samples)}")

    tokenizer = BilingualSubwordTokenizer(vocab_size=4096)
    tokenizer.train_from_corpus(corpus)
    tokenizer.save(WEIGHTS_DIR / "vocab.json")

    print("\nStep 2: Initializing KavachNet1M (~1M Parameters)...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = KavachNet1M(vocab_size=4096, embed_dim=128, hidden_dim=128, num_classes=num_classes)
    model.to(device)
    
    total_params, _ = model.count_parameters()
    print(f"Target Model Parameters: {total_params:,} on {device}")

    # Dataset & DataLoader
    train_dataset = CyberDataset(samples, tokenizer, max_len=64)
    dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    # Multi-task Loss functions & Optimizer
    ce_loss_fn = nn.CrossEntropyLoss()
    mse_loss_fn = nn.MSELoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)

    print("\nStep 3: Training KavachNet1M across intents, risk regression & embeddings...")
    model.train()
    for epoch in range(1, epochs + 1):
        total_loss = 0.0
        correct = 0
        total = 0
        
        for batch in dataloader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)
            risks = batch["risk"].to(device)

            optimizer.zero_grad()
            outputs = model(input_ids, attention_mask)

            loss_intent = ce_loss_fn(outputs["logits"], labels)
            loss_risk = mse_loss_fn(outputs["risk_score"], risks)
            loss = loss_intent + 0.5 * loss_risk

            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            total_loss += loss.item() * len(labels)
            preds = outputs["logits"].argmax(dim=-1)
            correct += (preds == labels).sum().item()
            total += len(labels)

        avg_loss = total_loss / total
        acc = (correct / total) * 100.0
        if epoch % 5 == 0 or epoch == epochs:
            print(f"Epoch [{epoch:02d}/{epochs:02d}] - Loss: {avg_loss:.4f} - Intent Accuracy: {acc:.2f}%")

    print("\nStep 4: Computing canonical semantic embeddings for response generation...")
    model.eval()
    with torch.no_grad():
        canonical_embeddings = {}
        for sample in samples:
            tag_id = sample["label"]
            ids, mask = tokenizer.encode(sample["text"], max_length=64)
            ids_t = torch.tensor([ids], dtype=torch.long).to(device)
            mask_t = torch.tensor([mask], dtype=torch.long).to(device)
            out = model(ids_t, mask_t)
            emb = out["embedding"].cpu().squeeze(0).tolist()
            if tag_id not in canonical_embeddings:
                canonical_embeddings[tag_id] = []
            canonical_embeddings[tag_id].append({"text": sample["text"], "vector": emb, "lang": sample["lang"]})

    # Save model weights & metadata
    torch.save(model.state_dict(), WEIGHTS_DIR / "kavach_net_1m.pt")
    
    with open(WEIGHTS_DIR / "embeddings.json", "w", encoding="utf-8") as f:
        json.dump(canonical_embeddings, f)

    print(f"\nTraining Complete! Weights successfully saved to {WEIGHTS_DIR / 'kavach_net_1m.pt'}")
    return model

if __name__ == "__main__":
    train_model(epochs=25, batch_size=16)
