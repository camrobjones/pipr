
# PIPR Experiment 3

Web interface for PIPR experiment using django/jsPsych.

Hosted at https://camrobjones.com/pipr3/expt.

## Overview

Participants read passages which contain a) a critical sentence with an
ambiguous pronoun and b) a continuation sentence which is inconsistent
with one interpretation of the pronoun.

Self-paced reading is used to measure the reading speed of the continuation
sentence to check whether it is sensitive to the plausibility of the
pronoun interpretation which it contradicts. The self-paced reading
code is adapted from https://github.com/UiL-OTS-labs/jspsych-uil-template-docs.

`lm/` contains code for getting surprisal for each item (for E1/2 and E3 stimuli).