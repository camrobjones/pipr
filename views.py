"""
views.py
--------
Retrieve item data and render as HTTP Responses

"""

import os
import random
import json

from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone as tz
import pandas as pd

"""
Constants
---------
"""

# General parameters
RESULTS_DIR = 'pronouns/data/results/'  # Store responses
FILLER_RATIO = 2  # Ratio of Fillers:Experimental Items

# CSV column names
ID_COLS = ["sent_id", "order", "item_id", "item_type"]
CONTENT_COLS = ["sent", "question", "NP1", "NP2"]
MODE_COLUMNS = {
    "expt": [f"expt_{col}" for col in CONTENT_COLS],
    "syntax_norm": [f"syntax_{col}" for col in CONTENT_COLS],
    "physics_norm": ["physics_sent", "physics_question",
                     "expt_NP1", "expt_NP2"],
}


"""
Load Data
---------
Helper functions to load and reformat data.
TODO: refactor and combine
"""


def get_stimuli(mode="expt", limit=None):
    """Loads stimuli csv and returns dict of data needed for mode

    Args:
        mode (str, optional): {"expt", "syntax_norm", "physics_norm"}
        limit (int, optional): Max number of experimental stimuli

    Returns:
        list of dict: Records-style data for jsPsych
    """

    # Load csv
    stimuli_df = pd.read_csv('pronouns/data/stimuli.csv')

    # Sample sent_ids
    sent_ids = set(stimuli_df.sent_id)
    if limit is not None and int(limit) < len(sent_ids):
        sent_ids = random.sample(sent_ids, k=int(limit))

    # Choose one order (A or B) for each sent_id
    orders = [random.choice(["A", "B"]) for i in range(len(sent_ids))]

    # Generate item_ids
    stimuli_ids = [f"{a}_{b}" for a, b in zip(sent_ids, orders)]

    # Get rows from df
    stimuli_df = stimuli_df[stimuli_df.item_id.isin(stimuli_ids)]

    # clean columns and na
    stimuli_df = stimuli_df[ID_COLS + MODE_COLUMNS[mode]].fillna("")
    stimuli_df.columns = ID_COLS + CONTENT_COLS

    # Randomize NP1/NP2 order
    stimuli_df['reversed'] = random.choices([True, False], k=len(stimuli_df))

    return stimuli_df.to_dict(orient='records')


def get_fillers(n_fillers):
    """Get filler items and return a dict of data

    Args:
        n_fillers (int): Number of fillers to return

    Returns:
        list of dict: Records-style data for jsPsych
    """

    # Load data
    filler_df = pd.read_csv('pronouns/data/fillers.csv')
    # TODO: filler_df.groupby('sent_id').sample(k=1)

    # Get sample of sent_ids
    unique_ids = set(filler_df.sent_id)
    n_fillers = min(n_fillers, len(unique_ids))
    sent_ids = random.sample(unique_ids, k=n_fillers)

    # Randomly select bias for each sent_id
    biases = random.choices(["NP1", "NP2"], k=len(sent_ids))
    filler_ids = [f"{a}_{b}" for a, b in zip(sent_ids, biases)]

    # Get data for ids
    filler_sample = filler_df[filler_df.item_id.isin(filler_ids)].fillna("")

    # Randomize NP1/NP2 order
    filler_sample['reversed'] = random.choices([True, False],
                                               k=len(filler_sample))

    return filler_sample.to_dict(orient='records')


def home(request):
    """Control panel for launching the experiment"""
    return render(request, 'pronouns/home.html')


def expt(request):
    """Return experiment view

    GET Args:
        n (int): Max no. experimental items
        mode (str): Key for experiment type
        fillers (bool): Flag. Include fillers?
    """

    # Parse GET data
    limit = request.GET.get('n')
    mode = request.GET.get('mode', 'expt')
    fillers = request.GET.get('fillers')

    # Get experimental items
    items = get_stimuli(mode=mode, limit=limit)

    # Get fillers if requested
    if fillers is not None and mode != "physics_norm":
        n_fillers = FILLER_RATIO * len(items)
        filler_data = get_fillers(n_fillers)
        items += filler_data

    # Create view context
    conf = {"mode": mode}
    context = {"items": items, "conf": conf}

    # Create new key for new expt attempt
    request.session.cycle_key()

    # Return view
    return render(request, 'pronouns/expt.html', context)


def save_results(request):
    """Save JSON of experiment results

    The POST is written to JSON as-is.
    """
    # Generate filename
    session_key = request.session.session_key
    timestamp = tz.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"{timestamp}-{session_key}.json"
    filepath = os.path.join(RESULTS_DIR, filename)

    # Check RESULTS_DIR exists
    if not os.path.isdir(RESULTS_DIR):
        os.mkdir(RESULTS_DIR)

    # Get posted data
    post = json.loads(request.body.decode('utf-8'))

    # Write file
    with open(filepath, 'w') as f:
        json.dump(post, f, indent=4)

    # Notify User
    return JsonResponse({"success": True})
