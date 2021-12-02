
# Does world knowledge influence the propositional interpretation of language? Evidence from pronoun resolution

Code to run 3 Experiments investigating the influence of physical plausibility on language comprehension.

The code for each experiment is kept on separate branches (expt1, expt2, and expt3).

All experiments are run on a python/django backend and a js-psych driven frontend.

The directory organization follows django convention. HTML templates are found in 
`/templates/<appname>/`. JS files are in `static/<appname>/`. Python code to
load the data, serve the experiment page, and store results is in `views.py`
and the definition of the database schema is in `models.py`.

The language model code (for all 3 expts) is on the `expt3` branch in the `lm` directory.

The apps should be "plug-and-play" so you should be able to import them into
a different django project and run them. Let me know if you have any difficulty
finding/running/adapting anything! c8jones@ucsd.edu