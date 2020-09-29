# Generated by Django 3.1.1 on 2020-09-24 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.TextField()),
                ('key', models.TextField()),
                ('ua_header', models.TextField(default='')),
                ('screen_width', models.TextField(default='')),
                ('screen_height', models.TextField(default='')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('condition', models.IntegerField(blank=True, null=True)),
                ('birth_year', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stimulus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(max_length=128)),
                ('item_id', models.CharField(max_length=128)),
                ('stimulus', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Trial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction_time', models.FloatField()),
                ('key_press', models.IntegerField(blank=True, null=True)),
                ('response', models.TextField(blank=True, null=True)),
                ('condition', models.IntegerField(blank=True, null=True)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='pronouns.participant')),
                ('stimulus', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='pronouns.stimulus')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(default=0)),
                ('language', models.TextField(default='')),
                ('proficiency', models.TextField(default='')),
                ('learned', models.TextField(default='')),
                ('active', models.TextField(default='')),
                ('proportion', models.TextField(default='')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pronouns.participant')),
            ],
        ),
    ]
