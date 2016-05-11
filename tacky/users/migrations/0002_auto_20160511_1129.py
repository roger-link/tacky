# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-11 16:29
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('red', models.CommaSeparatedIntegerField(max_length=5)),
                ('black', models.CommaSeparatedIntegerField(max_length=5)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], verbose_name='username'),
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
