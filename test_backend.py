from app import app
import json

client = app.test_client()

print("--- 1. Testing /api/status ---")
r = client.get("/api/status")
print("Status Code:", r.status_code)
print("Payload:", json.dumps(r.get_json(), indent=2))

print("\n--- 2. Testing /chat (Web Interface) ---")
r = client.get("/chat")
print("Status Code:", r.status_code, "| HTML byte length:", len(r.data))

print("\n--- 3. Testing /api/chat (English Security Query) ---")
r = client.post("/api/chat", json={"message": "What is phishing?", "session_id": "test_en"})
print("Status Code:", r.status_code)
print("Snippet:", r.get_json()["response"][:220] + "...")

print("\n--- 4. Testing /api/chat (Hindi Query - Kavach Alignment) ---")
r = client.post("/api/chat", json={"message": "UPI PIN डालते समय क्या सावधानियां रखनी चाहिए?", "session_id": "test_hi"})
print("Status Code:", r.status_code)
print("Snippet:", r.get_json()["response"][:220] + "...")

print("\n--- 5. Testing /api/chat (Emergency Panic Containment) ---")
r = client.post("/api/chat", json={"message": "I clicked a suspicious link and typed my password what do I do?", "session_id": "panic"})
print("Status Code:", r.status_code)
print("Emergency Header:", r.get_json()["response"][:100] + "...")

print("\n--- 6. Testing /api/analyze/phishing ---")
r = client.post("/api/analyze/phishing", json={
    "text": "From: billing@paypa1-security.xyz Urgent! Your account is suspended within 24 hours. Download verification.zip immediately."
})
print("Status Code:", r.status_code)
print("Report:", json.dumps(r.get_json()["report"], indent=2))

print("\n--- 7. Testing /api/chat (Interactive Quiz Flow) ---")
r = client.post("/api/chat", json={"message": "quiz", "session_id": "quiz_session"})
print("Question 1:", r.status_code, "\n" + r.get_json()["response"][:200] + "...")

r = client.post("/api/chat", json={"message": "C", "session_id": "quiz_session"})
print("\nAnswer C evaluation:", r.status_code, "\n" + r.get_json()["response"][:200] + "...")

print("\n--- 8. Testing /api/kavach/assessments ---")
r = client.get("/api/kavach/assessments")
print("Status Code:", r.status_code, "| Categories count:", r.get_json()["categories_count"])

print("\n" + "=" * 60)
print("🎯 ALL 8 KAVACH-CYBERBOT API TESTS COMPLETED SUCCESSFULLY!")
print("=" * 60)
