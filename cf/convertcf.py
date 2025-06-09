import pandas as pd
import json
import math

df = pd.read_csv("cf.csv")
problems = []

for _, row in df.iterrows():
    tags = row["problem_tags"]
    
    # Handle NaN tags
    if pd.isna(tags):
        tags_list = []
    else:
        tags_list = [tag.strip() for tag in tags.split(",")]

    if pd.isna(row["problem_statement"]):
        continue
    problems.append({
        "contest": int(row["contest"]) if not pd.isna(row["contest"]) else None,
        "problem_name": row["problem_name"],
        "problem_statement": row["problem_statement"],
        "problem_tags": tags_list
    })

with open("data/codeforces.json", "w") as f:
    json.dump(problems, f, indent=2)
