from flask import Flask, request, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

# Два номера
PHONE_1 = "996501371580"
PHONE_2 = "996501373903"

# Хранилище сообщений отдельно по номеру
messages = {
    PHONE_1: [],
    PHONE_2: []
}

@app.route("/")
def index():
    return render_template(
        "phone.html",
        phone1=PHONE_1,
        phone2=PHONE_2,
        messages=messages
    )

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)

        to_number = str(data.get("to")).replace("+", "")
        sender = data.get("from")
        text = data.get("text")

        if to_number not in messages:
            return jsonify({"status": "ignored"}), 200

        message = {
            "from": sender,
            "text": text,
            "time": datetime.now().strftime("%H:%M")
        }

        messages[to_number].append(message)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)