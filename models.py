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
    condition = models.IntegerField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    # Demographics
    birth_year = models.IntegerField(blank=True, null=True)
    gender = models.CharField(blank=True, null=True, max_length=2)
    handedness = models.CharField(blank=True, null=True, max_length=10)

    # Feedback
    post_test_purpose = models.TextField(default="")
    post_test_correct = models.TextField(default="")
    post_test_rule = models.TextField(default="")
    post_test_pronoun = models.TextField(default="")
    post_test_syntax = models.TextField(default="")
    post_test_semantics = models.TextField(default="")
    post_test_other = models.TextField(default="")


class Stimulus(models.Model):
    """Experimental Stimulus data"""
    item_type = models.CharField(max_length=128)  # Filler, Catch, or Critical
    item_id = models.CharField(max_length=128)  # UID for item
    question_no = models.CharField(max_length=128)  # No. of Question


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
    reaction_time = models.FloatField()  # RT in ms
    key_press = models.IntegerField(blank=True, null=True)  # Response code
    response = models.TextField(blank=True, null=True)  # Decoded response
    condition = models.IntegerField(blank=True, null=True)  # Decoded response
    trial_index = models.IntegerField(blank=True, null=True)  # Index for ppt
    reversed_flag = models.BooleanField(default=False)  # L-R reversed


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
