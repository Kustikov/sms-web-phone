import os
from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, emit

# Определяем путь к текущей директории
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Явно указываем папку templates
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))
socketio = SocketIO(app, cors_allowed_origins="*")

# Храним SMS в памяти (без базы данных)
messages = []

# Главная страница (Web Phone UI)
@app.route("/")
def index():
    return render_template("phone.html", messages=messages)

# Webhook для приема SMS от провайдера
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)

        to_number = data.get("to")
        sender = data.get("from")
        text = data.get("text")

        if not to_number or not sender or not text:
            return jsonify({"status": "error", "message": "Invalid data"}), 400

        message = {
            "to": to_number,
            "from": sender,
            "text": text
        }

        # Сохраняем в памяти
        messages.append(message)

        # Отправляем в реальном времени в UI
        socketio.emit("new_sms", message)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print("Webhook error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# Точка входа
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)