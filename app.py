from flask import Flask, jsonify, render_template, request

from ML.mlScript import Model

app = Flask(__name__)


@app.route("/home", methods=["GET", "POST"])
def home():
    return "welcome"


@app.route("/chat", methods=["GET", "POST"])
def chat():
    return render_template("index.html")


@app.route("/bot/response/")
def bot_response():
    user_input = request.args.get("msg", "", type=str)
    return jsonify(response=Model.respond(user_input))


if __name__ == "__main__":
    app.run(debug=True)
