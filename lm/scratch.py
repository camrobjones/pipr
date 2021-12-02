import json
import re

import pandas as pd

from pipr3.lm import lm

MODULE_NAME = "pipr3"

# Check items don't vary before critical

with open(MODULE_NAME + "/data/stimuli.json") as f:
    stimuli = json.load(f)

