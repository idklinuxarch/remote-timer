from flask import Flask, render_template, jsonify, request
import threading
import time

app = Flask(__name__)

timer_state = {
    "running": False,
    "seconds": 0
}

# ⏱️ background timer loop
def timer_loop():
    while True:
        time.sleep(1)
        if timer_state["running"]:
            timer_state["seconds"] += 1

threading.Thread(target=timer_loop, daemon=True).start()

@app.route("/")
def home():
    return "Remote Timer Running"

@app.route("/control")
def control():
    return render_template("control.html")

@app.route("/overlay")
def overlay():
    return render_template("overlay.html")

# ▶ START
@app.route("/api/start", methods=["POST"])
def start():
    timer_state["running"] = True
    return jsonify(timer_state)

# ⏹ STOP
@app.route("/api/stop", methods=["POST"])
def stop():
    timer_state["running"] = False
    return jsonify(timer_state)

# 🔄 RESET
@app.route("/api/reset", methods=["POST"])
def reset():
    timer_state["seconds"] = 0
    timer_state["running"] = False
    return jsonify(timer_state)

# ➕ ADD TIME
@app.route("/api/add", methods=["POST"])
def add_time():
    data = request.get_json()
    seconds = data.get("seconds", 0)

    timer_state["seconds"] += seconds
    return jsonify(timer_state)

# 📡 GET STATE
@app.route("/api/state")
def state():
    return jsonify(timer_state)

if __name__ == "__main__":
    app.run(debug=True)

    import os

    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 10000))
        app.run(host="0.0.0.0", port=port)