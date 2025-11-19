from flask import Flask, request, send_file
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "hello"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "mysql+pymysql://chatuser:chatpass@db/chatdb"
)
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Daniel: save message to "database" (a text file in chat_logs directory)
def save_msg_to_db(room, user, message, timestamp):
    new_msg = Message(room=room, username=user, message=message, timestamp=timestamp)
    db.session.add(new_msg)
    db.session.commit()


db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(100))
    username = db.Column(db.String(100))
    message = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)

    def __init__(self, room, username, message, timestamp):
        self.room = room
        self.username = username
        self.message = message
        self.timestamp = timestamp


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
    elif (  # Chen: get messages from "database" (a text file in chat_logs directory)
        request.method == "GET"
    ):
        messages = (
            Message.query.filter_by(room=room).order_by(Message.timestamp.asc()).all()
        )
        formated_lines = [
            f"[{m.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {m.username}: {m.message}\n"
            for m in messages
        ]
        return formated_lines, 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
