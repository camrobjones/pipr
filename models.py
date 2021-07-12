"""
Database storage for ppts and trials
"""

from django.db import models

# Create your models here.


class Participant(models.Model):
    """Class to store participant data"""

    ip_address = models.TextField()
    key = models.TextField()  # Generated hex key to track ppt
    session_key = models.TextField()  # Check for multiple sessions
    workerId = models.TextField(default="")  # Amazon Mechanical Turk Worker Id
    SONA_code = models.TextField(default="")  # SONA participant code
    get_args = models.TextField(default="")  # Get args issued with request
    notes = models.TextField(default="")  # Get args issued with request

    # Device
    ua_header = models.TextField(default="")
    screen_width = models.TextField(default="")
    screen_height = models.TextField(default="")

    # Validation
    captcha_score = models.FloatField(blank=True, null=True)

    # Experiment
    start_time = models.DateTimeField(auto_now_add=True)
    list_idx = models.IntegerField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    # Conditions
    UNAMBIGUOUS = "UN"
    AMBIGUOUS = "AM"
    UNASSIGNED = "NA"
    CONDITIONS = [
        (UNAMBIGUOUS, "Unambiguous"),
        (AMBIGUOUS, "Ambiguous"),
        (UNASSIGNED, "Unassigned")
    ]
    condition = models.CharField(
        max_length=2,
        choices=CONDITIONS,
        default=UNASSIGNED
    )

    # Demographics
    birth_year = models.IntegerField(blank=True, null=True)
    gender = models.CharField(blank=True, null=True, max_length=2)
    handedness = models.CharField(blank=True, null=True, max_length=10)
    dyslexia = models.BooleanField(blank=True, null=True)
    adhd = models.BooleanField(blank=True, null=True)
    asd = models.BooleanField(blank=True, null=True)
    vision = models.CharField(blank=True, null=True, max_length=10)

    # Feedback
    post_test_purpose = models.TextField(default="")
    post_test_inconsistent = models.TextField(default="")
    post_test_pronoun = models.TextField(default="")
    post_test_example = models.TextField(default="")
    post_test_other = models.TextField(default="")


class Stimulus(models.Model):
    """Experimental Stimulus data"""
    item_type = models.CharField(max_length=128)  # Filler, Catch, or Critical
    item_id = models.CharField(max_length=128)  # UID for item
    
    sent_id = models.IntegerField()
    continuation = models.CharField(max_length=10)  # NP1 or NP2
    order = models.CharField(max_length=10)  # A or B
    unambiguous = models.IntegerField()  # 0 or 1


class Trial(models.Model):
    """Store response and RT for each trial"""
    participant = models.ForeignKey(
        Participant,
        on_delete=models.RESTRICT
    )
    stimulus = models.ForeignKey(
        Stimulus,
        on_delete=models.RESTRICT
    )

    # Critical region times (ms)
    rt_crit_p3 = models.FloatField(default=-1)
    rt_crit_p2 = models.FloatField(default=-1)
    rt_crit_p1 = models.FloatField(default=-1)
    rt_crit = models.FloatField(default=-1)
    rt_crit_sp1 = models.FloatField(default=-1)
    rt_crit_sp2 = models.FloatField(default=-1)
    rt_crit_sp3 = models.FloatField(default=-1)

    # Continuation region times (ms)
    rt_cont_p3 = models.FloatField(default=-1)
    rt_cont_p2 = models.FloatField(default=-1)
    rt_cont_p1 = models.FloatField(default=-1)
    rt_cont = models.FloatField(default=-1)
    rt_cont_sp1 = models.FloatField(default=-1)
    rt_cont_sp2 = models.FloatField(default=-1)
    rt_cont_sp3 = models.FloatField(default=-1)

    # Whole reading time (ms)
    passage_reading_time = models.FloatField(default=-1)

    # Comprehension Question
    answer = models.CharField(max_length=10, default="")
    expected_answer = models.CharField(max_length=10, default="")
    answer_rt = models.FloatField(default=-1)

    # Index for ppt
    trial_index = models.IntegerField(blank=True, null=True)


class Language(models.Model):
    """Stores data on each language the participant knows"""
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE
    )
    index = models.IntegerField(default=0)  # Input order index
    language = models.TextField(default="")  # Name of language
    proficiency = models.TextField(default="")  # Level of proficiency
    learned = models.TextField(default="")  # Age first learned
    active = models.TextField(default="")  # No. years used
    proportion = models.TextField(default="")  # % of time used currently
