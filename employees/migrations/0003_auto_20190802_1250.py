# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-08-02 07:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_auto_20190729_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worker',
            name='user',
        ),
        migrations.DeleteModel(
            name='Worker',
        ),
    ]
