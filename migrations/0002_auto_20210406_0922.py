# Generated by Django 3.1.1 on 2021-04-06 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipr2', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stimulus',
            name='stimulus',
        ),
        migrations.AddField(
            model_name='stimulus',
            name='question_no',
            field=models.CharField(default=4, max_length=128),
            preserve_default=False,
        ),
    ]