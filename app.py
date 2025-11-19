from flask import Flask, request, send_file
from datetime import datetime

app = Flask(__name__)

# In-memory chat storage
chat_rooms = {}

# get /
@app.route("/")
def get():
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
        message_data = {"timestamp": timestamp, "user": user, "message": message}
        chat_rooms.setdefault(room, []).append(message_data)
        return "message received", 204
    else:
        raise NotImplementedError("GET method not implemented yet.")



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
