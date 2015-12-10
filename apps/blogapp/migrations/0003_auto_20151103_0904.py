# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_auto_20151103_0903'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogtable',
            old_name='Category',
            new_name='category',
        ),
    ]
