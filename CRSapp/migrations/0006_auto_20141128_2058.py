# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CRSapp', '0005_auto_20141128_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userreservehistory',
            name='status_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userreservehistory',
            name='status_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userreservehistory',
            name='status_reserved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userreservehistory',
            name='status_returned',
            field=models.BooleanField(default=False),
        ),
    ]
