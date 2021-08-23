"""
Scripts to get surprisal for E1 stims
"""

import json
import re

import pandas as pd

from pipr3.lm import lm

"""
Parameters
----------
"""
MODULE_NAME = "pipr3"

"""
Load data
---------
"""


def get_region_probs(text, model_name):
    """Get surprisal for critical regions in text"""

    regions = list(re.finditer("#[^/]+/", text))  # Find all recorded groups

    probs = []

    for region in regions:
        seen = text[:region.start()]
        seen = re.sub('[/#\n]', '', seen)

        unseen = region.group()
        unseen = re.sub('[/#\n]', '', unseen)

        prob = lm.next_seq_prob(seen, unseen, model_name)
        probs.append(prob.item())

    return probs


def clean_lstm_text(text):
    """Clean text for lstm processing"""
    text = re.sub('[/#\n]', '', text)  # Remove special characters

    # h/t https://stackoverflow.com/a/3645946
    text = re.sub('([.,!?()\'"-])', r' \1 ', text)  # Pad punctuation
    text = re.sub('\s{2,}', ' ', text)  # Collapse multiple spaces

    return text


def generate_lstm_stim(text):
    """Generate stim format for lstm probabilities"""
    regions = list(re.finditer("#[^/]+/", text))  # Find all recorded groups

    # Var to store cleaned text
    cleaned_text = ""

    # Var to track end of last region
    last_idx = 0

    # This is where we store word counts for each region
    # We do this so we can combine probabilities for SPR regions later
    token_counts = []

    # loop through regions
    for region in regions:
        # clean context
        context = text[last_idx:region.start()]
        context = clean_lstm_text(context)
        cleaned_text += context

        # clean target region
        target = region.group()
        target = clean_lstm_text(target)

        # Token count for this region
        tokens = [t for t in target.split(" ") if t]
        token_counts.append(len(tokens))

        for token in tokens:
            cleaned_text += f"*{token}* "

        last_idx = region.end()

    return {"text": cleaned_text, "token_counts": token_counts}


# LM probabilities
def get_lm_probs(model_name):
    with open(MODULE_NAME + "/data/stimuli.json") as f:
        stimuli = json.load(f)

    spl_data = []
    region_names = [f"{s}_r{n}" for s in ["crit", "cont"] for n in range(1, 8)] 

    for ix, item in enumerate(stimuli):
        print(f"{ix}/{len(stimuli)}")
        for j, version in enumerate(item):
            print(f"\t{j}/{len(version)}")
            probs = get_region_probs(version["stimulus"], model_name)
            stim_data = {region_names[i]: probs[i] for i in range(len(probs))}
            stim_data["item_id"] = version["item_id"]

            spl_data.append(stim_data)

    spl_df = pd.DataFrame(spl_data)

    spl_df.to_csv(f"pipr3/data/surprisal_{model_name}.csv")


# LSTM stimuli
def generate_lstm_stims():
    with open(MODULE_NAME + "/data/stimuli.json") as f:
        stimuli = json.load(f)

    processed_stims = []
    token_counts = []

    region_names = [f"{s}_r{n}" for s in ["crit", "cont"] for n in range(1, 8)]

    for item in stimuli:
        for version in item:
            # Clean text for LSTM
            stim = generate_lstm_stim(version["stimulus"])
            processed_stims.append(stim["text"] + "\n")

            # Store token counts to combine token surprisals later
            t_c = stim["token_counts"]
            stim_data = {region_names[i]: t_c[i] for i in range(len(t_c))}
            stim_data["item_id"] = version["item_id"]
            token_counts.append(stim_data)

    # Write stimuli file
    with open(MODULE_NAME + "/data/stimuli_lstm.txt", "w") as out:
        out.writelines(processed_stims)

    tc_df = pd.DataFrame(token_counts)

    tc_df.to_csv(f"pipr3/data/token_counts.csv")



# It broke ... steel plate unharmed
# [tensor(-24.3314), tensor(-17.6134), tensor(-31.3971), tensor(-27.5524), tensor(-18.1449), tensor(-28.9194), tensor(-25.0143)]

# It broke ... steel plate unharmed
# [tensor(-24.3314), tensor(-17.6134), tensor(-30.4908), tensor(-27.7786), tensor(-18.2058), tensor(-28.8605), tensor(-24.9949)]

