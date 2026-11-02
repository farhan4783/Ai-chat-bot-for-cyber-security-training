import json
import csv
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Redundant Kavach categories that should merge into CyberBot's core intents
TAG_MERGES = {
    "kavach_phishing": "phishing_basics",
    "kavach_passwords": "password_security",
    "kavach_social_engineering": "social_engineering",
    "kavach_public_wifi": "public_wifi"
}

# Extensive common typos, definition queries, and conversational variants
ADDITIONAL_PATTERNS = {
    "phishing_basics": [
        "what is phising", "what is phissing", "what is fishing scam", "what is fising",
        "phising", "phissing", "define phising", "define phishing", "explain phishing", "explain phising",
        "what does phishing mean", "phishing meaning", "phising meaning", "tell me about phishing",
        "tell me about phising", "what is a phishing email", "what is a phishing attack",
        "how does phishing work", "how do attackers phish", "how to identify a phishing email",
        "phishing example", "phishing vs legit email", "phishing red flags", "what are phishing attacks",
        "फ़िशिंग क्या है", "फ़िशिंग का मतलब क्या है", "फ़िशिंग कैसे होती है", "phising attack"
    ],
    "malware_and_viruses": [
        "what is malware", "what is malwear", "what is a computer virus", "define malware",
        "explain malware", "types of malware", "how does malware spread", "malwear definition",
        "trojan vs virus", "spyware definition", "what does malware do", "मैलवेयर क्या है"
    ],
    "ransomware_recovery": [
        "what is ransomware", "what is ransomeware", "what is ransome", "define ransomware",
        "explain ransomware", "how ransomware attacks work", "how does ransomware encrypt files",
        "what is a ransom note", "रैनसमवेयर क्या है"
    ],
    "password_security": [
        "what is a strong password", "how to create a strong password", "password security tips",
        "what is a passphrase", "password manager definition", "why unique passwords matter",
        "पासवर्ड सुरक्षा क्या है", "मजबूत पासवर्ड कैसे बनाएं"
    ],
    "2fa_mfa": [
        "what is 2fa", "what is mfa", "what is two factor authentication", "what are passkeys",
        "why use 2fa", "how does mfa protect accounts", "2fa vs mfa", "एमएफए क्या है"
    ],
    "social_engineering": [
        "what is social engineering", "define social engineering", "social engineering attacks",
        "pretexting and baiting", "human hacking definition", "सोशल इंजीनियरिंग क्या है"
    ],
    "public_wifi": [
        "what are public wifi risks", "is public wifi safe", "what is an evil twin attack",
        "public wifi dangers", "using vpn on public wifi", "सार्वजनिक वाईफाई के खतरे"
    ],
    "kavach_upi": [
        "what is upi fraud", "what is upi scam", "explain upi scams", "upi pin rules",
        "do i need pin to receive money", "upi fraud prevention", "यूपीआई धोखाधड़ी क्या है"
    ],
    "kavach_otp_banking": [
        "what is otp fraud", "banking scams definition", "why never share otp", "fake kyc call",
        "bank call fraud", "ओटीपी धोखाधड़ी क्या है"
    ],
    "kavach_fake_websites": [
        "what is a fake website", "how to spot a spoofed website", "fake login page",
        "homograph domain attack", "lookalike website", "नकली वेबसाइट की पहचान"
    ],
    "kavach_shopping": [
        "what is online shopping fraud", "fake shopping website scam", "unbelievable discount scam",
        "marketplace fraud", "ऑनलाइन शॉपिंग स्कैम क्या है"
    ],
    "kavach_jobs": [
        "what is a job scam", "work from home fraud", "recruitment fee scam",
        "fake offer letter", "नौकरी धोखाधड़ी क्या है"
    ],
    "kavach_qr_scams": [
        "what is a qr code scam", "what is quishing", "qr sticker fraud",
        "scanning qr to receive money scam", "क्यूआर कोड स्कैम क्या है"
    ],
    "kavach_social_media": [
        "what are social media scams", "fake account impersonation", "instagram giveaway scam",
        "social media account takeover", "सोशल मीडिया फ्रॉड क्या है"
    ]
}

def clean_step_text(text):
    """Strip leading numbers like '1. ' or '1) ' to prevent double numbering."""
    return re.sub(r"^\d+[\.\)\-]\s*", "", text).strip()

def compile_dataset():
    kavach_path = BASE_DIR / "kavach_data.json"
    cyber_path = BASE_DIR / "cybersecurity.json"
    csv_path = BASE_DIR.parent / "CTDAPD Dataset.csv"
    output_path = BASE_DIR / "unified_cyber_dataset.json"

    with open(kavach_path, "r", encoding="utf-8") as f:
        kavach_data = json.load(f)

    with open(cyber_path, "r", encoding="utf-8") as f:
        cyber_data = json.load(f)

    intent_map = {}

    # 1. Ingest CyberBot core intents
    for item in cyber_data.get("intents", []):
        tag = item["tag"]
        action_steps_clean = [clean_step_text(s) for s in item.get("action_steps", []) if s.strip()]
        
        intent_map[tag] = {
            "tag": tag,
            "patterns_en": list(item.get("patterns", [])),
            "patterns_hi": [],
            "summary_en": item.get("summary", ""),
            "summary_hi": "",
            "action_steps_en": action_steps_clean,
            "action_steps_hi": [],
            "red_flags": item.get("red_flags", []),
            "responses_en": item.get("responses", []),
            "responses_hi": [],
            "pro_tip_en": item.get("pro_tip", ""),
            "pro_tip_hi": "",
            "default_risk": 0.25
        }
        if "ransomware" in tag or "emergency" in tag or "incident" in tag:
            intent_map[tag]["default_risk"] = 0.90
        elif "phishing" in tag or "credential" in tag or "malware" in tag:
            intent_map[tag]["default_risk"] = 0.70
        elif "password" in tag or "2fa" in tag:
            intent_map[tag]["default_risk"] = 0.30

    # 2. Ingest Kavach categories and merge redundant ones
    for cat in kavach_data.get("categories", []):
        cat_id = cat["id"]
        raw_tag = f"kavach_{cat_id.replace('-', '_')}"
        target_tag = TAG_MERGES.get(raw_tag, raw_tag)

        name_en = cat["name"]["en"]
        name_hi = cat["name"]["hi"]

        if target_tag not in intent_map:
            intent_map[target_tag] = {
                "tag": target_tag,
                "name_en": name_en,
                "name_hi": name_hi,
                "patterns_en": [
                    f"What is {name_en}?",
                    f"How to stay safe from {name_en}?",
                    f"Explain {name_en} fraud and scams",
                    f"Protect against {name_en}"
                ],
                "patterns_hi": [
                    f"{name_hi} क्या है?",
                    f"{name_hi} से कैसे बचें?",
                    f"{name_hi} धोखाधड़ी के बारे में बताएं",
                    f"{name_hi} सुरक्षा नियम"
                ],
                "summary_en": f"Comprehensive guidance on {name_en} based on Kavach Cybersecurity Platform guidelines.",
                "summary_hi": f"कवच साइबर सुरक्षा दिशानिर्देशों पर आधारित {name_hi} से बचाव की विस्तृत जानकारी।",
                "action_steps_en": [],
                "action_steps_hi": [],
                "red_flags": [],
                "responses_en": [],
                "responses_hi": [],
                "pro_tip_en": f"Always verify transactions and unexpected communications regarding {name_en}.",
                "pro_tip_hi": f"{name_hi} से जुड़े किसी भी अनपेक्षित संदेश या कॉल की पहले आधिकारिक स्रोत से पुष्टि करें।",
                "default_risk": 0.60
            }

        target = intent_map[target_tag]
        # Ingest questions and explanations
        for q in cat.get("questions", []):
            q_en = q["question"]["en"]
            q_hi = q["question"]["hi"]
            exp_en = q["explanation"]["en"]
            exp_hi = q["explanation"]["hi"]

            if q_en not in target["patterns_en"]:
                target["patterns_en"].append(q_en)
            if q_hi not in target["patterns_hi"]:
                target["patterns_hi"].append(q_hi)

            if exp_en and exp_en not in target["responses_en"]:
                target["responses_en"].append(exp_en)
            if exp_hi and exp_hi not in target["responses_hi"]:
                target["responses_hi"].append(exp_hi)

    # 3. Inject typo variants & definition patterns
    for tag, patterns in ADDITIONAL_PATTERNS.items():
        if tag in intent_map:
            for p in patterns:
                if re.search(r"[\u0900-\u097F]", p):
                    if p not in intent_map[tag]["patterns_hi"]:
                        intent_map[tag]["patterns_hi"].append(p)
                else:
                    if p not in intent_map[tag]["patterns_en"]:
                        intent_map[tag]["patterns_en"].append(p)

    # 4. Ingest CTDAPD Dataset stats
    telemetry_stats = {"attack_vectors": {}, "malware_types": {}, "total_records": 0}
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= 10000:
                    break
                telemetry_stats["total_records"] += 1
                vec = row.get("Attack_Vector", "None")
                mal = row.get("Malware_Type", "None")
                if vec and vec != "None":
                    telemetry_stats["attack_vectors"][vec] = telemetry_stats["attack_vectors"].get(vec, 0) + 1
                if mal and mal != "None":
                    telemetry_stats["malware_types"][mal] = telemetry_stats["malware_types"].get(mal, 0) + 1
    except Exception as e:
        print(f"Telemetry parse error: {e}")

    final_output = {
        "metadata": {
            "version": "3.1",
            "name": "Kavach-CyberBot-Unified-Refined-Dataset",
            "total_intents": len(intent_map),
            "kavach_quiz_questions": sum(len(c.get("questions", [])) for c in kavach_data.get("categories", []))
        },
        "intents": list(intent_map.values()),
        "kavach_assessments": kavach_data.get("categories", []),
        "kavach_videos": kavach_data.get("videos", []),
        "telemetry_stats": telemetry_stats
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)

    print(f"Successfully compiled refined dataset to {output_path}")
    print(f"Consolidated Intents: {len(intent_map)}")
    print(f"Phishing Patterns Total: {len(intent_map['phishing_basics']['patterns_en']) + len(intent_map['phishing_basics']['patterns_hi'])}")

if __name__ == "__main__":
    compile_dataset()
