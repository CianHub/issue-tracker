# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-12 14:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0010_auto_20180710_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.IntegerField(choices=[(1, 'Incomplete'), (2, 'In Progress'), (3, 'Complete')], default=1),
        ),
    ]