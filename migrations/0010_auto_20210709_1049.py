# Generated by Django 3.1.1 on 2021-07-09 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipr3', '0009_auto_20210709_1035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='conditions',
        ),
        migrations.AddField(
            model_name='participant',
            name='adhd',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='asd',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='dyslexia',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
