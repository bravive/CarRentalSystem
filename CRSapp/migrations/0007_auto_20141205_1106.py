# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CRSapp', '0006_auto_20141128_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartype',
            name='rentalfee',
            field=models.PositiveIntegerField(max_length=200),
        ),
    ]
