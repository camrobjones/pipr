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

from pipr2.models import Participant, Trial, Stimulus, Language
from pipr2.data.words import wordlist

"""
Constants
---------
"""

MODULE_NAME = "pipr2"

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


def get_stimuli(limit=None):
    """Load stimuli json and return dict of stims"""
    with open(MODULE_NAME + "/data/stimuli.json") as f:
        data = json.load(f)

    out = []
    for pair in data:

        # Choose one of two orders
        item = random.choice(pair)

        # Randomize order of responses
        for question in item['questions']:
            question["reversed"] = random.random() > 0.5

        # Randomize order of questions
        random.shuffle(item['questions'])

        out.append(item)

    if limit is not None:
        out = random.choices(out, k=limit)

    return out


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

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', "")

    ppt = Participant.objects.create(
        key=key, ip_address=ip, condition=1)

    ppt.SONA_code = sona_code

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
    items = get_stimuli(limit=limit)

    # Add reading times
    # TODO: Move to json script
    for item in items:
        item['time'] = get_reading_time(item['passage'])

    # Create view context
    conf = {"key": ppt.key, "ppt_id": ppt.id}
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

    # Passage reading times

    # Get trials
    passages = [item for item in data if item.get('trial_part') == "preview"]

    for passage_data in passages:
        stimulus, created = Stimulus.objects.get_or_create(
            item_id=passage_data.get('item_id'),
            item_type="passage",
            question_no="passage"
        )
        trial = Trial.objects.create(
            participant=ppt,
            stimulus=stimulus,
            reaction_time=passage_data.get('rt'),
            trial_index=passage_data.get('trial_index'),
            condition=ppt.condition
        )
        trial.save()

    # Get trials
    trials = [item for item in data if item.get('trial_part') == "trial"]

    for trial_data in trials:
        stimulus, created = Stimulus.objects.get_or_create(
            item_id=trial_data.get('item_id'),
            item_type=trial_data.get('item_type'),
            question_no=trial_data.get('question_no')
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
        data['question_no'] = trial.stimulus.question_no
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
