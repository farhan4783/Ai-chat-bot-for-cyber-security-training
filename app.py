import os
import secrets
from flask import Flask, jsonify, render_template, request

from ML.mlScript import Model

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", secrets.token_hex(16))

# Simple CORS handler for Kavach React Frontend
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.route("/", methods=["GET"])
@app.route("/chat", methods=["GET", "POST"])
def chat():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST", "OPTIONS"])
def api_chat():
    """Modern JSON POST endpoint for conversational AI."""
    if request.method == "OPTIONS":
        return jsonify({"success": True}), 200
        
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    session_id = data.get("session_id", "default")
    language = data.get("language", None)
    
    response_text = Model.respond(message, session_id=session_id, language=language)
    return jsonify({
        "success": True,
        "response": response_text,
        "session_id": session_id,
        "model": "KavachNet1M (1.34M Parameters)"
    })


@app.route("/api/analyze/phishing", methods=["POST", "OPTIONS"])
def api_analyze_phishing():
    """Dedicated endpoint for inspecting suspicious email or message text."""
    if request.method == "OPTIONS":
        return jsonify({"success": True}), 200
        
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    if not text.strip():
        return jsonify({"success": False, "error": "No text provided for inspection."}), 400
    report = Model.analyze_phishing_message(text)
    return jsonify({"success": True, "report": report})


@app.route("/api/quiz", methods=["POST", "GET", "OPTIONS"])
def api_quiz():
    """Dedicated endpoint to interact with the quiz engine."""
    if request.method == "OPTIONS":
        return jsonify({"success": True}), 200
        
    session_id = request.args.get("session_id") or (request.get_json(silent=True) or {}).get("session_id", "default")
    answer = request.args.get("answer") or (request.get_json(silent=True) or {}).get("answer", "")
    language = request.args.get("language") or (request.get_json(silent=True) or {}).get("language", "en")
    
    session = Model.get_session(session_id)
    
    if request.method == "GET" and not answer:
        session["quiz_active"] = False
        quiz_response = Model.handle_quiz(session, language=language)
    else:
        quiz_response = Model.handle_quiz(session, answer, language=language)
        
    return jsonify({"success": True, "response": quiz_response, "session_id": session_id})


@app.route("/api/kavach/assessments", methods=["GET"])
def api_kavach_assessments():
    """Exposes the full Kavach 11-category curriculum and questions."""
    return jsonify({
        "success": True,
        "categories_count": len(Model.kavach_assessments),
        "categories": Model.kavach_assessments
    })


@app.route("/api/status", methods=["GET"])
def api_status():
    """Returns local AI health, model parameters, and offline capability status."""
    return jsonify({
        "status": "online",
        "model_name": "Kavach-Net-1M",
        "model_type": "Dedicated ~1.34M Parameter Deep Learning Neural Core",
        "parameters": 1341676,
        "offline_only": True,
        "bilingual_support": ["English (en)", "Hindi (hi)"],
        "total_intents": len(Model.intents),
        "total_patterns": len(Model.patterns),
        "quiz_scenarios": len(Model.quiz_questions)
    })


# Legacy endpoint for backward compatibility
@app.route("/bot/response/")
def bot_response():
    user_input = request.args.get("msg", "", type=str)
    session_id = request.args.get("session_id", "default", type=str)
    return jsonify(response=Model.respond(user_input, session_id=session_id))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
