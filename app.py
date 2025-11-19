from flask import Flask, send_file

app = Flask(__name__)


# get /<room>
@app.route("/<room>")
def get_room(room):
    return send_file("Client/index.html")


# post /api/chat/<room>
@app.route("/api/chat/<room>", methods=["POST"])
def post_message(room):
    raise NotImplementedError("This endpoint is not implemented yet.")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
