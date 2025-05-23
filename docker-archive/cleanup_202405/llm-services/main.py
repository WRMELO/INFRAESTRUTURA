from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.post("/ask")
def ask():
    payload = request.json
    prompt = payload.get("prompt", "")
    # TODO: implementar chamada ao LLM (por exemplo, via requests)
    response = {"answer": f"Você perguntou: {prompt}"}
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
