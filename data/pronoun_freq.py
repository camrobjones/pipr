from nltk.corpus import switchboard as corpus

tw = corpus.tagged_words(tagset='universal')
tags = [t[1] for t in tw]
c = Counter(tags)
c['PRON'] / len(tags)
