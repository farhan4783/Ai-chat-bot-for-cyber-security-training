import json
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def compile_dataset():
    kavach_path = BASE_DIR / "kavach_data.json"
    cyber_path = BASE_DIR / "cybersecurity.json"
    csv_path = BASE_DIR.parent / "CTDAPD Dataset.csv"
    output_path = BASE_DIR / "unified_cyber_dataset.json"

    with open(kavach_path, "r", encoding="utf-8") as f:
        kavach_data = json.load(f)

    with open(cyber_path, "r", encoding="utf-8") as f:
        cyber_data = json.load(f)

    # 1. Collect all distinct tags / categories
    # Combine Kavach's 11 categories with CyberBot's intents
    intent_map = {}
    
    # Process CyberBot's core intents
    for item in cyber_data.get("intents", []):
        tag = item["tag"]
        intent_map[tag] = {
            "tag": tag,
            "patterns_en": list(item.get("patterns", [])),
            "patterns_hi": [],
            "summary_en": item.get("summary", ""),
            "summary_hi": "",
            "action_steps_en": item.get("action_steps", []),
            "action_steps_hi": [],
            "responses_en": item.get("responses", []),
            "responses_hi": [],
            "pro_tip_en": item.get("pro_tip", ""),
            "pro_tip_hi": "",
            "default_risk": 0.15
        }
        if "ransomware" in tag or "emergency" in tag:
            intent_map[tag]["default_risk"] = 0.95
        elif "phishing" in tag or "credential" in tag or "malware" in tag:
            intent_map[tag]["default_risk"] = 0.75
        elif "password" in tag or "2fa" in tag:
            intent_map[tag]["default_risk"] = 0.35

    # Process Kavach categories and questions
    for cat in kavach_data.get("categories", []):
        cat_id = cat["id"]
        tag = f"kavach_{cat_id.replace('-', '_')}"
        name_en = cat["name"]["en"]
        name_hi = cat["name"]["hi"]

        if tag not in intent_map:
            intent_map[tag] = {
                "tag": tag,
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
                    f"{name_hi} सुरक्षा टिप्स"
                ],
                "summary_en": f"Comprehensive guidance on {name_en} based on Kavach Cybersecurity Platform guidelines.",
                "summary_hi": f"कवच साइबर सुरक्षा दिशानिर्देशों पर आधारित {name_hi} से बचाव की विस्तृत जानकारी।",
                "action_steps_en": [],
                "action_steps_hi": [],
                "responses_en": [],
                "responses_hi": [],
                "pro_tip_en": f"Always verify transactions and unexpected communications regarding {name_en}.",
                "pro_tip_hi": f"{name_hi} से जुड़े किसी भी अनपेक्षित संदेश या कॉल की पहले आधिकारिक स्रोत से पुष्टि करें।",
                "default_risk": 0.65
            }

        # Add questions and explanations as training patterns and knowledge
        for q in cat.get("questions", []):
            q_en = q["question"]["en"]
            q_hi = q["question"]["hi"]
            exp_en = q["explanation"]["en"]
            exp_hi = q["explanation"]["hi"]
            
            intent_map[tag]["patterns_en"].append(q_en)
            intent_map[tag]["patterns_hi"].append(q_hi)
            
            # Use explanations as canonical verified responses
            if exp_en not in intent_map[tag]["responses_en"]:
                intent_map[tag]["responses_en"].append(exp_en)
            if exp_hi not in intent_map[tag]["responses_hi"]:
                intent_map[tag]["responses_hi"].append(exp_hi)

    # 2. Extract telemetry statistics from CTDAPD Dataset.csv
    telemetry_stats = {
        "attack_vectors": {},
        "malware_types": {},
        "total_records": 0
    }
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= 10000:  # Sample top 10,000 records for telemetry profile
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

    # Build compiled training dataset
    final_output = {
        "metadata": {
            "version": "3.0",
            "name": "Kavach-CyberBot-Unified-Dataset",
            "total_intents": len(intent_map),
            "kavach_categories": len(kavach_data.get("categories", [])),
            "kavach_quiz_questions": sum(len(c.get("questions", [])) for c in kavach_data.get("categories", []))
        },
        "intents": list(intent_map.values()),
        "kavach_assessments": kavach_data.get("categories", []),
        "kavach_videos": kavach_data.get("videos", []),
        "telemetry_stats": telemetry_stats
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)

    print(f"Successfully compiled unified dataset to {output_path}")
    print(f"Total Intents: {len(intent_map)}")
    print(f"Total Quiz Questions from Kavach: {final_output['metadata']['kavach_quiz_questions']}")

if __name__ == "__main__":
    compile_dataset()

