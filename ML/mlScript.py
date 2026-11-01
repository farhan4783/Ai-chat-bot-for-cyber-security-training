import os
import sys
import json
import re
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure ML package is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ML.inference import KavachAIInferenceEngine

DATASET_PATH = PROJECT_ROOT / "dataset" / "unified_cyber_dataset.json"
LEGACY_DATASET_PATH = PROJECT_ROOT / "dataset" / "cybersecurity.json"

class CyberBotAI:
    """
    Kavach-CyberBot Master Controller.
    Combines the ~1.34M Parameter Deep Learning Neural Core (KavachNet1M),
    Kavach's 11-category bilingual assessment engine (110 questions),
    and real-time phishing & panic inspection.
    """
    def __init__(self):
        self.engine = KavachAIInferenceEngine()
        self.dataset_path = DATASET_PATH if DATASET_PATH.exists() else LEGACY_DATASET_PATH
        self.intents = {}
        self.patterns = []
        self.quiz_questions = []
        self.kavach_assessments = []
        self.sessions = {}
        self.load_data()

    def load_data(self):
        if self.dataset_path.exists():
            with open(self.dataset_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.kavach_assessments = data.get("kavach_assessments", [])
            for item in data.get("intents", []):
                tag = item["tag"]
                self.intents[tag] = item
                for p in item.get("patterns_en", item.get("patterns", [])):
                    self.patterns.append(p)
                for p in item.get("patterns_hi", []):
                    self.patterns.append(p)

            # Build unified quiz list: Kavach questions + Scenario questions
            for cat in self.kavach_assessments:
                cat_name = cat["name"]["en"]
                for q in cat.get("questions", []):
                    opts_dict = {chr(65 + i): opt for i, opt in enumerate(q["options"]["en"])}
                    opts_hi_dict = {chr(65 + i): opt for i, opt in enumerate(q["options"]["hi"])}
                    correct_letter = chr(65 + q["answer"])
                    self.quiz_questions.append({
                        "category": cat_name,
                        "scenario": q["question"]["en"],
                        "scenario_hi": q["question"]["hi"],
                        "options": opts_dict,
                        "options_hi": opts_hi_dict,
                        "answer": correct_letter,
                        "explanation": q["explanation"]["en"],
                        "explanation_hi": q["explanation"]["hi"]
                    })

        # Fallback to legacy quiz questions if unified empty
        if not self.quiz_questions and LEGACY_DATASET_PATH.exists():
            with open(LEGACY_DATASET_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.quiz_questions = data.get("quiz_questions", [])

        print(f"CyberBot AI Loaded: {len(self.intents)} intents, {len(self.patterns)} patterns, {len(self.quiz_questions)} quiz questions.")

    def get_session(self, session_id):
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "quiz_idx": 0,
                "quiz_active": False,
                "quiz_score": 0,
                "quiz_total": 0,
                "language": "en"
            }
        return self.sessions[session_id]

    def analyze_phishing_message(self, text):
        return self.engine.analyze_phishing(text)

    def handle_quiz(self, session, user_answer=None, language="en"):
        """Interactive scenario-based quiz state machine supporting English and Hindi."""
        is_hi = (language == "hi" or session.get("language") == "hi")
        
        # Start a new quiz session
        if not session["quiz_active"]:
            session["quiz_active"] = True
            session["quiz_idx"] = 0
            session["quiz_score"] = 0
            session["quiz_total"] = min(len(self.quiz_questions), 5)
            session["language"] = "hi" if is_hi else "en"

            first_q = self.quiz_questions[0]
            scenario = first_q.get("scenario_hi" if is_hi else "scenario", first_q.get("scenario", ""))
            opts_map = first_q.get("options_hi" if is_hi else "options", first_q.get("options", {}))
            opts = "\n".join([f"- **{k})** {v}" for k, v in opts_map.items()])

            intro = (
                "### 🎯 कवच साइबर सुरक्षा क्विज़ (Kavach Cyber Quiz)\n\n"
                f"**श्रेणी / Category**: `{first_q.get('category', 'Cybersecurity')}`\n\n"
                f"**परिदृश्य (Scenario 1/{session['quiz_total']})**:\n{scenario}\n\n"
                f"{opts}\n\n"
                "*👉 कृपया सही विकल्प के लिए **A**, **B**, **C**, या **D** लिखकर जवाब दें।*"
                if is_hi else
                "### 🎯 Kavach Interactive Cybersecurity Quiz\n\n"
                f"**Domain**: `{first_q.get('category', 'Cybersecurity')}`\n\n"
                f"**Scenario 1/{session['quiz_total']}**:\n{scenario}\n\n"
                f"{opts}\n\n"
                "*👉 Reply with **A**, **B**, **C**, or **D**.*"
            )
            return intro

        # Process user's answer
        current_idx = session["quiz_idx"]
        eval_message = ""

        if user_answer:
            prev_q = self.quiz_questions[current_idx]
            correct_ans = prev_q["answer"].strip().upper()
            user_ans_clean = user_answer.strip().upper()
            explanation = prev_q.get("explanation_hi" if is_hi else "explanation", prev_q.get("explanation", ""))

            if user_ans_clean == correct_ans:
                session["quiz_score"] += 1
                eval_message = (
                    f"✅ **सही उत्तर! (Option {correct_ans})**\n\n{explanation}\n\n---\n\n"
                    if is_hi else
                    f"✅ **Correct! (Option {correct_ans})**\n\n{explanation}\n\n---\n\n"
                )
            else:
                eval_message = (
                    f"❌ **गलत उत्तर। सही विकल्प था: **{correct_ans}****\n\n{explanation}\n\n---\n\n"
                    if is_hi else
                    f"❌ **Incorrect. The correct answer was **{correct_ans}****\n\n{explanation}\n\n---\n\n"
                )

            current_idx += 1
            session["quiz_idx"] = current_idx

        # Check if quiz ended
        if current_idx >= session["quiz_total"]:
            session["quiz_active"] = False
            score = session["quiz_score"]
            total = session["quiz_total"]
            pct = int((score / total) * 100)
            badge = "Cyber Guardian (उत्कृष्ट)" if pct >= 80 else ("Security Aware (अच्छा)" if pct >= 60 else "Needs Practice (सुधार आवश्यक)")

            return (
                f"{eval_message}"
                f"### 🏆 क्विज़ पूर्ण! (Quiz Complete)\n\n"
                f"**अंक (Score)**: **{score}/{total}** ({pct}%)\n"
                f"**स्तर (Rating)**: `{badge}`\n\n"
                f"{'शानदार प्रदर्शन! आपने आधुनिक साइबर खतरों से निपटने की बेहतरीन समझ दिखाई है।' if pct >= 80 else 'अच्छा प्रयास! उपरोक्त सुरक्षा नियमों का अभ्यास करें ताकि ऑनलाइन धोखेबाज़ी से सुरक्षित रह सकें।'}\n\n"
                f"*दोबारा अभ्यास के लिए 'quiz' लिखें, या कोई भी साइबर सवाल पूछें!*"
                if is_hi else
                f"{eval_message}"
                f"### 🏆 Quiz Complete!\n\n"
                f"**Your Final Score**: **{score}/{total}** ({pct}%)\n"
                f"**Awareness Rating**: `{badge}`\n\n"
                f"{'Outstanding performance! You demonstrated sharp instincts against modern cyber threats.' if pct >= 80 else 'Good effort! Review the lessons above to sharpen your threat detection instincts.'}\n\n"
                f"*Type 'quiz' to test another topic, or ask any cybersecurity question!*"
            )

        # Present next question
        q = self.quiz_questions[current_idx]
        scenario = q.get("scenario_hi" if is_hi else "scenario", q.get("scenario", ""))
        opts_map = q.get("options_hi" if is_hi else "options", q.get("options", {}))
        opts = "\n".join([f"- **{k})** {v}" for k, v in opts_map.items()])

        return (
            f"{eval_message}"
            f"### 🎯 प्रश्न {current_idx + 1}/{session['quiz_total']} ({q.get('category', 'Security')})\n\n"
            f"**परिदृश्य (Scenario)**: {scenario}\n\n"
            f"{opts}\n\n"
            f"*👉 कृपया **A**, **B**, **C**, या **D** लिखकर जवाब दें।*"
            if is_hi else
            f"{eval_message}"
            f"### 🎯 Scenario {current_idx + 1}/{session['quiz_total']} ({q.get('category', 'Security')})\n\n"
            f"**Scenario**: {scenario}\n\n"
            f"{opts}\n\n"
            f"*👉 Reply with **A**, **B**, **C**, or **D**.*"
        )

    def respond(self, message, session_id="default", language=None):
        if not isinstance(message, str) or not message.strip():
            return "Please type a cybersecurity question, paste a suspicious email to analyze, or type **'quiz'** to test your knowledge!"

        clean_msg = message.strip()
        session = self.get_session(session_id)
        if language:
            session["language"] = language

        # Detect Hindi if characters present
        is_hi = (language == "hi" or bool(re.search(r"[\u0900-\u097F]", clean_msg)))

        # Handle active quiz responses
        if session["quiz_active"] and clean_msg.upper() in ["A", "B", "C", "D"]:
            return self.handle_quiz(session, clean_msg, language="hi" if is_hi else "en")

        # Handle quiz trigger
        if re.search(r"\b(quiz|quizz|test me|cyber test|start quiz|take quiz|क्विज़|परीक्षा)\b", clean_msg.lower()):
            session["quiz_active"] = False
            return self.handle_quiz(session, language="hi" if is_hi else "en")

        # Direct phishing inspection triggers
        if any(trigger in clean_msg.lower() for trigger in ["analyze this", "check this email", "is this email phishing", "inspect this", "check this message"]):
            clean_sub = re.sub(r"(?i)^(analyze this|check this email|is this email phishing|inspect this|check this message)[:\s]*", "", clean_msg).strip()
            if len(clean_sub) > 10:
                report = self.analyze_phishing_message(clean_sub)
                red_flags_list = "\n".join([f"- ⚠️ {f}" for f in report["red_flags"]]) if report["red_flags"] else "- No explicit red flags detected."
                return (
                    f"### 🛡️ Phishing Inspection Report\n\n"
                    f"**Risk Score**: **{report['score']}/100** (`{report['risk_level']}`)\n\n"
                    f"**Verdict**: {report['verdict']}\n\n"
                    f"#### 🚩 Detected Indicators:\n{red_flags_list}\n\n"
                    f"> 💡 *Always navigate to services directly via verified apps or official domains.*"
                )

        # Neural Model Inference
        return self.engine.predict(clean_msg, session_id=session_id, user_lang="hi" if is_hi else "en")


# Global model singleton
Model = CyberBotAI()

if __name__ == "__main__":
    print("Testing CyberBot Kavach 1M AI Engine...")
    samples = [
        "What is phishing?",
        "UPI PIN डालते समय क्या सावधानियां रखनी चाहिए?",
        "I clicked a suspicious link and typed my password what do I do?",
        "quiz"
    ]
    for s in samples:
        print(f"\n--- USER: {s} ---")
        print(Model.respond(s))
