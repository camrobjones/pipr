# Generated by Django 3.1.1 on 2020-09-24 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pronouns', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='captcha_score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]