# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-11 23:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.Question'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='down_votes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='answer',
            name='up_votes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='down_votes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='up_votes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
