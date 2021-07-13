"""
Transform raw text of stims into json
"""

import re
import json

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable

"""
Helper functions
"""


font = TTFont('pipr3/static/pipr3/fonts/Open_Sans/OpenSans-Regular.ttf')
cmap = font['cmap']
t = cmap.getcmap(3,1).cmap
s = font.getGlyphSet()
units_per_em = font['head'].unitsPerEm


def getTextWidth(text, pointSize):
    total = 0
    for c in text:
        if ord(c) in t and t[ord(c)] in s:
            total += s[t[ord(c)]].width
        else:
            total += s['.notdef'].width
    total = total*float(pointSize)/units_per_em
    return total


def insert_linebreaks(text, max_width=840, font_size=25,
                      group_pattern=" */ *"):
    """Return text with linebreaks (with max linewidth of max_width px)"""

    # Split into SPR groups
    groups = re.split(group_pattern, text)

    # Initialise variables
    new_text = ""
    current_line = ""
    line_width = 0

    # Cycle through SPR groups
    for group in groups:

        clean_group = re.sub("[\{\}#\/]", "", group) + " "

        group_width = getTextWidth(clean_group, font_size)

        # If line is not full, add group to line
        if (line_width + group_width) <= max_width:
            current_line += (group + " /")
            line_width += group_width

        # If line is full, add to text and clear line
        else:
            new_text += (current_line[:-1] + "\n" + "/")
            current_line = group + " /"
            line_width = group_width

    # Add any remaining text in current line
    if current_line:
        new_text += (current_line)

    # Remove final group boundary.
    new_text = new_text[:-1]

    return new_text


"""
"""

# data = json.load(open("pipr3/data/stimuli.json"))
# for i, item in enumerate(data):
#     lens = []
#     for version in item: 
#         lens.append(version["stimulus"].count("\n"))

#     print(i+1, lens)


def create_version(passage, sent_id, order, continuation, unambiguous):
    """Create a version of the stimulus"""

    # Extract NPs
    a, np1, b, np2, c, pronoun, d = re.split("[\{\}]", passage)

    # Extract continuations
    d_parts = re.split("\[|\]", d)
    cont1, cont2 = re.split("/", d_parts[1])

    # Order
    if order == "B":
        # Swap NP1 & NP2
        np1, np2 = np2, np1
        # Swap continuations (so they map to np1/2 order)
        cont1, cont2 = cont2, cont1

    # Continuation
    if continuation == "NP1":
        cont = cont1
    else:
        cont = cont2

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

    # NP1 capitalization
    if re.search("\. \/ *$", a):
        np1 = np1[0].title() + np1[1:]

    # Find longest continuation
    cont_long = cont1 if len(cont1) > len(cont2) else cont2
    cont_long = "{" + cont_long + "}"
    d = d_parts[0] + cont_long + d_parts[2]

    # Build passage
    passage = ''.join([a, np1, b, np2, c, longest, d])
    # Insert linebreaks
    passage = insert_linebreaks(passage)
    # Replace longest NP with actual pronoun
    passage = re.sub(longest, pronoun, passage)
    passage = re.sub(cont_long, cont, passage)

    """
    Create version data
    """

    am_str = "amb" if unambiguous == 0 else "un"

    version_data = {"sent_id": sent_id,
                    "order": order,
                    "item_type": "ACTIVE",
                    "continuation": continuation,
                    "unambiguous": unambiguous,
                    "item_id": f"{sent_id}_{order}_{continuation}_{am_str}",
                    "stimulus": passage,
                    "question": question,
                    "qanswer": answer
                    }

    return version_data


def create_lists(stimuli):
    """Create lists counterbalanced across conditions
    """
    # Get no of unique versions
    n_lists = len(stimuli[0])

    # Initialize list of lists
    lists = []

    for list_index in range(n_lists):

        # Initialize version index as list_index
        version_index = list_index
        current_list = []

        for item in stimuli:

            current_list.append(item[version_index])

            # Increment index by 1 mod n_lists
            version_index = (version_index + 1) % n_lists

        lists.append(current_list)

    return lists


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

# Save stim versions
with open("pipr3/data/stimuli.json", "w") as f:
    json.dump(stimuli_list, f, indent=4)


"""
Create and save lists
"""

# Ambiguous
stims_am = [
        [v for v in item if v['unambiguous'] == 0]
        for item in stimuli_list
]

lists_am = create_lists(stims_am)
with open("pipr3/data/stimuli_lists_AM.json", "w") as f:
    json.dump(lists_am, f, indent=4)

# Unambiguous
stims_un = [
        [v for v in item if v['unambiguous'] == 1]
        for item in stimuli_list
]

lists_un = create_lists(stims_un)
with open("pipr3/data/stimuli_lists_UN.json", "w") as f:
    json.dump(lists_un, f, indent=4)
