
from pipr2.views import get_stimuli

from collections import Counter

c = Counter()


for n in range(40):
    stims = get_stimuli()

    c.update([i['item_id'] for i in stims])