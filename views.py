"""
views.py
--------
Retrieve item data and render as HTTP Responses

"""

import os
import random
import json
import re
import math

import requests
import pandas as pd
from nltk import corpus
import syllables
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils import timezone as tz
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

from pipr3.models import Participant, Trial, Stimulus, Language, Likert
from pipr3.data.words import wordlist

"""
Constants
---------
"""

MODULE_NAME = "pipr3"

# General parameters
RESULTS_DIR = MODULE_NAME + '/data/results/'  # Store responses
FILLER_RATIO = 2  # Ratio of Fillers:Experimental Items

RECAPTCHA_URL = "https://www.google.com/recaptcha/api/siteverify"

LANGUAGE_REGEX = "language_([0-9])+"

random.seed()

CMUDICT = corpus.cmudict.dict()

SYLL_MS = 191  # Source: https://doi.org/10.1167/iovs.11-8284

SYLL_MS = 30  # Source: https://doi.org/10.1167/iovs.11-8284
READING_TIME_BASE = 250  # Thinking time buffer

NO_LISTS = 4

# What % of passages have comp questions
QUESTION_PROP = 1/3


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


def get_list_idx(condition):
    """Generate list index for new participant"""

    # Get most recent ppt
    last_ppt = Participant.objects.filter(condition=condition).last()

    # Increment last list idx if it exists
    if last_ppt:
        last_idx = last_ppt.list_idx

        return (last_idx + 1) % NO_LISTS

    return 0


"""
Load Data
---------
Helper functions to load and reformat data.
"""


def get_stimuli(limit=None, cond=None):
    """Load stimuli json and return dict of stims"""
    with open(MODULE_NAME + "/data/stimuli.json") as f:
        data = json.load(f)

    out = []
    for versions in data:

        # Choose one of two orders
        item = random.choice(versions)

        # Randomly present questions
        if random.random() > QUESTION_PROP:
            item["question"] = ""
            item["qanswer"] = ""

        out.append(item)

    # Shuffle & limit
    limit = limit or len(out)
    out = random.sample(out, k=limit)

    return out


def get_stimuli_by_list(list_idx, condition, limit=None):
    """Get a specific list of stimuli for the ppt"""
    with open(MODULE_NAME + f"/data/stimuli_lists_{condition}.json") as f:
        data = json.load(f)

    # Select one list
    stimuli = data[list_idx]

    # Get idx of stimuli to remove questions from
    n_no_q = math.floor((1-QUESTION_PROP) * len(stimuli))
    no_q_idx = random.sample(range(len(stimuli)), k=n_no_q)

    # Remove question from sampled items
    for idx in no_q_idx:
        item = stimuli[idx]
        item["question"] = ""
        item["qanswer"] = ""

    # Shuffle & limit
    limit = limit or len(stimuli)
    stimuli = random.sample(stimuli, k=limit)

    return stimuli


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


def init_ppt(request):
    """Create new ppt"""

    # Get params
    sona_code = request.GET.get('code', "")

    # Create key
    key = generate_key()

    # Get condition
    condition = request.GET.get('condition')

    # Randomly assign condition
    if condition is None:
        condition = random.choice(["AM", "UN"])

    # Get list index
    list_idx = get_list_idx(condition=condition)

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', "")

    ppt = Participant.objects.create(
        key=key, ip_address=ip, list_idx=list_idx, condition=condition)

    ppt.SONA_code = sona_code
    ppt.get_args = str(request.GET.dict())

    return ppt


def home(request):
    """Control panel for launching the experiment"""
    return render(request, MODULE_NAME + '/home.html')


def expt(request):
    """Return experiment view

    GET Args:
        n (int): Max no. experimental items
        mode (str): Key for experiment type
        fillers (bool): Flag. Include fillers?
    """

    # Parse GET data
    limit = request.GET.get('n') or None
    limit = int(limit) if limit else None

    # Create ppt
    ppt = init_ppt(request)

    # Get experimental items
    items = get_stimuli_by_list(list_idx=ppt.list_idx, limit=limit,
                                condition=ppt.condition)

    # Create view context
    conf = {"key": ppt.key, "ppt_id": ppt.id, "condition": ppt.condition}
    context = {"items": items, "conf": conf}

    # Create new key for new expt attempt
    request.session.cycle_key()

    # Store session key
    ppt.session_key = request.session.session_key

    ppt.save()

    # Return view
    return render(request, MODULE_NAME + '/expt.html', context)


def error(request):
    """Control panel for launching the experiment"""
    return render(request, MODULE_NAME + '/error.html')


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
    trials = [t for t in data if t.get("trial_part") == "trial"]

    # Group trial data by trial
    fixation_indices = [idx for idx, el in enumerate(trials)
                        if el["item_type"] == "FIX_CROSS"]
    slice_ends = fixation_indices[1:] + [len(trials)]
    trials = [trials[fixation_indices[i]:slice_ends[i]]
              for i in range(len(fixation_indices))]

    for trial in trials:
        
        # Split trial data into parts
        if len(trial) == 3:
            fixation, passage, question = trial
        else:
            # No question data
            fixation, passage = trial
            question = {}

        # Passage reading time
        pass_te = passage.get("time_elapsed")
        fix_te = fixation.get("time_elapsed")
        reading_time = pass_te - fix_te

        stimulus, created = Stimulus.objects.get_or_create(
            item_id=passage.get('item_id'),
            item_type="passage",
            sent_id=passage.get("sent_id"),
            continuation=passage.get('continuation'),
            order=passage.get('order'),
            unambiguous=passage.get('unambiguous')
        )

        trial = Trial.objects.create(
            participant=ppt,
            stimulus=stimulus,
            trial_index=fixation.get('trial_index'),

            # SPR times
            rt_crit_p3=passage.get("rt1"),
            rt_crit_p2=passage.get("rt2"),
            rt_crit_p1=passage.get("rt3"),
            rt_crit=passage.get("rt4"),
            rt_crit_sp1=passage.get("rt5"),
            rt_crit_sp2=passage.get("rt6"),
            rt_crit_sp3=passage.get("rt7"),

            # Continuation region times (ms)
            rt_cont_p3=passage.get("rt8"),
            rt_cont_p2=passage.get("rt9"),
            rt_cont_p1=passage.get("rt10"),
            rt_cont=passage.get("rt11"),
            rt_cont_sp1=passage.get("rt12"),
            rt_cont_sp2=passage.get("rt13"),
            rt_cont_sp3=passage.get("rt14"),

            # Whole reading time (ms)
            passage_reading_time=reading_time,

            # Comprehension Question
            answer=question.get("answer", ""),
            expected_answer=question.get("expected_answer", ""),
            answer_rt=question.get("rt", -1)
        )
        trial.save()

    # -- Demographics -- #

    # Get demo trial
    demo = [item for item in data if item.get('trial_part') == "demographics"]
    demo = demo[0]  # only one demo trial

    # Extract data to ppt obj
    demo_data = json.loads(demo.get('responses', "{}"))
    ppt.birth_year = demo_data.get('demographics_year') or None
    ppt.gender = demo_data.get('demographics_gender')
    ppt.handedness = demo_data.get('demographics_handedness')
    ppt.dyslexia = demo_data.get('dyslexia') == "true"
    ppt.adhd = demo_data.get('adhd') == "true"
    ppt.asd = demo_data.get('asd') == "true"
    ppt.vision = demo_data.get('demographics_vision')
    ppt.vision_reason = demo_data.get('demographics_vision_reason')
    ppt.native_english = demo_data.get('demographics_english') == "yes"

    # -- VVIQ -- #

    # Get relevant items
    vviq_items = [item for item in data if item.get('trial_part') == "vviq"]

    for vviq_item in vviq_items:

        # Get response data
        vviq_data = json.loads(vviq_item.get('responses', "{}"))
        
        # Pass empty trials (e.g. instructions)
        if not vviq_data:
            continue

        for key, value in vviq_data.items():

            # Get item_id
            match = re.match("vviq-response-([0-9+]-[0-9+])", key)
            item_id = match.groups()[0]

            # Convert response to int
            response = int(value)

            likert_response = Likert.objects.create(
                participant=ppt,
                scale="VVIQ",
                item_id=item_id,
                response=response
                )

    # -- Languages -- #

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
            f"https://ucsd.sona-systems.com/services/SonaAPI.svc/WebstudyCredit?experiment_id=2151&credit_token=5edbe67c06d3444abf48aa43985c572b&survey_code={ppt.SONA_code}")
        content = response.content.decode()
        ppt.notes = ppt.notes + f"SONA credit response:\n{content}\n"

    ppt.save()

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
        data['sent_id'] = trial.stimulus.sent_id
        data['continuation'] = trial.stimulus.continuation
        data['order'] = trial.stimulus.order
        data['unambiguous'] = trial.stimulus.unambiguous
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


def lang_data():
    """Get language data"""
    data_list = []

    for language in Language.objects.all():

        data = language.__dict__
        data.pop('_state')

        data_list.append(data)

    df = pd.DataFrame(data_list)
    df = df.sort_values('id').reset_index(drop=True)
    return df


def likert_data():
    """Get likert response data"""
    data_list = []

    for response in Likert.objects.all():

        data = response.__dict__
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
    elif model == "language":
        data = lang_data()
    elif model == "likert":
        data = likert_data()
    else:
        raise ValueError(
            "'model' must be 'trial' or 'participant', not %r" % model)

    fname = f'pipr_{model}_{tz.now():%Y-%m-%d-%H-%M-%S}.csv'

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{fname}"'

    data.to_csv(response, index=False)

    return response
