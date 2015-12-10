# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0003_auto_20151103_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogtable',
            name='status',
            field=models.SmallIntegerField(choices=[(0, b'Inactive'), (1, b'active'), (2, b'Delete')]),
        ),
        migrations.AlterField(
            model_name='category',
            name='status',
            field=models.SmallIntegerField(choices=[(0, b'Inactive'), (1, b'active'), (2, b'Delete')]),
        ),
    ]
