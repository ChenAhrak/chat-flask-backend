from flask import Flask, json, request, send_file
from datetime import datetime


app = Flask(__name__)


def save_msg_to_db(room, user, message, timestamp):
    with open(f"chat_logs/{room}.txt", "a") as f:
        json.dump(
            {"user": user, "message": message, "timestamp": timestamp.isoformat()}, f
        )
        f.write("\n")

@app.route("/")
def index():
    return send_file("Client/index.html")

# get /<room>
@app.route("/<room>")
def get_room(room):
    return send_file("Client/index.html")


# /api/chat/<room>
@app.route("/api/chat/<room>", methods=["POST", "GET"])
def chat_rooms_endpoint(room):
    if request.method == "POST":
        user = request.form.get("username")
        message = request.form.get("msg")
        timestamp = datetime.now()
        save_msg_to_db(room, user, message, timestamp)
        return "message saved", 204
    elif request.method == "GET":
        try:
            with open(f"chat_logs/{room}.txt", "r") as f:
                lines = f.readlines()

            # החזרת הטקסט כמו שהפרונט־אנד מצפה
            return "".join(lines), 200

        except FileNotFoundError:
            # חדר ריק – אין עדיין קובץ
            return "", 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)