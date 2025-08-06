from recommendme.embeddings import Embedding
embedder = Embedding(path="data/leetcode_questions.csv.json")
embedder.generate_embeddings()

print("FAISS index created and metadata saved!")

index = embedder.get_faiss_embeddings()
metadata = embedder.get_metadata()

print(f"Loaded FAISS index with {index.ntotal} vectors")
print(f"Metadata loaded: {len(metadata)} entries")
