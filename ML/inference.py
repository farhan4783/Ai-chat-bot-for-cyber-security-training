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
    Production-grade inference engine using the 1-Million Parameter KavachNet1M model.
    Sub-15ms local CPU inference with bilingual (EN/HI) reasoning, risk assessment,
    emergency triage, and scenario-based training.
    """
    def __init__(self):
        self.device = torch.device("cpu")
        self.tokenizer = None
        self.model = None
        self.tag_to_id = {}
        self.id_to_tag = {}
        self.intents = {}
        self.kavach_assessments = []
        self.sessions = {}
        self.loaded = False
        self.load()

    def load(self):
        vocab_path = WEIGHTS_DIR / "vocab.json"
        weights_path = WEIGHTS_DIR / "kavach_net_1m.pt"
        tag_map_path = WEIGHTS_DIR / "tag_map.json"
        dataset_path = DATASET_DIR / "unified_cyber_dataset.json"

        if not (vocab_path.exists() and weights_path.exists() and tag_map_path.exists()):
            print("Model weights not yet generated. Ready to initialize once training completes.")
            return

        # Load Tokenizer & Metadata
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

        # Load Model
        num_classes = len(self.id_to_tag)
        self.model = KavachNet1M(vocab_size=4096, embed_dim=128, hidden_dim=128, num_classes=num_classes)
        self.model.load_state_dict(torch.load(weights_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()
        self.loaded = True
        print(f"KavachAI 1M Parameter Model Loaded ({num_classes} classes). Ready for inference.")

    def check_emergency(self, text):
        """High-priority instant triage for active compromises."""
        panic_patterns = [
            r"\b(i clicked|clicked on|clicked a)\b.*\b(link|attachment|file)\b",
            r"\b(i entered|typed my)\b.*\b(password|credentials|code|otp)\b",
            r"\b(got hacked|hacked my|am i hacked|i am hacked|compromised)\b",
            r"\b(ransomware|files are encrypted|ransom note)\b",
            r"\b(sent money|transferred money|gift cards sent|upi money deducted)\b",
            r"\b(पैसे कट गए|हैक हो गया|पासवर्ड बता दिया|लिंक पर क्लिक कर दिया)\b"
        ]
        text_lower = text.lower()
        for p in panic_patterns:
            if re.search(p, text_lower):
                return True
        return False

    def detect_language(self, text):
        """Simple Devanagari character detection."""
        if re.search(r"[\u0900-\u097F]", text):
            return "hi"
        return "en"

    def predict(self, text, session_id="default", user_lang=None):
        if not self.loaded:
            self.load()
            if not self.loaded:
                return "AI model is currently initializing. Please try again in a moment."

        lang = user_lang or self.detect_language(text)
        is_hi = (lang == "hi")

        # 1. Emergency Incident Check
        if self.check_emergency(text):
            if is_hi:
                return (
                    "🚨 **आपातकालीन साइबर सुरक्षा चेतावनी: तुरंत कार्रवाई करें!**\n\n"
                    "यदि आपने किसी संदिग्ध लिंक पर क्लिक किया है या पासवर्ड/OTP साझा कर दिया है:\n"
                    "1. 🔌 **डिवाइस डिस्कनेक्ट करें**: तुरंत Wi-Fi बंद करें या मोबाइल डेटा बंद करें।\n"
                    "2. 🔑 **पासवर्ड बदलें**: किसी सुरक्षित डिवाइस से अपने सभी महत्वपूर्ण खातों के पासवर्ड बदलें।\n"
                    "3. 💳 **बैंक को सूचित करें**: अपने बैंक/UPI प्रदाता के आधिकारिक हेल्पलाइन नंबर पर तुरंत कॉल करें।\n"
                    "4. 🛡️ **1930 पर कॉल करें**: भारत सरकार के राष्ट्रीय साइबर अपराध पोर्टल (cybercrime.gov.in) पर रिपोर्ट करें।\n"
                    "5. ❌ **कभी भी अनचाहे कॉलर को दोबारा OTP या स्क्रीन शेयर न दें।**"
                )
            else:
                return (
                    "🚨 **CRITICAL INCIDENT ALERT: IMMEDIATE CONTAINMENT REQUIRED!**\n\n"
                    "If you entered credentials, shared an OTP, or clicked a suspicious link:\n"
                    "1. 🔌 **ISOLATE IMMEDIATELY**: Disconnect Wi-Fi, Ethernet, and mobile data.\n"
                    "2. 🔑 **RESET CREDENTIALS**: From a separate trusted device, change your passwords and revoke active sessions.\n"
                    "3. 🏦 **FREEZE BANKING & UPI**: Contact your bank's official emergency helpline right away.\n"
                    "4. 🛡️ **REPORT THE INCIDENT**: File a report on your national cybercrime portal (e.g., cybercrime.gov.in / dial 1930 in India).\n"
                    "5. ⚠️ **DO NOT PAY**: Never transfer ransom money or download remote desktop tools (AnyDesk, TeamViewer) suggested by callers."
                )

        # 2. Model Forward Pass
        ids, mask = self.tokenizer.encode(text, max_length=64)
        input_ids = torch.tensor([ids], dtype=torch.long).to(self.device)
        attention_mask = torch.tensor([mask], dtype=torch.long).to(self.device)

        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask)
            logits = outputs["logits"]
            risk_score = float(outputs["risk_score"].item())
            probs = F.softmax(logits, dim=-1)
            confidence, pred_idx = probs.max(dim=-1)
            confidence = float(confidence.item())
            pred_tag = self.id_to_tag.get(pred_idx.item(), "bot_capabilities")

        # 3. Format Response
        intent_info = self.intents.get(pred_tag, {})
        
        summary = intent_info.get("summary_hi" if is_hi else "summary_en", "")
        if not summary:
            summary = intent_info.get("summary_en", "Guidance from Kavach Cybersecurity Engine.")

        actions = intent_info.get("action_steps_hi" if is_hi else "action_steps_en", [])
        if not actions:
            actions = intent_info.get("action_steps_en", [])

        pro_tip = intent_info.get("pro_tip_hi" if is_hi else "pro_tip_en", "")
        if not pro_tip:
            pro_tip = intent_info.get("pro_tip_en", "")

        responses = intent_info.get("responses_hi" if is_hi else "responses_en", [])
        if not responses:
            responses = intent_info.get("responses_en", [])

        # Build clean structured markdown response
        response_parts = []
        if responses:
            response_parts.append(responses[0])
        elif summary:
            response_parts.append(summary)

        if actions:
            header = "#### 🛡️ सुरक्षा उपाय (Security Steps):" if is_hi else "#### 🛡️ Recommended Security Actions:"
            response_parts.append(header)
            for idx, act in enumerate(actions, 1):
                response_parts.append(f"{idx}. {act}")

        if pro_tip:
            tip_header = "💡 **कवच सुरक्षा सुझाव:**" if is_hi else "💡 **Kavach Security Tip:**"
            response_parts.append(f"\n{tip_header} {pro_tip}")

        # Risk indicator badge
        risk_pct = int(risk_score * 100)
        risk_badge = f"\n\n*(Neural Threat Assessment: {risk_pct}% Risk Potential | Intent: `{pred_tag}` | Confidence: {confidence*100:.1f}%)*"
        response_parts.append(risk_badge)

        return "\n\n".join(response_parts)

    def analyze_phishing(self, text):
        """Neural + Heuristic Phishing & Scam Analyzer."""
        text_lower = text.lower()
        red_flags = []
        base_score = 15

        # Linguistic & technical indicators
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

        # Neural Risk Evaluation
        if self.loaded:
            ids, mask = self.tokenizer.encode(text, max_length=64)
            with torch.no_grad():
                out = self.model(torch.tensor([ids]), torch.tensor([mask]))
                neural_risk = float(out["risk_score"].item()) * 100
                score = int(0.5 * min(base_score, 100) + 0.5 * neural_risk)
        else:
            score = min(base_score, 100)

        # Categorize
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

