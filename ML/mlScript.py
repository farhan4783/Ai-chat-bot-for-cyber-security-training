import json
import re
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

DATASET_PATH = Path(__file__).resolve().parents[1] / "dataset" / "cybersecurity.json"

class LocalCyberBotAI:
    def __init__(self, dataset_path=DATASET_PATH):
        self.dataset_path = dataset_path
        self.intents = {}
        self.patterns = []
        self.pattern_labels = []
        self.pattern_texts = []
        self.quiz_questions = []
        self.sessions = {}  # session_id -> { "quiz_idx": int, "quiz_active": bool, "score": int }
        
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            analyzer="word",
            sublinear_tf=True,
            strip_accents="unicode",
            token_pattern=r"(?u)\b\w+\b"
        )
        self.classifier = LogisticRegression(
            C=10.0,
            max_iter=1000,
            solver="lbfgs",
            random_state=42
        )
        self.pattern_vectors = None
        self.load_dataset()
        self.train()

    def load_dataset(self):
        with open(self.dataset_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.quiz_questions = data.get("quiz_questions", [])
        
        for item in data.get("intents", []):
            tag = item["tag"]
            self.intents[tag] = item
            for pattern in item.get("patterns", []):
                self.patterns.append(pattern)
                self.pattern_labels.append(tag)
                self.pattern_texts.append(pattern)

    def train(self):
        if not self.patterns:
            raise ValueError("No training patterns found in dataset.")
        
        X = self.vectorizer.fit_transform(self.patterns)
        self.pattern_vectors = X
        self.classifier.fit(X, self.pattern_labels)
        print(f"CyberBot Local AI trained on {len(self.patterns)} patterns across {len(self.intents)} intents.")

    def get_session(self, session_id):
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "quiz_idx": 0,
                "quiz_active": False,
                "quiz_score": 0,
                "quiz_total": 0
            }
        return self.sessions[session_id]

    def check_emergency(self, text):
        """Immediate detection for users in panic or active incident."""
        panic_patterns = [
            r"\b(i clicked|clicked on|clicked a)\b.*\b(link|attachment|file)\b",
            r"\b(i entered|typed my)\b.*\b(password|credentials|code)\b",
            r"\b(got hacked|hacked my|am i hacked|i am hacked|compromised)\b",
            r"\b(ransomware|files are encrypted|ransom note)\b",
            r"\b(sent money|transferred money|gift cards sent)\b"
        ]
        text_lower = text.lower()
        for p in panic_patterns:
            if re.search(p, text_lower):
                return True
        return False

    def analyze_phishing_message(self, text):
        """Inspects arbitrary message/email text for phishing indicators."""
        text_lower = text.lower()
        red_flags = []
        score = 10  # baseline

        # Urgency triggers
        urgency_terms = ["immediate", "urgent", "24 hours", "suspended", "suspend", "action required", 
                         "final notice", "terminated", "act now", "critical alert", "security alert"]
        found_urgency = [term for term in urgency_terms if term in text_lower]
        if found_urgency:
            score += 25
            red_flags.append(f"**Artificial Urgency & Threat**: Contains pressure keywords ({', '.join(found_urgency[:3])}). Scammers use fear to bypass critical thinking.")

        # Financial / Sensitive Actions
        action_terms = ["gift card", "wire transfer", "bitcoin", "crypto", "verify password", 
                        "confirm identity", "update payment", "invoice attached", "unpaid invoice", "payroll"]
        found_actions = [term for term in action_terms if term in text_lower]
        if found_actions:
            score += 30
            red_flags.append(f"**Sensitive Financial or Credential Demand**: Mentions {', '.join(found_actions[:3])}. Legitimate companies rarely request unexpected payment or password verifications via message.")

        # Impersonation triggers
        impersonation_terms = ["paypal", "microsoft", "google", "apple", "netflix", "bank", "it support", "helpdesk", "ceo", "hr department", "dhl", "fedex", "usps"]
        found_impersonation = [term for term in impersonation_terms if term in text_lower]
        if found_impersonation:
            score += 20
            red_flags.append(f"**High-Profile Brand / Authority Impersonation**: Cites {', '.join(found_impersonation[:2])}. Attackers masquerade as reputable brands to borrow credibility.")

        # Suspicious links or attachments
        if re.search(r"https?://|www\.|\.xyz|\.top|\.click|\.ru|\.work|bit\.ly|tinyurl", text_lower):
            score += 25
            red_flags.append("**Hyperlinks or Shortened URLs Present**: Check the domain carefully. Do not click; hover to inspect the real destination.")
        
        if re.search(r"\.(exe|scr|iso|zip|rar|vbs|bat)\b", text_lower):
            score += 35
            red_flags.append("**High-Risk Attachment Detected**: Mentions dangerous or archived file extensions commonly used to distribute malware.")

        if "dear customer" in text_lower or "dear user" in text_lower or "valued client" in text_lower:
            score += 15
            red_flags.append("**Generic Greeting**: Uses non-personalized greeting ('Dear Customer') typical of mass phishing campaigns.")

        score = min(score, 98)

        if score >= 70:
            rating = "🚨 CRITICAL THREAT (Likely Phishing / Scam)"
            badge_color = "threat-critical"
            guidance = "Do NOT click any links, do NOT download attachments, and do NOT reply. Report this message to your company's IT security team or mark it as phishing in your email client."
        elif score >= 40:
            rating = "⚠️ SUSPICIOUS (Proceed with Caution)"
            badge_color = "threat-suspicious"
            guidance = "Treat this message with high skepticism. Verify the request through a known, independent phone number or official app before taking any action."
        else:
            rating = "ℹ️ LOW RISK / INFORMATIONAL"
            badge_color = "threat-low"
            guidance = "No overt indicators of malicious intent were detected, but always confirm sender identity before sharing confidential information."

        output = [
            f"### 🔍 Phishing Threat Analysis Report\n",
            f"**Threat Assessment**: `{rating}` (Risk Score: **{score}/100**)\n",
            "#### 🚩 Detected Red Flags:",
        ]
        if red_flags:
            for flag in red_flags:
                output.append(f"- {flag}")
        else:
            output.append("- No obvious phishing triggers detected in the provided snippet.")

        output.append("\n#### 🛡️ Recommended Action:")
        output.append(f"{guidance}\n")
        output.append("> **Golden Rule**: When an unexpected message demands immediate action, pause. Real organizations will never punish you for taking 2 minutes to independently verify.")
        return "\n".join(output)

    def handle_quiz(self, session, user_text=""):
        user_clean = user_text.strip().upper()
        
        # If starting fresh
        if not session["quiz_active"]:
            session["quiz_active"] = True
            session["quiz_idx"] = 0
            session["quiz_score"] = 0
            session["quiz_total"] = len(self.quiz_questions)

        current_idx = session["quiz_idx"]

        # Evaluate previous question if user responded with A/B/C/D
        eval_message = ""
        if current_idx > 0 and user_clean in ["A", "B", "C", "D"]:
            prev_q = self.quiz_questions[current_idx - 1]
            correct = prev_q["correct_answer"]
            if user_clean == correct:
                session["quiz_score"] += 1
                eval_message = f"✅ **Correct!** ({user_clean})\n{prev_q['explanation']}\n\n---\n"
            else:
                eval_message = f"❌ **Incorrect.** You selected **{user_clean}**, but the correct answer is **{correct}**.\n{prev_q['explanation']}\n\n---\n"

        # Check if quiz finished
        if current_idx >= len(self.quiz_questions):
            session["quiz_active"] = False
            score = session["quiz_score"]
            total = len(self.quiz_questions)
            pct = int((score / total) * 100)
            
            badge = "🏆 Cyber Security Champion" if pct >= 80 else ("🛡️ Security Aware" if pct >= 60 else "⚠️ Training Recommended")
            
            return (
                f"{eval_message}"
                f"### 🎯 Quiz Complete!\n\n"
                f"**Your Score**: **{score}/{total}** ({pct}%)\n"
                f"**Status**: `{badge}`\n\n"
                f"{'Fantastic job! You demonstrated strong awareness against modern cyber threats.' if pct >= 80 else 'Good effort! Review the topics above and practice recognizing social engineering traps.'}\n\n"
                f"*Type 'quiz' to try again, or ask any cybersecurity question!*"
            )

        # Present the next question
        q = self.quiz_questions[current_idx]
        session["quiz_idx"] += 1

        opts = "\n".join([f"- **{k})** {v}" for k, v in q["options"].items()])

        return (
            f"{eval_message}"
            f"### 🎯 Cybersecurity Scenario Quiz ({current_idx + 1}/{len(self.quiz_questions)})\n\n"
            f"**Scenario**: {q['scenario']}\n\n"
            f"{opts}\n\n"
            f"*👉 Reply with **A**, **B**, **C**, or **D**.*"
        )

    def predict_intent(self, text):
        """Classify user intent using TF-IDF + LogisticRegression + Semantic Cosine Similarity."""
        # Check emergency panic triggers first
        if self.check_emergency(text):
            return "incident_response_immediate", 0.99, "Emergency panic indicator detected"

        # Check for phishing analyzer intent
        if any(trigger in text.lower() for trigger in ["analyze this", "check this email", "is this email phishing", "inspect this", "check this message"]):
            # If text has content beyond the trigger, analyze directly
            clean_sub = re.sub(r"(?i)^(analyze this|check this email|is this email phishing|inspect this|check this message)[:\s]*", "", text).strip()
            if len(clean_sub) > 15:
                return "DIRECT_PHISHING_ANALYSIS", 1.0, clean_sub
            return "phishing_analyzer_trigger", 0.95, text

        # Check for quiz intent
        if re.search(r"\b(quiz|test me|cyber test|start quiz|take quiz|knowledge check)\b", text.lower()):
            return "quiz_request", 0.99, text

        X_user = self.vectorizer.transform([text])
        
        # LogisticRegression classification probabilities
        probs = self.classifier.predict_proba(X_user)[0]
        best_class_idx = np.argmax(probs)
        best_intent = self.classifier.classes_[best_class_idx]
        classifier_conf = probs[best_class_idx]

        # Semantic Cosine Similarity against all exemplar patterns
        sims = cosine_similarity(X_user, self.pattern_vectors)[0]
        best_sim_idx = np.argmax(sims)
        best_sim_score = sims[best_sim_idx]
        best_pattern_intent = self.pattern_labels[best_sim_idx]
        nearest_pattern = self.patterns[best_sim_idx]

        # Blended confidence: Give weight to exact semantic pattern matching
        if best_sim_score > 0.65:
            final_intent = best_pattern_intent
            final_conf = max(classifier_conf, best_sim_score)
        else:
            final_intent = best_intent
            final_conf = classifier_conf

        return final_intent, final_conf, nearest_pattern

    def format_topic_response(self, intent_tag):
        """Builds an industry-grade, beautifully structured Markdown response."""
        data = self.intents.get(intent_tag)
        if not data:
            return "I apologize, but I do not have detailed information on that topic yet. Try asking about phishing, ransomware, passwords, MFA, public Wi-Fi, or incident reporting."

        lines = []
        summary = data.get("summary", "")
        if summary:
            lines.append(f"{summary}\n")

        red_flags = data.get("red_flags", [])
        if red_flags:
            lines.append("#### 🚩 Warning Signs & Red Flags:")
            for flag in red_flags:
                lines.append(f"- {flag}")
            lines.append("")

        action_steps = data.get("action_steps", [])
        if action_steps:
            lines.append("#### 🛡️ Recommended Best Practices & Action Steps:")
            for step in action_steps:
                lines.append(f"- {step}")
            lines.append("")

        pro_tip = data.get("pro_tip", "")
        if pro_tip:
            lines.append(f"> 💡 **Pro Tip**: {pro_tip}\n")

        follow_ups = data.get("follow_ups", [])
        if follow_ups:
            lines.append("##### 💬 Related Questions You Can Ask:")
            for q in follow_ups[:3]:
                lines.append(f"- *\"{q}\"*")

        return "\n".join(lines).strip()

    def respond(self, message, session_id="default"):
        if not isinstance(message, str) or not message.strip():
            return "Please type a cybersecurity question, paste a suspicious email to analyze, or type **'quiz'** to test your knowledge!"

        clean_msg = message.strip()
        session = self.get_session(session_id)

        # Handle active quiz session if user answers A, B, C, D
        if session["quiz_active"] and clean_msg.upper() in ["A", "B", "C", "D"]:
            return self.handle_quiz(session, clean_msg)

        # Predict intent
        intent, conf, extra = self.predict_intent(clean_msg)

        # Direct phishing inspection
        if intent == "DIRECT_PHISHING_ANALYSIS":
            return self.analyze_phishing_message(extra)

        # Quiz request
        if intent == "quiz_request":
            session["quiz_active"] = False  # Reset
            return self.handle_quiz(session)

        # If confidence is too low (< 0.20)
        if conf < 0.20:
            return (
                "I'm not quite sure I understood that question. As a cybersecurity awareness trainer, I can help you with:\n\n"
                "- **Phishing & Scams**: Spotting fake emails, smishing texts, and BEC wire fraud.\n"
                "- **Passwords & MFA**: Passphrases, password managers, 2FA, and passkeys.\n"
                "- **Malware & Ransomware**: Protection, symptoms, and containment.\n"
                "- **Emergency Incident Response**: What to do immediately if you clicked a suspicious link.\n"
                "- **Safe Habits**: Public Wi-Fi safety, USB security, and software updates.\n\n"
                "*Tip: You can also type **'quiz'** to start an interactive security test or paste a suspicious email snippet!*"
            )

        return self.format_topic_response(intent)


# Instantiate the global AI engine
Model = LocalCyberBotAI()

if __name__ == "__main__":
    print("Testing CyberBot Local AI...")
    test_queries = [
        "What is phishing?",
        "I clicked a suspicious link and typed my password what do I do?",
        "How do passkeys work?",
        "Analyze this email: From support@paypal-security.xyz Urgent! Your account is suspended, click here to verify.",
        "quiz"
    ]
    for q in test_queries:
        print(f"\n--- USER: {q} ---")
        print(Model.respond(q))
