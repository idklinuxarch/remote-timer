from flask import Flask, jsonify, send_file
import os

app = Flask(__name__)

state = {
    "seconds": 300,
    "running": False
}

@app.route("/api/state")
def api_state():
    return jsonify(state)

@app.route("/api/start")
def start():
    state["running"] = True
    return jsonify(state)

@app.route("/api/stop")
def stop():
    state["running"] = False
    return jsonify(state)

@app.route("/api/add")
def add():
    state["seconds"] += 60
    return jsonify(state)

@app.route("/overlay")
def overlay():
    return send_file("overlay.html")

@app.route("/control")
def control():
    return send_file("control.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)