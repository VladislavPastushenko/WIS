# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


def assign_users(apps, schema_editor):
    User = apps.get_model('auth', 'user')
    Person = apps.get_model('main', 'Person')
    person1 = Person.objects.get(pk=1)
    person2 = Person.objects.get(pk=2)

    user1 = User.objects.get(username="xkravc")
    user2 = User.objects.get(username="xvojna")

    person1.user = user1
    person2.user = user2

    person1.save()
    person2.save()

    # Set user1 as superuser
    user1.is_superuser = True
    user1.is_staff = True
    user1.is_admin = True
    user1.save()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_create_users'),
    ]

    operations = [
        migrations.RunPython(assign_users)
    ]
