# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-12 14:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20160511_2022'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coordinate',
            old_name='coordinate',
            new_name='position',
        ),
    ]
