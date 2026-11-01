import math
import torch
import torch.nn as nn
import torch.nn.functional as F

class MultiHeadSelfAttention(nn.Module):
    """
    Scaled dot-product multi-head self-attention layer.
    Allows tokens to attend across entire sequence context.
    """
    def __init__(self, embed_dim=256, num_heads=4):
        super().__init__()
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        assert self.head_dim * num_heads == embed_dim, "embed_dim must be divisible by num_heads"
        
        self.qkv_proj = nn.Linear(embed_dim, embed_dim * 3)
        self.out_proj = nn.Linear(embed_dim, embed_dim)

    def forward(self, x, mask=None):
        B, L, D = x.shape
        qkv = self.qkv_proj(x).reshape(B, L, 3, self.num_heads, self.head_dim)
        q, k, v = qkv.unbind(dim=2)  # Each is [B, L, H, d_h]
        
        q = q.transpose(1, 2)  # [B, H, L, d_h]
        k = k.transpose(1, 2)
        v = v.transpose(1, 2)
        
        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.head_dim)
        if mask is not None:
            # mask shape: [B, L]
            scores = scores.masked_fill(mask.unsqueeze(1).unsqueeze(2) == 0, -1e9)
        attn = F.softmax(scores, dim=-1)
        out = torch.matmul(attn, v)  # [B, H, L, d_h]
        out = out.transpose(1, 2).reshape(B, L, D)
        return self.out_proj(out)

class KavachNet1M(nn.Module):
    """
    Kavach-Net-1M: Dedicated ~1.14M Parameter Cybersecurity Deep Learning Architecture.
    
    Trained for multi-task operations:
      - Head A: Intent & Security Topic Classification (43 classes)
      - Head B: Threat Severity & Phishing Risk Regression (0.0 - 1.0)
      - Head C: Normalized Semantic Vectors (128-dim) for RAG retrieval
    """
    def __init__(self, vocab_size=4096, embed_dim=128, hidden_dim=128, num_classes=43):
        super().__init__()
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.hidden_dim = hidden_dim
        self.num_classes = num_classes

        # 1. Token Embeddings
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        
        # 2. 2-Layer Bidirectional Gated Recurrent Unit (BiGRU)
        self.gru1 = nn.GRU(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.gru2 = nn.GRU(hidden_dim * 2, hidden_dim, batch_first=True, bidirectional=True)
        
        # 3. Multi-Head Scaled Dot-Product Attention & Normalization
        self.attention = MultiHeadSelfAttention(embed_dim=hidden_dim * 2, num_heads=4)
        self.norm = nn.LayerNorm(hidden_dim * 2)
        
        # 4. Bottleneck Projection
        self.bottleneck = nn.Sequential(
            nn.Linear(hidden_dim * 2, embed_dim),
            nn.ReLU(),
            nn.Dropout(0.2)
        )
        
        # 5. Multi-Task Output Heads
        self.intent_head = nn.Linear(embed_dim, num_classes)
        self.risk_head = nn.Sequential(
            nn.Linear(embed_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )
        self.embed_head = nn.Linear(embed_dim, embed_dim)

    def forward(self, input_ids, attention_mask=None):
        # [B, L] -> [B, L, D]
        x = self.embedding(input_ids)
        
        # BiGRU layers
        x, _ = self.gru1(x)
        x, _ = self.gru2(x)
        
        # Self-Attention + Residual connection + LayerNorm
        attn_out = self.attention(x, mask=attention_mask)
        x = self.norm(x + attn_out)
        
        # Masked Attention Pooling
        if attention_mask is not None:
            mask_exp = attention_mask.unsqueeze(-1).float()
            pooled = (x * mask_exp).sum(dim=1) / mask_exp.sum(dim=1).clamp(min=1.0)
        else:
            pooled = x.mean(dim=1)
            
        features = self.bottleneck(pooled)
        
        logits = self.intent_head(features)
        risk_score = self.risk_head(features)
        semantic_vec = F.normalize(self.embed_head(features), p=2, dim=-1)
        
        return {
            "logits": logits,
            "risk_score": risk_score.squeeze(-1),
            "embedding": semantic_vec
        }

    def count_parameters(self):
        total = sum(p.numel() for p in self.parameters())
        trainable = sum(p.numel() for p in self.parameters() if p.requires_grad)
        return total, trainable

if __name__ == "__main__":
    model = KavachNet1M()
    total, trainable = model.count_parameters()
    print("=" * 60)
    print(f"KavachNet1M Architecture Initialized")
    print(f"Total Parameters:     {total:,}")
    print(f"Trainable Parameters: {trainable:,}")
    print("=" * 60)
    
    # Test forward pass with dummy batch
    dummy_ids = torch.randint(0, 4096, (2, 32))
    dummy_mask = torch.ones(2, 32)
    output = model(dummy_ids, dummy_mask)
    print("Forward Pass Shapes:")
    print("Logits shape:      ", output["logits"].shape)
    print("Risk score shape:  ", output["risk_score"].shape)
    print("Embedding shape:   ", output["embedding"].shape)

