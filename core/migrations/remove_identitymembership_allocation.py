# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-31 20:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', 'create_access_token_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='identitymembership',
            name='allocation',
        ),
    ]