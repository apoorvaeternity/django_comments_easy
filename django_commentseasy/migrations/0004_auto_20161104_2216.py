# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-04 16:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_commentseasy', '0003_auto_20161104_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentseasy',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
