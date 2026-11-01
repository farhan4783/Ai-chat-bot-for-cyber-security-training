import re
import json
from collections import Counter
from pathlib import Path

SPECIAL_TOKENS = ["<pad>", "<unk>", "<bos>", "<eos>"]

class BilingualSubwordTokenizer:
    """
    Fast, lightweight subword/word-piece tokenizer supporting English & Hindi (Devanagari).
    Vocab size budgeted for ~4,096 tokens to maintain exact ~1M model parameter constraint.
    """
    def __init__(self, vocab_size=4096):
        self.vocab_size = vocab_size
        self.token_to_id = {}
        self.id_to_token = {}
        for idx, tok in enumerate(SPECIAL_TOKENS):
            self.token_to_id[tok] = idx
            self.id_to_token[idx] = tok

    def _normalize(self, text):
        text = text.strip().lower()
        # Keep English, Hindi Unicode range (\u0900-\u097F), digits, and basic punctuation
        text = re.sub(r"[^\w\s\u0900-\u097F\?\!\.\,\-]", " ", text)
        return text

    def _tokenize_words(self, text):
        norm = self._normalize(text)
        # Split on whitespace and punctuation
        tokens = re.findall(r"[\u0900-\u097F]+|[a-zA-Z0-9]+|[\?\!\.]", norm)
        return tokens

    def train_from_corpus(self, texts):
        word_counts = Counter()
        char_counts = Counter()
        
        for t in texts:
            words = self._tokenize_words(t)
            word_counts.update(words)
            for w in words:
                char_counts.update(list(w))

        # Always include frequent characters first
        current_id = len(self.token_to_id)
        for char, _ in char_counts.most_common():
            if char not in self.token_to_id:
                self.token_to_id[char] = current_id
                self.id_to_token[current_id] = char
                current_id += 1
                if current_id >= self.vocab_size:
                    break

        # Fill remaining budget with most common words / subwords
        for word, _ in word_counts.most_common():
            if current_id >= self.vocab_size:
                break
            if word not in self.token_to_id:
                self.token_to_id[word] = current_id
                self.id_to_token[current_id] = word
                current_id += 1

        print(f"Tokenizer trained. Total vocab size: {len(self.token_to_id)}")

    def encode(self, text, max_length=128, add_special_tokens=True):
        words = self._tokenize_words(text)
        ids = []
        if add_special_tokens:
            ids.append(self.token_to_id["<bos>"])

        for w in words:
            if w in self.token_to_id:
                ids.append(self.token_to_id[w])
            else:
                # Subword fallback to character level
                matched = False
                for c in list(w):
                    if c in self.token_to_id:
                        ids.append(self.token_to_id[c])
                        matched = True
                if not matched:
                    ids.append(self.token_to_id["<unk>"])

        if add_special_tokens:
            ids.append(self.token_to_id["<eos>"])

        # Truncate or Pad
        attention_mask = [1] * len(ids)
        if len(ids) > max_length:
            ids = ids[:max_length]
            attention_mask = attention_mask[:max_length]
        else:
            padding_len = max_length - len(ids)
            ids.extend([self.token_to_id["<pad>"]] * padding_len)
            attention_mask.extend([0] * padding_len)

        return ids, attention_mask

    def decode(self, token_ids):
        tokens = []
        for tid in token_ids:
            if tid in self.id_to_token:
                tok = self.id_to_token[tid]
                if tok not in SPECIAL_TOKENS:
                    tokens.append(tok)
        return " ".join(tokens)

    def save(self, filepath):
        data = {
            "vocab_size": self.vocab_size,
            "token_to_id": self.token_to_id,
            "id_to_token": {str(k): v for k, v in self.id_to_token.items()}
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        tok = cls(vocab_size=data["vocab_size"])
        tok.token_to_id = data["token_to_id"]
        tok.id_to_token = {int(k): v for k, v in data["id_to_token"].items()}
        return tok

