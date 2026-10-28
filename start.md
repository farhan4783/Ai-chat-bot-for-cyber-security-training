# CyberBot Startup & Verification Guide

Follow these steps to run and test CyberBot locally.

## 1. Open PowerShell in the project directory
```powershell
cd "c:\Users\Acer\Desktop\Dekstop\Imp\New folder (2)\CyberBot-main"
```

## 2. Verify / Run the Automated Test Suite
Run the test script to verify that the local AI model, phishing inspector, and quiz state machine are healthy:
```powershell
py test_backend.py
```

## 3. Run the Web Application
```powershell
py app.py
```
*(If `py` is not mapped, use `python app.py`)*

## 4. Open in Your Browser
Visit:
```text
http://127.0.0.1:5000/chat
```

---

## 5. Features to Try in the Browser

1. **Interactive Security Scenario Quiz**:
   - Click **"Practice Cyber Quiz"** in the sidebar or type `quiz`.
   - The bot presents scenario questions and click-to-answer buttons (`Option A`, `Option B`, `Option C`, `Option D`).
   - Try answering with **D** on the first question to see the instant feedback and next scenario.

2. **Phishing Email Inspector**:
   - Click the prompt card **"Phishing Analyzer"** or paste any suspicious email:
   - Example prompt:
     ```text
     Analyze this email: From: billing@paypa1-update.com Subject: Urgent Account Suspension. Click here to verify your identity.
     ```
   - CyberBot returns an instant **Risk Assessment Score** with red-flag breakdown.

3. **Emergency Incident Triage**:
   - Ask:
     ```text
     I clicked a suspicious link and typed my password what do I do?
     ```
   - CyberBot detects emergency panic triggers and outputs the immediate 5-step containment checklist.
