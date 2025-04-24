from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.get("/")
def index():
    return "Serviço Web ativo!"

@app.post("/proxy")
def proxy():
    data = request.json or {}
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL não fornecida"}), 400
    resp = requests.get(url)
    return (resp.content, resp.status_code, resp.headers.items())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8003)
