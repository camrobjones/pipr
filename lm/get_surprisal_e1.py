"""
Scripts to get surprisal for E1 stims
"""

import pandas as pd

from pipr3.lm.lm import mask_probability_df

# Stimuli
stimuli = pd.read_csv("stims.csv")

stimuli = mask_probability_df(stimuli)

stimuli.to_csv("expt_prob.csv")

# Physics norming
phys = pd.read_csv("physics.csv")

phys = mask_probability_df(phys)

phys.to_csv("phys_prob.csv")

# Fillers
fillers = pd.read_csv("fillers.csv")

fillers = mask_probability_df(fillers)

fillers.to_csv("fillers_prob.csv")