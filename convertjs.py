import pandas as pd
import json
from recommendme.data_loader import convert_to_json
import numpy as np



convert_to_json(
    path="leetcode_questions.csv",
    field_map={
        "title": "Question Title",
        "desc": "Question Text",
        "tags": "Topic Tagged text",
        "difficulty": "Difficulty Level"
    }
)