import os
from flask import Flask, request, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Список номеров
NUMBERS = ["996501371580", "996501373903"]

# Хранилище сообщений в памяти
messages = {num: [] for num in NUMBERS}

# --- WEBHOOK ---
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    to_number = data.get("to")
    sender = data.get("from")
    text = data.get("text")

    if to_number not in NUMBERS:
        return "Unknown number", 404

    msg = {"sender": sender, "text": text}
    messages[to_number].append(msg)

    # пушим в Web UI
    socketio.emit("new_sms", {"number": to_number, "sender": sender, "text": text})
    return "OK"

# --- WEB UI ---
@app.route("/")
def index():
    return render_template("templates/phone.html", numbers=NUMBERS, messages=messages)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)