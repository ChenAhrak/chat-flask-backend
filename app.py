from flask import Flask, request, send_file
from datetime import datetime
import mysql.connector
import os

# חיבור למסד נתונים (במקרה ש-Flask רץ בתוך Docker)
def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )

app = Flask(__name__)


# -----------------------------
# Chen + Daniel: GET /
# -----------------------------
@app.route("/")
def index():
    return send_file("Client/index.html")


# -----------------------------
# Daniel: GET /<room>
# -----------------------------
@app.route("/<room>")
def get_room(room):
    return send_file("Client/index.html")


# -----------------------------
# API: POST / GET /api/chat/<room>
# -----------------------------
@app.route("/api/chat/<room>", methods=["POST", "GET"])
def chat_rooms_endpoint(room):

    # ---------- POST: Save message ----------
    if request.method == "POST":
        user = request.form.get("username", "anonymous")
        message = request.form.get("msg")

        if not message:
            return "message is required", 400

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO messages (room, username, message, timestamp)
            VALUES (%s, %s, %s, NOW())
        """, (room, user, message))

        db.commit()
        cursor.close()
        db.close()

        return "", 204

    # ---------- GET: Get messages ----------
    elif request.method == "GET":
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT timestamp, username, message
            FROM messages
            WHERE room = %s
            ORDER BY timestamp ASC
        """, (room,))

        rows = cursor.fetchall()
        cursor.close()
        db.close()

        if not rows:
            return "", 207

        formatted_lines = [
            f"[{row['timestamp']}] {row['username']}: {row['message']}"
            for row in rows
        ]

        return "\n".join(formatted_lines), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
