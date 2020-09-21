
# PIPR Experiment 1

Web interface for PIPR experiment using django/jsPsych.

Hosted at https://camrobjones.com/pronouns/.

## Overview

Stimuli and fillers are loaded from csvs in 'data/' and rendered as timeline variables in jsPsych. The The ratio of fillers to experimental items is parameterisable (currently 2:1). Fillers are 50% NP1-biased and 50% NP-2 biased, so the overall (syntax) NP1-biased:NP2-biased ratio is 1:2.

Stimuli and fillers are mixed and randomly ordered. Participants are presented with a sentence for 3s, then a question and two possible responses (NP1, NP2). The order of the responses is randomised.

User responses are sent back at the end of the experiment and saved as a JSON in 'data/results/{timestamp}-{session-key}.json'.

## Todo

### Stimuli

    - Create more stimuli
    - Improve lower quality stimuli
        - Some experimental stimuli don't work in the norming formats.

### DB

    - Create schema to store:
        - Stimuli
        - Particicpants
        - Participant Responses

## Updates

- Added CAPTCHA v3 protection
