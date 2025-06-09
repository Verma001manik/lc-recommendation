import pandas as pd
import json

df = pd.read_csv("leetcode_questions.csv")

problems = []

for _, row in df.iterrows():
    tags_raw = row.get("Topic Tagged text", "")
    tags_list = [tag.strip() for tag in str(tags_raw).split(",") if tag.strip()]

    problems.append({
        "id": int(row["Question ID"]),
        "title": row["Question Title"],
        "slug": row["Question Slug"],
        "description": str(row["Question Text"]),
        "tags": tags_list,
        "difficulty": row["Difficulty Level"]
    })

with open("data/problems.json", "w") as f:
    json.dump(problems, f, indent=2)
