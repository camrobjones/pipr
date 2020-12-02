"""
views.py
--------
Retrieve item data and render as HTTP Responses

"""

import os
import random
import json
import re

import requests
import pandas as pd
from nltk import corpus
import syllables
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils import timezone as tz
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

from pronouns.models import Participant, Trial, Stimulus, Language
from pronouns.data.words import wordlist

"""
Constants
---------
"""

# General parameters
RESULTS_DIR = 'pronouns/data/results/'  # Store responses
FILLER_RATIO = 2  # Ratio of Fillers:Experimental Items

# Conditions
CONDITIONS = ["expt", "syntax_norm", "physics_norm"]
COND_2_INDEX = {"expt": 0,
                "e": 0,
                "syntax_norm": 1,
                "s": 1,
                "physics_norm": 2,
                "p": 2}
CONDITION = 1

# CSV column names
ID_COLS = ["sent_id", "order", "item_id", "item_type"]
CONTENT_COLS = ["sent", "question", "NP1", "NP2"]
MODE_COLUMNS = {
    "expt": [f"expt_{col}" for col in CONTENT_COLS],
    "syntax_norm": [f"syntax_{col}" for col in CONTENT_COLS],
    "physics_norm": ["physics_sent", "physics_question",
                     "expt_NP1", "expt_NP2"],
}

RECAPTCHA_URL = "https://www.google.com/recaptcha/api/siteverify"

LANGUAGE_REGEX = "language_([0-9])+"

random.seed()

CMUDICT = corpus.cmudict.dict()

SYLL_MS = 191  # Source: https://doi.org/10.1167/iovs.11-8284
READING_TIME_BASE = 250  # Thinking time buffer


"""
Helper functions
----------------
"""


def generate_key():
    """Generate ppt key"""
    return random.choice(wordlist)


def no_syllables(word):
    """Get no syllables in word"""
    pronunciations = CMUDICT.get(word)
    if pronunciations is not None:
        sylls = [len(list(y for y in x if y[-1].isdigit())) for x in pronunciations]
        return max(sylls)

    return syllables.estimate(word)


def get_reading_time(text, syll_ms=SYLL_MS):
    """Get reading time for text in ms, based on const * syllables"""
    words = re.findall("[a-z]+", text.lower())

    sylls = sum(no_syllables(word) for word in words)

    reading_time = READING_TIME_BASE + sylls * SYLL_MS

    return reading_time


"""
Load Data
---------
Helper functions to load and reformat data.
"""

# TODO: refactor and combine


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


def get_catch(condition):
    """Get catch trials"""
    catch_df = pd.read_csv('pronouns/data/catch.csv')

    if condition == "physics_norm":
        trial_type = "physics"
    else:
        trial_type = "experimental"

    catch_trials = catch_df[catch_df.trial_type == trial_type].fillna("")

    return catch_trials.to_dict(orient="records")


def ua_data(request):
    """Store ppt ua_data"""
    post = json.loads(request.body.decode('utf-8'))

    # print(post)

    ppt_id = post['ppt_id']

    ppt = Participant.objects.get(pk=ppt_id)
    ppt.ua_header = post.get('ua_header', "")
    ppt.screen_width = post.get('width', "")
    ppt.screen_height = post.get('height', "")
    ppt.workerId = post.get('workerId', "")
    ppt.save()

    return JsonResponse({"success": True})


def cycle_condition(cond):
    """Cycle through conditions"""
    if cond < 2:
        return cond + 1
    return 0


def get_condition():
    """Generate condition"""

    # Filter out ppts who exited early
    ppts = Participant.objects.exclude(ua_header="")

    # Filter out ppts who did not finish within 60 mins
    hour_ago = tz.now() - tz.timedelta(seconds=36000)
    ppts = ppts.exclude(
        Q(start_time__lte=hour_ago) & Q(end_time__isnull=True))

    # Select most recent qualifying ppt
    last = ppts.last()

    if last is not None:
        return cycle_condition(last.condition)
    return 0


def init_ppt(request):
    """Create new ppt"""

    # Get params
    mode = request.GET.get('mode')
    sona_code = request.GET.get('code', "")

    # Create key
    key = generate_key()

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', "")

    # condition
    if mode is not None:
        condition = COND_2_INDEX[mode]
    elif CONDITION is not None:
        condition = CONDITION
    else:
        condition = get_condition()

    ppt = Participant.objects.create(
        key=key, ip_address=ip, condition=condition)

    ppt.SONA_code = sona_code

    return ppt


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
    fillers = request.GET.get('fillers', True)
    catch = request.GET.get('catch', True)

    # Create ppt
    ppt = init_ppt(request)
    mode = CONDITIONS[ppt.condition]

    # Get experimental items
    items = get_stimuli(mode=mode, limit=limit)

    # Get experimental items
    if catch != "false":
        items += get_catch(condition=mode)

    # Get fillers if requested
    if fillers != "false" and mode != "physics_norm":
        n_fillers = 45  # FILLER_RATIO * len(items)
        filler_data = get_fillers(n_fillers)
        items += filler_data

    # Add reading times
    for item in items:
        item['time'] = get_reading_time(item['sent'])

    # Create view context
    conf = {"mode": mode, "key": ppt.key, "ppt_id": ppt.id}
    context = {"items": items, "conf": conf}

    # Create new key for new expt attempt
    request.session.cycle_key()

    # Store session key
    ppt.session_key = request.session.session_key

    ppt.save()

    # Return view
    return render(request, 'pronouns/expt.html', context)


def error(request):
    """Control panel for launching the experiment"""
    return render(request, 'pronouns/error.html')


"""
API Views
"""


def save_results(request):
    """Save JSON of experiment results

    The POST is written to JSON as-is.
    """

    # Get posted data
    session_key = request.session.session_key
    post = json.loads(request.body.decode('utf-8'))
    ppt_id = post.get('ppt_id', session_key)

    # Generate filename
    timestamp = tz.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"{timestamp}-{ppt_id}.json"
    filepath = os.path.join(RESULTS_DIR, filename)

    # Check RESULTS_DIR exists
    if not os.path.isdir(RESULTS_DIR):
        os.mkdir(RESULTS_DIR)

    # Write file
    with open(filepath, 'w') as f:
        json.dump(post, f, indent=4)

    # Retreieve ppt
    ppt = Participant.objects.get(pk=ppt_id)

    # store results
    data = post['results']

    # Get trials
    trials = [item for item in data if item.get('trial_part') == "trial"]

    for trial_data in trials:
        stimulus, created = Stimulus.objects.get_or_create(
            item_id=trial_data.get('item_id'),
            item_type=trial_data.get('item_type'),
            stimulus=trial_data.get('stimulus')
        )
        trial = Trial.objects.create(
            participant=ppt,
            stimulus=stimulus,
            reaction_time=trial_data.get('rt'),
            key_press=trial_data.get('key_press'),
            response=trial_data.get('response'),
            trial_index=trial_data.get('trial_index'),
            reversed_flag=trial_data.get('reversed', False),
            condition=ppt.condition
        )
        trial.save()

    demo = [item for item in data if item.get('trial_part') == "demographics"]

    demo = demo[0]
    demo_data = json.loads(demo.get('responses', "{}"))
    ppt.birth_year = demo_data.get('demographics_year') or None
    ppt.gender = demo_data.get('demographics_gender')
    ppt.handedness = demo_data.get('demographics_handedness')

    # Get matches
    lang_matches = [re.match(LANGUAGE_REGEX, l) for l in demo_data]
    lang_indexes = [l.groups()[0] for l in lang_matches if l]

    for idx in lang_indexes:
        language = Language.objects.create(
            participant=ppt,
            index=int(idx),
            language=demo_data.get(f"language_{idx}", ""),
            proficiency=demo_data.get(f"language_proficiency_{idx}", ""),
            learned=demo_data.get(f"language_learned_{idx}", ""),
            active=demo_data.get(f"language_active_{idx}", ""),
            proportion=demo_data.get(f"language_proportion_{idx}", "")
        )

    # Store feedback
    feedback = filter(lambda x: x.get('trial_part') == "post_test", data)

    for feedback_item in feedback:
        feedback_data = json.loads(feedback_item.get('responses', "{}"))
        for name, response in feedback_data.items():
            setattr(ppt, name, response)

    ppt.end_time = tz.now()

    # Grant credit
    if ppt.SONA_code != "":
        response = requests.get(
            f"https://ucsd.sona-systems.com/services/SonaAPI.svc/WebstudyCredit?experiment_id=1973&credit_token=0f5cafc5a8494590ab491efffc8ab35f&survey_code={ppt.SONA_code}")
        content = response.content.decode()
        ppt.notes = ppt.notes + f"SONA credit response:\n{content}\n"

    ppt.save()

    # Notify User
    return JsonResponse({"success": True})


def validate_captcha(request):
    """Validate captcha token"""

    post = json.loads(request.body.decode('utf-8'))

    ppt_id = post['ppt_id']
    token = post.get('token')

    # print(token)

    data = {"response": token,
            "secret": settings.CAPTCHA_SECRET_KEY}

    # print(data)

    response = requests.post(RECAPTCHA_URL, data=data)

    # print(response)
    content = response.content
    # print(response.content)

    response_data = json.loads(content)
    # print(response_data)

    score = response_data.get('score')
    ppt = Participant.objects.get(pk=ppt_id)
    ppt.captcha_score = score
    ppt.save()

    return JsonResponse(response_data)


def is_admin(user):
    return user.is_superuser


def trial_data():
    """Get data on all trials"""
    data_list = []

    for trial in Trial.objects.all():

        data = trial.__dict__
        data['item_id'] = trial.stimulus.item_id
        data['item_type'] = trial.stimulus.item_type
        data.pop('_state')

        data_list.append(data)

    df = pd.DataFrame(data_list)
    df = df.sort_values('id').reset_index(drop=True)
    return df


def ppt_data():
    """Get data on all participants"""
    data_list = []

    for ppt in Participant.objects.all():

        data = ppt.__dict__
        data.pop('_state')

        data_list.append(data)

    df = pd.DataFrame(data_list)
    df = df.sort_values('id').reset_index(drop=True)
    return df


@user_passes_test(is_admin)
def download_data(request, model):
    """Download csv of model data"""
    if model == "trial":
        data = trial_data()
    elif model == "participant":
        data = ppt_data()
    else:
        raise ValueError(
            "'model' must be 'trial' or 'participant', not %r" % model)

    fname = f'pipr_{model}_{tz.now():%Y-%m-%d-%H-%M-%S}.csv'

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{fname}"'

    data.to_csv(response, index=False)

    return response
