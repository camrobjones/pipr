"""
Transform raw text of stims into json
"""

import re
import json


with open("pipr2/data/stims_raw.txt") as f:
    text = f.read()

pattern = "Intro: +"

stim_secs = re.split(pattern, text)

stim_secs = stim_secs[1:]  # discard intro text of 1

stimuli_list = []

for i, sec in enumerate(stim_secs):
    print(i)

    # Store both order versions of stimulus
    version_list = []

    # Split into passage and questions
    passage, questions_text = re.split(r"\s+Questions:\s+", sec)

    """
    Format questions
    """

    # Remove next question title
    question_text = re.sub(r"\s+[1-9]+\. .*", "", questions_text)

    # Split into questions
    questions = re.split("\n(CQ[123C]: .*)\n", question_text)

    """
    Format passage
    """

    # Remove subsection markers
    passage = re.sub("\n(Setup|Critical|Continuation):", "", passage)
    # Extract keywords
    p_parts = re.split("[\{\}]", passage)

    # Create two versions of passage
    for order in ["A", "B"]:

        # Optionally swap keywords
        if order == "B":
            p_parts[1], p_parts[3] = p_parts[3], p_parts[1]

        # Rejoin string
        passage = ''.join(p_parts)

        # Extract question prompts and responses to list of dicts

        # Note: we do this here so we can switch the order of the
        # critical question responses
        question_list = []
        for question in questions:
            pat = "CQ([123C]): (.+?\?) \[(.+?) ?/ ?(.+?) ?\]"
            match = re.match(pat, question)
            q_num, prompt, a, b = match.groups()

            # Switch order of responses for critical Q
            if q_num == "C" and order == "B":
                responses = [b, a]
            else:
                responses = [a, b]

            question_list.append(
                {"question_no": q_num,
                 "prompt": prompt,
                 "responses": responses,
                 "critical": 1 if q_num == "C" else 0}
            )

        version_list.append(
            {"sent_id": i+1,
             "order": order,
             "item_id": f"{i+1}_{order}",
             "passage": passage,
             "questions": question_list
             }
        )

    # Add both versions to master list
    stimuli_list.append(version_list)

with open("pipr2/data/stimuli.json", "w") as f:
    json.dump(stimuli_list, f, indent=4)
