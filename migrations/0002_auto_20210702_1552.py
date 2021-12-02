# Generated by Django 3.1.1 on 2021-07-02 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipr3', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trial',
            name='condition',
        ),
        migrations.RemoveField(
            model_name='trial',
            name='key_press',
        ),
        migrations.RemoveField(
            model_name='trial',
            name='reaction_time',
        ),
        migrations.RemoveField(
            model_name='trial',
            name='response',
        ),
        migrations.RemoveField(
            model_name='trial',
            name='reversed_flag',
        ),
        migrations.AddField(
            model_name='trial',
            name='answer',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='trial',
            name='answer_rt',
            field=models.FloatField(default=-1),
        ),
        migrations.AddField(
            model_name='trial',
            name='expected_answer',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='trial',
            name='rt_cont',
            field=models.FloatField(default=-1),
        ),
        migrations.AddField(
            model_name='trial',
            name='rt_cont_p1',
            field=models.FloatField(default=-1),
        ),
        migrations.AddField(
            model_name='trial',
            name='rt_cont_p2',
            field=models.FloatField(default=-1),
        ),
        migrations.AddField(
            model_name='trial',
            name='rt_cont_p3',
            field=models.FloatField(default=-1),
        ),
        migrations.AddField(
            model_name='trial',
            name='rt_cont_sp1',
            field=models.FloatField(default=-1),
        ),
        migrations.AddField(
            model_name='trial',
            name='rt_crit',
            field=models.FloatField(default=-1),
        ),
        migrations.AddField(
            model_name='trial',
            name='rt_crit_p1',
            field=models.FloatField(default=-1),
        ),
        migrations.AddField(
            model_name='trial',
            name='rt_crit_p2',
            field=models.FloatField(default=-1),
        ),
        migrations.AddField(
            model_name='trial',
            name='rt_crit_p3',
            field=models.FloatField(default=-1),
        ),
        migrations.AddField(
            model_name='trial',
            name='rt_crit_sp1',
            field=models.FloatField(default=-1),
        ),
        migrations.AddField(
            model_name='trial',
            name='time_elapsed',
            field=models.FloatField(default=-1),
        ),
    ]