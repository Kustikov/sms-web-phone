from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Хранилище SMS в памяти
messages = []

@app.route("/")
def index():
    return render_template("phone.html", messages=messages)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)

        message = {
            "to": data.get("to"),
            "from": data.get("from"),
            "text": data.get("text")
        }

        messages.append(message)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)