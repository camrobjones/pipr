# Generated by Django 3.1.1 on 2020-12-01 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pronouns', '0014_participant_sona_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='notes',
            field=models.TextField(default=''),
        ),
    ]