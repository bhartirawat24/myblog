# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0004_auto_20151103_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='contact',
            field=models.CharField(default=b'', unique=True, max_length=100, blank=True),
        ),
    ]
