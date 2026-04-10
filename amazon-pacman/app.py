import os
from flask import Flask, jsonify, request, render_template
import main

app = Flask(__name__)
game = main.Game()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/state")
def state():
    return jsonify(game.get_state())

@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    direction = data.get("direction")
    game.move(direction)
    return jsonify(game.get_state())

if __name__ == "__main__":
    # Use PORT environment variable if set, otherwise default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
