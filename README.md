# CyberBot: Local AI Cybersecurity Awareness Training Platform

CyberBot is a 100% local, privacy-preserving AI chatbot designed specifically for **Cybersecurity Awareness Training**. It runs entirely on your local machine using `scikit-learn` NLP classification, semantic cosine similarity retrieval, and heuristic threat inspection—requiring **zero external cloud APIs or internet connectivity**.

---

## 🌟 Key Features

### 1. 100% Local & Air-Gapped AI Engine
- **Zero Cloud Leakage**: No user prompts, company emails, or credentials ever leave your local machine.
- **Hybrid Local NLP**: Combines Sublinear TF-IDF n-grams (1-3 words), calibrated multi-class `LogisticRegression`, and semantic cosine similarity against 277+ exemplar patterns across 32 core security intents.
- **Emergency Panic Detection**: Instantly detects indicators of active compromise (e.g., *"I clicked a link"*, *"I typed my password"*, *"ransomware"*) and delivers immediate step-by-step triage and containment advice.

### 2. Interactive Phishing Message Inspector
- Paste any email header, subject line, or message text into the chat (or click **"Inspect Phishing Email"**).
- CyberBot breaks down:
  - **Risk Assessment Score** (0–100 scale: Low, Suspicious, Critical Threat)
  - **Identified Red Flags** (artificial urgency, executive impersonation, credential harvesting triggers, risky attachment extensions, shortened URLs)
  - **Recommended Action & Precautions**

### 3. Scenario-Based Cyber Quizzes
- Type `quiz` or click **"Practice Cyber Quiz"** in the sidebar.
- CyberBot tests your practical security instincts through interactive workplace scenarios (Baiting, Vishing, BEC, Password entropy, Public Wi-Fi).
- Evaluates your answers (`A`, `B`, `C`, `D`), explains why an answer is right or wrong, and scores your awareness level.

### 4. 32 Comprehensive Cybersecurity Awareness Domains
Trained locally on real-world threat vectors, including:
- **Social Engineering & Phishing**: Phishing basics, Spear Phishing, Whaling, Smishing (SMS), Vishing (Voice), BEC / CEO Fraud.
- **Identity & Authentication**: Strong Passphrases, Password Managers, 2FA/MFA, MFA Fatigue Attacks, Passkeys (FIDO2).
- **Malware & Attacks**: Ransomware isolation, Trojans, Spyware, Infostealers, Zero-Day updates.
- **Network & Device Safety**: Public Wi-Fi & Evil Twins, VPN usage, HTTPS myths, Full Disk Encryption (BitLocker/FileVault).
- **Physical & Operational Security**: Clean Desk Policy, Screen Locking, BadUSB & Juice Jacking, Remote Work & Home Router security, Insider Threats & Shadow IT.
- **Incident Response & Recovery**: First 5 minutes after a click, Account Takeover recovery, Credit Freezes & HaveIBeenPwned.

---

## 🚀 Quick Start Guide

### Requirements
- **Python 3.11+**
- Packages: `Flask`, `scikit-learn`, `numpy`

### Installation & Run

1. Open PowerShell / Terminal in the project directory:
   ```powershell
   cd "c:\Users\Acer\Desktop\Dekstop\Imp\New folder (2)\CyberBot-main"
   ```

2. Run the application:
   ```powershell
   py app.py
   # Or using python:
   python app.py
   ```

3. Open your web browser and navigate to:
   ```text
   http://127.0.0.1:5000/chat
   ```

---

## 🛠️ API Reference

### 1. `POST /api/chat`
Send a question or command to the local AI.

**Request Body:**
```json
{
  "message": "What should I do if I clicked a suspicious link?",
  "session_id": "user_session_123"
}
```

**Response:**
```json
{
  "success": true,
  "response": "Immediate action can prevent a minor error from escalating into a full organizational breach...\n\n#### 🛡️ Recommended Best Practices:\n- 1. DISCONNECT IMMEDIATELY...",
  "session_id": "user_session_123"
}
```

### 2. `POST /api/analyze/phishing`
Inspect suspicious message text for phishing indicators.

**Request Body:**
```json
{
  "text": "From support@paypa1.xyz: Urgent! Your account is suspended within 24 hours. Click here to verify."
}
```

### 3. `GET /api/status`
Returns model training status and offline metrics.

---

## 📂 Project Structure

```text
CyberBot/
├── app.py                     # Modern Flask backend with REST & legacy endpoints
├── ML/
│   └── mlScript.py            # Local NLP Engine, Phishing Inspector & Quiz Engine
├── dataset/
│   ├── cybersecurity.json     # Master dataset: 32 intents, 277 patterns, quiz scenarios
│   └── build_dataset.py       # Generator script to expand and customize the dataset
├── templates/
│   └── index.html             # Responsive chat UI with Markdown & interactive quiz pills
├── static/
│   └── styles/style.css       # Clean cybersecurity-themed styling
└── test_backend.py            # Automated test suite verifying all local AI endpoints
```

---

## 💡 Customizing & Expanding the Dataset

To add your own organization-specific policies or new questions:
1. Open `dataset/build_dataset.py`.
2. Add your new patterns, rules, or quiz questions to the `DATASET` dictionary.
3. Run:
   ```powershell
   py dataset/build_dataset.py
   ```
4. Restart `app.py`. The model will retrain on launch in under 1 second!
