import re
import json
import torch
import torch.nn.functional as F
from pathlib import Path
from ML.tokenizer import BilingualSubwordTokenizer
from ML.model import KavachNet1M

BASE_DIR = Path(__file__).resolve().parent
WEIGHTS_DIR = BASE_DIR / "weights"
DATASET_DIR = BASE_DIR.parent / "dataset"

class KavachAIInferenceEngine:
    """
    Refined, production-grade inference engine using the ~1.34M Parameter KavachNet1M model.
    Sub-15ms local CPU inference with:
      - Typo-robust cyber tokenization
      - Semantic Cosine Similarity Verification
      - Clean, human-like structured responses (no double-numbering or garbled output)
      - Highly accurate Emergency Triage filter
    """
    def __init__(self):
        self.device = torch.device("cpu")
        self.tokenizer = None
        self.model = None
        self.tag_to_id = {}
        self.id_to_tag = {}
        self.intents = {}
        self.canonical_embeddings = {}
        self.kavach_assessments = []
        self.sessions = {}
        self.loaded = False
        self.load()

    def load(self):
        vocab_path = WEIGHTS_DIR / "vocab.json"
        weights_path = WEIGHTS_DIR / "kavach_net_1m.pt"
        tag_map_path = WEIGHTS_DIR / "tag_map.json"
        dataset_path = DATASET_DIR / "unified_cyber_dataset.json"
        emb_path = WEIGHTS_DIR / "embeddings.json"

        if not (vocab_path.exists() and weights_path.exists() and tag_map_path.exists()):
            print("Model weights not yet generated. Waiting for training to complete.")
            return

        self.tokenizer = BilingualSubwordTokenizer.load(vocab_path)
        with open(tag_map_path, "r", encoding="utf-8") as f:
            tag_data = json.load(f)
            self.tag_to_id = tag_data["tag_to_id"]
            self.id_to_tag = {int(k): v for k, v in tag_data["id_to_tag"].items()}

        with open(dataset_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.kavach_assessments = data.get("kavach_assessments", [])
            for item in data.get("intents", []):
                self.intents[item["tag"]] = item

        if emb_path.exists():
            with open(emb_path, "r", encoding="utf-8") as f:
                self.canonical_embeddings = json.load(f)

        num_classes = len(self.id_to_tag)
        self.model = KavachNet1M(vocab_size=4096, embed_dim=128, hidden_dim=128, num_classes=num_classes)
        self.model.load_state_dict(torch.load(weights_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()
        self.loaded = True
        print(f"KavachAI 1M Parameter Model Loaded ({num_classes} classes). Ready for inference.")

    def check_emergency(self, text):
        """
        Detects ACTIVE security incidents requiring instant containment.
        Carefully distinguishes active panic from educational queries.
        """
        text_lower = text.lower().strip()

        # If user is asking an educational or definitional question, it's NOT an emergency
        educational_prefixes = [
            "what is", "what are", "what does", "define", "explain", "tell me about",
            "meaning of", "how to recognize", "how to identify", "signs of", "difference between",
            "क्या है", "किसे कहते हैं", "का अर्थ", "कैसे पहचानें"
        ]
        for ep in educational_prefixes:
            if ep in text_lower:
                return False

        # Active incident indicators (first-person compromise)
        panic_patterns = [
            r"\b(i clicked|clicked on|accidentally clicked|just clicked)\b.*\b(link|attachment|file|website)\b",
            r"\b(i entered|i typed|i shared|i gave)\b.*\b(password|credentials|code|otp|pin|cvv)\b",
            r"\b(i got hacked|got hacked|hacked my|am i hacked|i am hacked|compromised my)\b",
            r"\b(files are encrypted|ransom note appeared|computer is locked by ransomware)\b",
            r"\b(sent money to scammer|transferred money by mistake|money got deducted from upi)\b",
            r"\b(पैसे कट गए|खाता हैक हो गया|पासवर्ड बता दिया|लिंक खोल दिया)\b"
        ]
        for p in panic_patterns:
            if re.search(p, text_lower):
                return True
        return False

    def detect_language(self, text):
        """Detects whether prompt is in Devanagari Hindi or English."""
        if re.search(r"[\u0900-\u097F]", text):
            return "hi"
        return "en"

    def clean_bullet(self, item):
        """Removes duplicate leading digits/symbols like '1. ', '1) ', '- ' to prevent double numbering."""
        return re.sub(r"^\d+[\.\)\-]\s*", "", item).strip()

    def find_best_semantic_intent(self, query_emb, top_k=3):
        """Matches query embedding with canonical exemplars for dual verification."""
        if not self.canonical_embeddings:
            return None, 0.0

        best_score = -1.0
        best_tag_id = None

        query_vec = torch.tensor(query_emb, dtype=torch.float32)

        for tag_id_str, items in self.canonical_embeddings.items():
            for item in items:
                cand_vec = torch.tensor(item["vector"], dtype=torch.float32)
                sim = F.cosine_similarity(query_vec.unsqueeze(0), cand_vec.unsqueeze(0)).item()
                if sim > best_score:
                    best_score = sim
                    best_tag_id = int(tag_id_str)

        return best_tag_id, best_score

    def predict(self, text, session_id="default", user_lang=None):
        if not self.loaded:
            self.load()
            if not self.loaded:
                return "AI model is currently initializing. Please try again in a moment."

        lang = user_lang or self.detect_language(text)
        is_hi = (lang == "hi")

        # 1. Emergency Incident Check (First-person active compromise)
        if self.check_emergency(text):
            if is_hi:
                return (
                    "🚨 **आपातकालीन साइबर सुरक्षा चेतावनी: तुरंत कार्रवाई करें!**\n\n"
                    "यदि आपने किसी संदिग्ध लिंक पर क्लिक किया है या पासवर्ड/OTP साझा कर दिया है:\n\n"
                    "1. 🔌 **डिवाइस डिस्कनेक्ट करें**: तुरंत Wi-Fi बंद करें या मोबाइल डेटा बंद करें ताकि मैलवेयर नेटवर्क में न फैले।\n"
                    "2. 🔑 **पासवर्ड बदलें**: किसी सुरक्षित और अलग डिवाइस से अपने खातों के पासवर्ड तुरंत बदलें।\n"
                    "3. 🏦 **बैंक को सूचित करें**: यदि वित्तीय जानकारी साझा हुई है, तो तुरंत अपने बैंक को सूचित कर कार्ड/UPI ब्लॉक करवाएं।\n"
                    "4. 🛡️ **1930 पर कॉल करें**: भारत सरकार के राष्ट्रीय साइबर अपराध पोर्टल (cybercrime.gov.in) पर तुरंत रिपोर्ट दर्ज करें।\n"
                    "5. ❌ **कभी भी किसी अनचाहे कॉलर के कहने पर एनीडेस्क (AnyDesk) या क्विकसपोर्ट जैसा रिमोट ऐप डाउनलोड न करें।**"
                )
            else:
                return (
                    "🚨 **CRITICAL INCIDENT ALERT: IMMEDIATE CONTAINMENT REQUIRED!**\n\n"
                    "If you entered credentials, shared an OTP, or clicked a suspicious link:\n\n"
                    "1. 🔌 **ISOLATE IMMEDIATELY**: Unplug Ethernet or disconnect Wi-Fi and mobile data to halt malware transmission.\n"
                    "2. 🔑 **RESET CREDENTIALS**: From a separate, trusted device, immediately change passwords and terminate other active sessions.\n"
                    "3. 🏦 **FREEZE BANKING & CARDS**: If payment data or banking OTPs were compromised, notify your bank immediately to block transactions.\n"
                    "4. 🛡️ **REPORT THE INCIDENT**: File an official report with your organization's IT Security/SOC or the national cybercrime portal (dial 1930 in India).\n"
                    "5. ⚠️ **PRESERVE EVIDENCE**: Do not delete the suspicious message, URL, or email header; security analysts need them to block the attacker."
                )

        # 2. Tokenize with cyber-typo normalization
        ids, mask = self.tokenizer.encode(text, max_length=64)
        input_ids = torch.tensor([ids], dtype=torch.long).to(self.device)
        attention_mask = torch.tensor([mask], dtype=torch.long).to(self.device)

        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask)
            logits = outputs["logits"]
            risk_score = float(outputs["risk_score"].item())
            emb = outputs["embedding"].squeeze(0).tolist()

            probs = F.softmax(logits, dim=-1)
            confidence, pred_idx = probs.max(dim=-1)
            confidence = float(confidence.item())
            pred_tag = self.id_to_tag.get(pred_idx.item(), "bot_capabilities")

        # 3. Semantic Cosine Verification (Reranker)
        sem_tag_id, sem_score = self.find_best_semantic_intent(emb)
        if sem_tag_id is not None and sem_score > 0.72:
            sem_tag = self.id_to_tag.get(sem_tag_id)
            if sem_tag and sem_tag != pred_tag:
                # If semantic vector is strong, use semantic intent
                pred_tag = sem_tag

        # 4. Format a Clean, Authoritative, Structured Response
        intent_info = self.intents.get(pred_tag, {})

        summary = intent_info.get("summary_hi" if is_hi else "summary_en", "")
        if not summary:
            summary = intent_info.get("summary_en", "")

        responses = intent_info.get("responses_hi" if is_hi else "responses_en", [])
        if not responses:
            responses = intent_info.get("responses_en", [])

        actions = intent_info.get("action_steps_hi" if is_hi else "action_steps_en", [])
        if not actions:
            actions = intent_info.get("action_steps_en", [])

        red_flags = intent_info.get("red_flags", [])

        pro_tip = intent_info.get("pro_tip_hi" if is_hi else "pro_tip_en", "")
        if not pro_tip:
            pro_tip = intent_info.get("pro_tip_en", "")

        # Format Sections
        response_sections = []

        # Section 1: Definition & Core Explanation
        if summary:
            response_sections.append(summary)
        elif responses:
            response_sections.append(responses[0])

        # Section 2: Red Flags (if available)
        if red_flags:
            flag_header = "#### 🚩 मुख्य खतरे और संकेत (Red Flags):" if is_hi else "#### 🚩 Common Red Flags & Warning Signs:"
            flag_lines = [flag_header]
            for flag in red_flags:
                clean_f = self.clean_bullet(flag)
                flag_lines.append(f"- ⚠️ {clean_f}")
            response_sections.append("\n".join(flag_lines))

        # Section 3: Recommended Action Steps (Cleanly numbered without duplicate digits)
        if actions:
            act_header = "#### 🛡️ सुरक्षा उपाय व बचाव के नियम:" if is_hi else "#### 🛡️ Recommended Security Actions & Best Practices:"
            act_lines = [act_header]
            for idx, act in enumerate(actions, 1):
                clean_a = self.clean_bullet(act)
                act_lines.append(f"{idx}. {clean_a}")
            response_sections.append("\n".join(act_lines))

        # Section 4: Pro-Tip
        if pro_tip:
            tip_header = "💡 **कवच सुरक्षा सुझाव:**" if is_hi else "💡 **Kavach Security Pro-Tip:**"
            response_sections.append(f"> {tip_header} {pro_tip}")

        # If completely empty, fallback
        if not response_sections:
            return (
                "Cybersecurity awareness trainer: Always verify suspicious messages, check domain names carefully, and never disclose sensitive passwords or OTPs."
            )

        return "\n\n".join(response_sections)

    def analyze_phishing(self, text):
        """Neural + Heuristic Phishing & Scam Analyzer."""
        text_lower = text.lower()
        red_flags = []
        base_score = 15

        indicators = [
            (r"(urgent|immediate|suspended|blocked|24 hours|within 10 minutes|खाता बंद|तुरंत)", "High urgency / psychological coercion tactic", 25),
            (r"(verify your identity|confirm password|enter otp|cvv|share pin|अपना otp दर्ज करें)", "Credential / banking secret harvesting attempt", 30),
            (r"(https?://\S+)", "Embedded URL link detected (requires domain verification)", 15),
            (r"(bit\.ly|tinyurl|is\.gd|t\.co|cutt\.ly)", "Obfuscated / shortened URL (hides true destination)", 25),
            (r"(\.exe|\.scr|\.bat|\.zip|\.iso|\.apk|\.vbs)", "Risky file attachment indicator (potential malware payload)", 30),
            (r"(won lottery|prize|gift card|bonus|free cash|₹\s*\d+|इनाम जीता)", "Unsolicited reward / lure baiting mechanism", 20),
            (r"(download anydesk|install teamviewer|screen share|quicksupport)", "Remote desktop control lure (KYC / refund fraud)", 35)
        ]

        for pattern, desc, weight in indicators:
            if re.search(pattern, text_lower):
                red_flags.append(desc)
                base_score += weight

        if self.loaded:
            ids, mask = self.tokenizer.encode(text, max_length=64)
            with torch.no_grad():
                out = self.model(torch.tensor([ids]), torch.tensor([mask]))
                neural_risk = float(out["risk_score"].item()) * 100
                score = int(0.5 * min(base_score, 100) + 0.5 * neural_risk)
        else:
            score = min(base_score, 100)

        if score >= 70:
            category = "CRITICAL PHISHING THREAT"
            verdict = "DO NOT CLICK, DO NOT REPLY, AND NEVER SHARE PASSWORDS OR OTPS."
        elif score >= 40:
            category = "SUSPICIOUS / POTENTIAL SCAM"
            verdict = "Exercise high caution. Independently verify sender through official channels."
        else:
            category = "LOW RISK MESSAGE"
            verdict = "No blatant phishing red flags detected, but always verify unexpected requests."

        return {
            "score": score,
            "risk_level": category,
            "verdict": verdict,
            "red_flags": red_flags,
            "flag_count": len(red_flags)
        }

    def get_session(self, session_id):
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "quiz_idx": 0,
                "score": 0,
                "quiz_active": False,
                "category": None
            }
        return self.sessions[session_id]
