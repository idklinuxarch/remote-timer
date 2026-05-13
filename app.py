from flask import Flask, render_template, jsonify, request
import threading
import time
import os

app = Flask(__name__)

# 🔒 CHANGE THIS PASSWOR
SECRET_KEY = "Oxford123"

timer_state = {
    "running": False,
    "seconds": 0
}

# ⏱ timer loop
def timer_loop():
    while True:
        time.sleep(1)
        if timer_state["running"]:
            timer_state["seconds"] += 1

threading.Thread(target=timer_loop, daemon=True).start()

# 🏠 pages
@app.route("/")
def home():
    return "Remote Timer Running"

@app.route("/control")
def control():
    return render_template("control.html")

@app.route("/overlay")
def overlay():
    return render_template("overlay.html")

# 🔐 helper check
def check_key():
    return request.headers.get("key") == SECRET_KEY

# ▶ start
@app.route("/api/start", methods=["POST"])
def start():
    if not check_key():
        return "Unauthorized", 401

    timer_state["running"] = True
    return jsonify(timer_state)

# ⏹ stop
@app.route("/api/stop", methods=["POST"])
def stop():
    if not check_key():
        return "Unauthorized", 401

    timer_state["running"] = False
    return jsonify(timer_state)

# 🔄 reset
@app.route("/api/reset", methods=["POST"])
def reset():
    if not check_key():
        return "Unauthorized", 401

    timer_state["seconds"] = 0
    timer_state["running"] = False
    return jsonify(timer_state)

# ➕ add time
@app.route("/api/add", methods=["POST"])
def add_time():
    if not check_key():
        return "Unauthorized", 401

    data = request.get_json()
    seconds = data.get("seconds", 0)

    timer_state["seconds"] += seconds
    return jsonify(timer_state)

# 📡 state (overlay)
@app.route("/api/state")
def state():
    return jsonify(timer_state)

# 🚀 run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
