from flask import Flask, request, jsonify
from flask_cors import CORS
from main import run_goal  
import os
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "✅ Multi-Agent API is running!", 200

@app.route("/api/execute", methods=["POST"])
def execute_goal():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON or missing Content-Type: application/json"}), 400

    user_goal = data.get("goal", "")
    if not user_goal:
        return jsonify({"error": "No goal provided"}), 400

    logging.info(f"Received goal: {user_goal}")
    
    try:
        result = run_goal(user_goal)
        return jsonify({"result": result})
    except Exception as e:
        logging.error(f"Execution error: {e}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
