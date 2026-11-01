# CyberBot: Local AI Cybersecurity Awareness Platform (Kavach-Net-1M)

CyberBot is a 100% local, privacy-preserving AI chatbot powered by **Kavach-Net-1M**—a dedicated **~1.34 Million Parameter Deep Learning Neural Network** trained specifically on modern cybersecurity threat vectors, bilingual English/Hindi threat curricula, and network attack telemetry.

Built as the intelligence backend for the [Kavach Cybersecurity Platform](https://github.com/SalmanKhan123-dev/Kavach-Cybersecurity-Platform.git), CyberBot executes in **< 15ms on local CPU** with zero external cloud or GPU requirements.

---

## 🌟 Key Features

### 1. 1-Million Parameter Deep Learning Model ("Kavach-Net-1M")
- **Custom Neural Architecture**: 2-layer Bidirectional GRU + 4-Head Scaled Dot-Product Attention + Multi-Task Output Heads.
- **Exact Parameter Count**: **1,341,676 parameters** (FP32 size: 5.3 MB).
- **Multi-Task Outputs**:
  - **Head A**: Multi-Class Intent Classifier across 43 security domains.
  - **Head B**: Threat Severity & Phishing Risk Regressor (0.0 – 1.0).
  - **Head C**: 128-dimensional Normalized Semantic Embeddings for response retrieval.

### 2. Bilingual English & Hindi Security Intelligence
- Seamlessly comprehends prompts and delivers guidance in both **English (`en`)** and **Hindi (`hi`)**.
- Incorporates the complete bilingual curriculum and question bank from the Kavach Cybersecurity Platform.

### 3. Comprehensive 43 Cybersecurity Domains & 110 Scenarios
Covers all 11 Kavach core categories and 32 CyberBot sub-domains:
- **Financial & Payment Security**: UPI Fraud, QR Code Scams (Quishing), OTP Theft, Net-Banking Traps.
- **Social Engineering**: Spear Phishing, CEO Fraud / BEC, Impersonation, Pretexting, Job Scams, Shopping Fraud.
- **Identity & Devices**: Passphrases, Password Managers, 2FA/MFA, Passkeys, Public Wi-Fi & Evil Twins.
- **Incident Response**: Emergency panic detection, active account takeover containment, credential exposure steps.

### 4. Real-Time Phishing & Scam Inspector
- Inspects emails, SMS, and messages for 7 distinct threat indicators (urgency, credential lures, shortened URLs, malware attachments).
- Evaluates risk score (0–100) using neural regression blended with rule-based heuristics.

### 5. Interactive Scenario Quiz Engine
- Powered by **110 verified assessment scenarios** across all 11 Kavach domains.
- Multi-turn state machine evaluates choices (`A`, `B`, `C`, `D`), delivers immediate explanations, and scores awareness levels.

---

## 🚀 Quick Start Guide

### Requirements
- **Python 3.11+** (Tested on Python 3.14)
- Packages: `Flask`, `torch`, `numpy`, `scikit-learn`

### Run the Application

1. Open PowerShell / Terminal:
   ```powershell
   cd "c:\Users\Acer\Desktop\Dekstop\Imp\New folder (2)\CyberBot-main"
   ```

2. Run the automated test suite:
   ```powershell
   py test_backend.py
   ```

3. Launch the web application:
   ```powershell
   py app.py
   ```

4. Open your browser:
   ```text
   http://127.0.0.1:5000/chat
   ```

---

## 🛠️ API Reference

### 1. `POST /api/chat`
Conversational endpoint with automatic language detection and risk scoring.
```json
{
  "message": "UPI PIN डालते समय क्या सावधानियां रखनी चाहिए?",
  "session_id": "user_session_1",
  "language": "hi"
}
```

### 2. `POST /api/analyze/phishing`
Inspects email or message snippets for phishing red flags.
```json
{
  "text": "From: billing@paypa1-update.com Subject: Urgent Account Suspension. Click here to verify."
}
```

### 3. `GET /api/status`
Returns model health, parameter count, and offline capability status.

### 4. `GET /api/kavach/assessments`
Returns the complete 11-category Kavach quiz curriculum and scenario database.

---

## 🔗 Integration with Kavach React Frontend
To connect the [Kavach Cybersecurity Platform](https://github.com/SalmanKhan123-dev/Kavach-Cybersecurity-Platform.git) directly:
1. Copy the updated [`Chatbot.jsx`](file:///C:/Users/Acer/.gemini/antigravity/brain/c9f84614-e3ba-49f2-8cd6-a3aef123653d/scratch/kavach_repo/src/pages/Chatbot.jsx) into `Kavach-Cybersecurity-Platform/src/pages/Chatbot.jsx`.
2. Ensure CyberBot's Flask server is running on `http://127.0.0.1:5000`.
3. The React app will automatically communicate with the local 1M-parameter AI engine!
