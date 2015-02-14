# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('CRSapp', '0002_auto_20141117_0601'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserReserveHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=200)),
                ('CIN', models.CharField(max_length=200)),
                ('fromdate', models.CharField(max_length=200)),
                ('fromtime', models.CharField(max_length=200)),
                ('todate', models.CharField(max_length=200)),
                ('totime', models.CharField(max_length=200)),
                ('createdtime', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
