# Generated by Django 3.1.1 on 2020-09-24 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pronouns', '0002_participant_captcha_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='session_key',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
