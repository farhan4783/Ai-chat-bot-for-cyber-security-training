# CyberBot Startup & Verification Guide (1M Parameter Model)

Follow these steps to run and test CyberBot with the newly trained **Kavach-Net-1M** deep learning model.

## 1. Open PowerShell in the project directory
```powershell
cd "c:\Users\Acer\Desktop\Dekstop\Imp\New folder (2)\CyberBot-main"
```

## 2. Run the Automated Test Suite
Verify that the 1M parameter model, bilingual engine, phishing analyzer, and quiz state machine are healthy:
```powershell
py test_backend.py
```
*(You will see all 8 API tests pass with status code 200 and model status showing 1,341,676 parameters)*

## 3. Run the Web Application
```powershell
py app.py
```

## 4. Open in Your Browser
Visit:
```text
http://127.0.0.1:5000/chat
```

---

## 5. Exciting Scenarios to Test

1. **English Phishing & Awareness**:
   - Ask: `What is phishing?`
   - Observe the structured security steps, pro tip, and the neural threat assessment confidence badge.

2. **Hindi Bilingual Support (Kavach Alignment)**:
   - Ask: `UPI PIN डालते समय क्या सावधानियां रखनी चाहिए?`
   - Observe the AI responding natively in Hindi explaining UPI scam mechanics.

3. **Emergency Panic Containment**:
   - Ask: `I clicked a suspicious link and typed my password what do I do?`
   - CyberBot detects emergency panic triggers and outputs the immediate 5-step containment checklist.

4. **110-Question Kavach Quiz Engine**:
   - Click **"Practice Cyber Quiz"** in the sidebar or type `quiz`.
   - Test your security knowledge with questions pulled directly from the Kavach platform across 11 core categories!
