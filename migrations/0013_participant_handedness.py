# Generated by Django 3.1.1 on 2020-11-18 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pronouns', '0012_participant_get_args'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='handedness',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
