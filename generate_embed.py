import json 
import os 
import faiss 
import numpy as np 
from sentence_transformers import SentenceTransformer

with open("data/problems.json", "r" ) as f :
    problems = json.load(f)

model = SentenceTransformer("BAAI/bge-small-en")

texts = [
    f"{p['title']}. {p['description']} Difficulty: {p['difficulty']}. Tags: {', '.join(p['tags'])}"
    for p in problems
]

embeddings = model.encode(texts,normalize_embeddings=True)
print("embeddings: ", embeddings)
os.makedirs("embeddings", exist_ok=True)
with open("embeddings/id_map.json", "w") as f:
    json.dump(problems, f, indent=2)

dimension = embeddings.shape[1]
print("dimension: ", dimension)
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))
faiss.write_index(index,"embeddings/faiss_index.bin")

print(" All done! FAISS index and metadata saved.")