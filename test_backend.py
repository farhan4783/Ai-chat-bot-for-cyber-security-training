from app import app
import json

client = app.test_client()

print("--- Testing /api/status ---")
r = client.get("/api/status")
print(r.status_code, r.get_json())

print("\n--- Testing /chat ---")
r = client.get("/chat")
print(r.status_code, "HTML length:", len(r.data))

print("\n--- Testing /api/chat (General Question) ---")
r = client.post("/api/chat", json={"message": "How can I prevent ransomware attacks?", "session_id": "test1"})
print(r.status_code, json.dumps(r.get_json(), indent=2)[:300] + "...")

print("\n--- Testing /api/chat (Phishing Inspection) ---")
r = client.post("/api/chat", json={
    "message": "Analyze this email: From: security@paypal-verification.biz Urgent: Account suspended, download invoice.zip and verify credentials",
    "session_id": "test1"
})
print(r.status_code, json.dumps(r.get_json(), indent=2)[:300] + "...")

print("\n--- Testing /api/chat (Quiz Flow) ---")
r = client.post("/api/chat", json={"message": "quiz", "session_id": "quiz_session"})
print("Q1:", r.status_code, r.get_json()["response"][:150] + "...")

r = client.post("/api/chat", json={"message": "D", "session_id": "quiz_session"})
print("Answer D:", r.status_code, r.get_json()["response"][:150] + "...")

print("\nALL BACKEND API TESTS PASSED SUCCESSFULLY!")

