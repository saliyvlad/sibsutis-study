import signal
import sys
import os
from flask import Flask, jsonify

app = Flask(__name__)

def handle_sigterm(signum, frame):
    print(f"[INFO] Получен сигнал {signum}, корректное завершение работы...", flush=True)
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGINT, handle_sigterm)

@app.route("/")
def index():
    return jsonify({
        "message": "Hello from containerized app!",
        "pid": os.getpid(),
        "status": "running"
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)