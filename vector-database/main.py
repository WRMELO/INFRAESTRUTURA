from flask import Flask, request, jsonify
import numpy as np
import faiss

app = Flask(__name__)

# Dimensão do vetor (ajuste conforme necessário)
dim = 128
index = faiss.IndexFlatL2(dim)

@app.post("/add")
def add_vectors():
    payload = request.json or {}
    vectors = np.array(payload.get("vectors", []), dtype='float32')
    if vectors.ndim == 1:
        vectors = vectors.reshape(1, -1)
    start_id = index.ntotal
    index.add(vectors)
    added_ids = list(range(start_id, start_id + vectors.shape[0]))
    return jsonify({"added_ids": added_ids})

@app.post("/search")
def search():
    payload = request.json or {}
    vector = np.array(payload.get("vector", []), dtype='float32')
    vector = vector.reshape(1, -1)
    k = int(payload.get("k", 5))
    distances, indices = index.search(vector, k)
    return jsonify({
        "distances": distances.tolist(),
        "ids": indices.tolist()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)
