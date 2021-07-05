"""
Transform raw text of stims into json
"""

import re
import json

"""
Helper functions
"""


def insert_linebreaks(text, max_chars=72, group_pattern=" */ *"):
    """Return text with linebreaks (with max linewidth of max_chars)"""

    # Split into SPR groups
    groups = re.split(group_pattern, text)

    # Initialise variables
    new_text = ""
    current_line = ""

    # Cycle through SPR groups
    for group in groups:

        # If line is not full, add group to line
        if len(current_line + (group + " /")) <= max_chars:
            current_line += (group + " /")

        # If line is full, add to text and clear line
        else:
            new_text += (current_line[:-1] + "\n" + "/")
            current_line = group + " /"

    # Add any remaining text in current line
    if current_line:
        new_text += (current_line)

    # Remove final group boundary.
    new_text = new_text[:-1]

    return new_text


def create_version(passage, sent_id, order, continuation, unambiguous):
    """Create a version of the stimulus"""

    # Extract NPs
    a, np1, b, np2, c, pronoun, d = re.split("[\{\}]", passage)

    # Extract continuations
    d_parts = re.split("\[|\]", d)
    continuations = re.split("/", d_parts[1])

    # Order
    if order == "B":
        # Swap NP1 & NP2
        np1, np2 = np2, np1
        # Swap continuations (so they map to np1/2 order)
        continuations = [continuations[1], continuations[0]]

    # NP1 capitalization
    if re.search("\. \/ *$", a):
        np1 = np1[0].title() + np1[1:]

    # Continuation
    if continuation == "NP1":
        d = d_parts[0] + continuations[0] + d_parts[2]
    else:
        d = d_parts[0] + continuations[1] + d_parts[2]

    # Unambiguous
    if unambiguous == 1:
        if continuation == "NP1":
            pronoun = np2
        else:
            pronoun = np1

    """
    Ensure linebreaks consistent across conditions
    """

    # Find longest np
    longest = np1 if len(np1) > len(np2) else np2
    longest = "{" + longest + "}"
    # Build passage
    passage = ''.join([a, np1, b, np2, c, longest, d])
    # Insert linebreaks
    passage = insert_linebreaks(passage)
    # Replace longest NP with actual pronoun
    passage = re.sub(longest, pronoun, passage)

    """
    Create version data
    """

    am_str = "amb" if unambiguous == 0 else "un"

    version_data = {"sent_id": sent_id,
                    "order": order,
                    "continuation": continuation,
                    "unambiguous": unambiguous,
                    "item_id": f"{i+1}_{order}_{continuation}_{am_str}",
                    "passage": passage,
                    "question": question,
                    "qanswer": answer
                    }

    return version_data


with open("pipr3/data/stims_raw.txt") as f:
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
    passage, question_text = re.split(r"\s+Questions:\s+", sec)

    """
    Format questions
    """

    # Remove next question title
    question_text = re.sub(r"\s+[0-9]+\. .*", "", question_text)

    # Split into questions
    _, question, answer = re.split("[QA]:", question_text)

    question = question.strip()
    answer = answer.strip()

    """
    Format passage
    """

    # Remove subsection markers
    passage_pattern = "\n(Setup|Critical|Critical Spillover|"
    passage_pattern += "Continuation|Continuation Spillover):"
    passage = re.sub(passage_pattern, "", passage)

    # Loop through parameter combinations
    for order in ("A", "B"):
        for continuation in ("NP1", "NP2"):
            for unambiguous in (0, 1):
                # Create and store versions
                version = create_version(passage=passage,
                                         sent_id=i+1,
                                         order=order,
                                         continuation=continuation,
                                         unambiguous=unambiguous)
                version_list.append(version)

    # Add both versions to master list
    stimuli_list.append(version_list)

with open("pipr3/data/stimuli.json", "w") as f:
    json.dump(stimuli_list, f, indent=4)
