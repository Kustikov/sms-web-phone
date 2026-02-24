from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Хранилище SMS в памяти
messages = []

@app.route("/", methods=["GET"])
def index():
    return render_template("phone.html", messages=messages)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    message = {
        "to": data.get("to"),
        "from": data.get("from"),
        "text": data.get("text")
    }

    messages.append(message)
    socketio.emit("new_sms", message)

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)