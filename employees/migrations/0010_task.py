# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-17 07:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0009_auto_20190708_1237'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_dt', models.DateTimeField(blank=True, null=True)),
                ('end_dt', models.DateTimeField(blank=True, null=True)),
                ('task_name', models.CharField(blank=True, max_length=255, null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employees.Projects')),
                ('task_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employees.Employee')),
            ],
        ),
    ]
