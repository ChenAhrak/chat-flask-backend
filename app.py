from flask import Flask, json, request, send_file
from datetime import datetime
import os

app = Flask(__name__)
CHAT_LOGS_DIR = "chat_logs"
os.makedirs(CHAT_LOGS_DIR, exist_ok=True)


# Daniel: save message to "database" (a text file in chat_logs directory)
def save_msg_to_db(room, user, message, timestamp):
    with open(f"chat_logs/{room}.txt", "a") as f:
        json.dump(
            {"user": user, "message": message, "timestamp": timestamp.isoformat()}, f
        )
        f.write("\n")


# Chen: get /
@app.route("/")
def index():
    return send_file("Client/index.html")


# Daniel:get /<room>
@app.route("/<room>")
def get_room(room):
    return send_file("Client/index.html")


# Daniel: /api/chat/<room>
@app.route("/api/chat/<room>", methods=["POST", "GET"])
def chat_rooms_endpoint(room):
    if request.method == "POST":
        user = request.form.get("username", "anonymous")
        message = request.form.get("msg")
        if not message:
            return "message is required", 400
        timestamp = datetime.now()
        save_msg_to_db(room, user, message, timestamp)
        return "message saved", 204
    elif (
        request.method == "GET"
    ):  # Chen: get messages from "database" (a text file in chat_logs directory)
        try:
            with open(f"chat_logs/{room}.txt", "r") as f:
                lines = f.readlines()
            return "".join(lines), 200

        except FileNotFoundError:
            return "", 207  # No messages yet


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
