# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogtable',
            name='status',
            field=models.SmallIntegerField(choices=[(0, b'Inactivate'), (1, b'activate'), (2, b'Delete')]),
        ),
    ]
