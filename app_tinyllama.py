from flask import Flask, request, jsonify, render_template
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

app = Flask(__name__)

model = None
tokenizer = None

def load_model():
    global model, tokenizer
    try:
        print("Loading TinyLlama...")
        tokenizer = AutoTokenizer.from_pretrained("TinyLlama/Tinyllama-1.1b-chat-v1.0")
        model = AutoModelForCausalLM.from_pretrained("TinyLlama/Tinyllama-1.1b-chat-v1.0", device_map="cpu")
        print("✅ Model loaded!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def parse_ticket(ticket_text):
    return {
        "incident_category": "technical" if any(k in ticket_text.lower() for k in ["error", "500", "bug", "crash"]) else "other",
        "affected_service": "unknown",
        "issue_summary": ticket_text[:200],
        "severity": "high" if "error" in ticket_text.lower() or "500" in ticket_text else "medium",
        "urgency": "high" if any(k in ticket_text.lower() for k in ["immediately", "asap", "urgent"]) else "medium",
        "channel": "portal",
        "status": "open",
        "confidence": 0.75
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model_loaded": model is not None})

@app.route('/parse-ticket', methods=['POST'])
def parse_api():
    data = request.get_json() or {}
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "text required"}), 400
    return jsonify(parse_ticket(text))

if __name__ == "__main__":
    if load_model():
        app.run(host="0.0.0.0", port=5000, debug=False)
