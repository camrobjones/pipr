import json

from pronouns.models import Participant, Trial

fname = "pronouns/data/results/2020-09-13-17-05-50-yiaymn3vqccu7prdy9w3hoypa50ayy2j.json"

ppt = Participant.objects.get(key="police")


with open(fname) as f:
    post = json.load(f)

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