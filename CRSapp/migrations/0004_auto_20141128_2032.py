# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CRSapp', '0003_userreservehistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userreservehistory',
            name='status',
        ),
        migrations.AddField(
            model_name='userreservehistory',
            name='status_confirmed',
            field=models.BooleanField(default=b'False'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userreservehistory',
            name='status_deleted',
            field=models.BooleanField(default=b'False'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userreservehistory',
            name='status_reserved',
            field=models.BooleanField(default=b'False'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userreservehistory',
            name='status_returned',
            field=models.BooleanField(default=b'False'),
            preserve_default=True,
        ),
    ]
