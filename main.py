from flask import Flask, render_template, redirect, request
import random
from recommendme.search import SearchEngine

app = Flask(__name__)

search_engine = SearchEngine(
    index_path="embeddings/leetcode_questions.csv.json_faiss_index.bin",
    metadata_path="embeddings/leetcode_questions.csv.json_id_map.json"
)

problems = search_engine.metadata 

@app.route("/")
def home():
    featured_problems = random.sample(problems, min(12, len(problems)))
    return render_template("index.html", results=featured_problems, selected_problem=None)

@app.route("/search", methods=["GET", "POST"])
def search():
    query = None
    selected_problem = None
    results = []
    
    if request.method == "POST":
        query = request.form.get("query")
        if not query or len(query.strip()) < 2:
            return redirect("/")
        
        results = search_engine.search(query, top_k=12)

    else:
        problem_id = request.args.get("q")
        if not problem_id or not problem_id.isdigit():
            return redirect("/")
            
        problem_id = int(problem_id)
        selected_problem = next((p for p in problems if p["id"] == problem_id), None)
        
        if not selected_problem:
            return redirect("/")

        query_text = f"{selected_problem['title']}. {selected_problem['desc']} Difficulty: {selected_problem['difficulty']}. Tags: {', '.join(selected_problem['tags'])}"
        results = search_engine.search(query_text, top_k=12, exclude_id=selected_problem["id"])
    
    return render_template("index.html", results=results, selected_problem=selected_problem, no_results=len(results) == 0)

if __name__ == '__main__':
    app.run(debug=True)
