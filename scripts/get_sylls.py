import re
import json

import pandas as pd

from pipr3.views import no_syllables


def get_sylls(text):
    """Get the no. syllables in a text"""
    words = re.findall("[a-z]+", text.lower())

    sylls = sum(no_syllables(word) for word in words)

    return sylls


stims = json.load(open("pipr3/data/stimuli.json"))

syll_data = []

for item in stims:
    for stim in item:
        row_data = {"item_id": stim['item_id']}
        row_data['passage_sylls'] = get_sylls(stim['stimulus'])
        syll_data.append(row_data)

df = pd.DataFrame(syll_data)

df.to_csv("pipr3/data/syll_data.csv")
df.to_csv("~/Documents/ucsd/projects/pronouns/pipr/analysis/pipr3/syll_data.csv")


# PIPR 1

df = pd.read_csv("pronouns/data/stimuli.csv")

df = df[["item_id", "syntax_question", "physics_question", "expt_question"]]

df = df.rename(columns={"syntax_question": "Syntax norming",
                        "physics_question": "Physics norming",
                        "expt_question": "Experimental"})

df = df.melt(id_vars="item_id", var_name="condition", value_name="question")

df['sylls'] = [get_sylls(q) for q in df.question]

df.to_csv("pronouns/data/question_syllables.csv")
