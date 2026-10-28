import os
import secrets
from flask import Flask, jsonify, render_template, request

from ML.mlScript import Model

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", secrets.token_hex(16))


@app.route("/", methods=["GET"])
@app.route("/chat", methods=["GET", "POST"])
def chat():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """Modern JSON POST endpoint for conversational AI."""
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    session_id = data.get("session_id", "default")
    response_text = Model.respond(message, session_id=session_id)
    return jsonify({
        "success": True,
        "response": response_text,
        "session_id": session_id
    })


@app.route("/api/analyze/phishing", methods=["POST"])
def api_analyze_phishing():
    """Dedicated endpoint for inspecting suspicious email or message text."""
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    if not text.strip():
        return jsonify({"success": False, "error": "No text provided for inspection."}), 400
    report = Model.analyze_phishing_message(text)
    return jsonify({"success": True, "report": report})


@app.route("/api/quiz", methods=["POST", "GET"])
def api_quiz():
    """Dedicated endpoint to interact with the quiz engine."""
    session_id = request.args.get("session_id") or (request.get_json(silent=True) or {}).get("session_id", "default")
    answer = request.args.get("answer") or (request.get_json(silent=True) or {}).get("answer", "")
    session = Model.get_session(session_id)
    
    if request.method == "GET" and not answer:
        session["quiz_active"] = False
        quiz_response = Model.handle_quiz(session)
    else:
        quiz_response = Model.handle_quiz(session, answer)
        
    return jsonify({"success": True, "response": quiz_response, "session_id": session_id})


@app.route("/api/status", methods=["GET"])
def api_status():
    """Returns local AI health, model parameters, and offline capability status."""
    return jsonify({
        "status": "online",
        "model_type": "100% Local Scikit-Learn NLP Engine",
        "offline_only": True,
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
