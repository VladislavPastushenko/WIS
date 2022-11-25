# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
from django.contrib.auth.models import User


def create_users(apps, schema_editor):
    user1 = User.objects.create_user(username="xkravc", password="123456", email=None)
    user2 = User.objects.create_user(username="xvojna", password="123456")

    user1.save()
    user2.save()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_users)
    ]
