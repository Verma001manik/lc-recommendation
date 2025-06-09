from flask import Flask, render_template, redirect, request
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import random

app = Flask(__name__)
model = SentenceTransformer("BAAI/bge-small-en")

# Load problems and FAISS index
with open("embeddings/id_map.json", "r") as f:
    problems = json.load(f)
index = faiss.read_index("embeddings/faiss_index.bin")

# Distance threshold to filter out gibberish/unrelated results
MAX_DISTANCE_THRESHOLD = 0.3

@app.route("/")
def home():
    featured_problems = random.sample(problems, min(12, len(problems)))
    return render_template("index.html", results=featured_problems, selected_problem=None)

# @app.route("/search", methods=["GET", "POST"])
# def search():
#     query = None
#     selected_problem = None

#     if request.method == "POST":
#         # Search using user input text
#         query = request.form.get("query")
#         if not query:
#             return redirect("/")
#         embedding = model.encode([query.lower()], convert_to_numpy=True).astype("float32")

#     else:
#         # Lookup by problem ID
#         problem_id = request.args.get("q")
#         if not problem_id or not problem_id.isdigit():
#             return redirect("/")

#         problem_id = int(problem_id)
#         selected_problem = next((p for p in problems if p["id"] == problem_id), None)
#         if not selected_problem:
#             return redirect("/")

#         # Convert selected problem into text form for embedding
#         query_text = f"{selected_problem['title']}. {selected_problem['description']} Difficulty: {selected_problem['difficulty']}. Tags: {', '.join(selected_problem['tags'])}"
#         embedding = model.encode([query_text], convert_to_numpy=True).astype("float32")

#     # Search similar problems
#     distances, indices = index.search(embedding, 12)

#     # Filter bad matches
#     filter_id = selected_problem["id"] if selected_problem else -1
#     results = [
#         problems[i]
#         for dist, i in zip(distances[0], indices[0])
#         if dist < MAX_DISTANCE_THRESHOLD and problems[i]["id"] != filter_id
#     ]

#     return render_template("index.html", results=results, selected_problem=selected_problem)
@app.route("/search", methods=["GET", "POST"])
def search():
    query = None
    selected_problem = None
    results = []
    
    if request.method == "POST":
        # Search using user input text
        query = request.form.get("query")
        if not query or len(query.strip()) < 2:  # Check for empty or very short queries
            return redirect("/")
        
        embedding = model.encode([query.lower()], convert_to_numpy=True).astype("float32")
        
        # Search similar problems
        distances, indices = index.search(embedding, 12)
        
        print(f"\n🔍 Query: '{query}'")
        print("🔢 Distances:", distances[0])
        # Check if the best match is too far (gibberish)
        if distances[0][0] >= MAX_DISTANCE_THRESHOLD:
            # No good matches found - return empty results
            return render_template("index.html", results=[], selected_problem=None, no_results=True)
            
        # Filter bad matches
        results = [
            problems[i]
            for dist, i in zip(distances[0], indices[0])
            if dist < MAX_DISTANCE_THRESHOLD
        ]
        
    else:
        # Lookup by problem ID (unchanged)
        problem_id = request.args.get("q")
        if not problem_id or not problem_id.isdigit():
            return redirect("/")
            
        problem_id = int(problem_id)
        selected_problem = next((p for p in problems if p["id"] == problem_id), None)
        
        if not selected_problem:
            return redirect("/")
            
        # Convert selected problem into text form for embedding
        query_text = f"{selected_problem['title']}. {selected_problem['description']} Difficulty: {selected_problem['difficulty']}. Tags: {', '.join(selected_problem['tags'])}"
        embedding = model.encode([query_text], convert_to_numpy=True).astype("float32")
        
        # Search similar problems
        distances, indices = index.search(embedding, 12)
        print(f"\n🔍 Query: '{query}'")
        print("🔢 Distances:", distances[0])
        # Filter bad matches and exclude the selected problem
        results = [
            problems[i]
            for dist, i in zip(distances[0], indices[0])
            if dist < MAX_DISTANCE_THRESHOLD and problems[i]["id"] != selected_problem["id"]
        ]
    
    return render_template("index.html", results=results, selected_problem=selected_problem, no_results=len(results) == 0)
if __name__ == '__main__':
    app.run(debug=True)
