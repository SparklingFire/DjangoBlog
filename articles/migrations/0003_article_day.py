# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-09-21 18:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_remove_subscription_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='day',
            field=models.DateField(default=datetime.date(2017, 9, 21), editable=False),
        ),
    ]