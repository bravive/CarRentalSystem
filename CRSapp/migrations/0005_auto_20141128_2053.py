# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CRSapp', '0004_auto_20141128_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userreservehistory',
            name='status_returned',
            field=models.BooleanField(default=b'True'),
        ),
    ]
