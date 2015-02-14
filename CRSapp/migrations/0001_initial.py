# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CarInventory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('CIN', models.CharField(max_length=200)),
                ('mile', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
                ('createdtime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CarReserveTimeSheet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fromdate', models.CharField(max_length=200)),
                ('fromtime', models.CharField(max_length=200)),
                ('todate', models.CharField(max_length=200)),
                ('totime', models.CharField(max_length=200)),
                ('car', models.ForeignKey(to='CRSapp.CarInventory')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CarType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cartype', models.CharField(max_length=200)),
                ('rentalfee', models.CharField(max_length=200)),
                ('picture', models.ImageField(upload_to=b'Car-type-picture')),
                ('createdtime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('First_name', models.CharField(default=b'', max_length=200, blank=True)),
                ('Last_name', models.CharField(default=b'', max_length=200, blank=True)),
                ('Address_1', models.CharField(default=b'', max_length=200, blank=True)),
                ('Address_2', models.CharField(default=b'', max_length=200, blank=True)),
                ('City', models.CharField(default=b'', max_length=200, blank=True)),
                ('State', models.CharField(default=b'', max_length=200, blank=True)),
                ('Zip', models.CharField(default=b'', max_length=6, blank=True)),
                ('Country', models.CharField(default=b'', max_length=200, blank=True)),
                ('Phone', models.CharField(default=b'', max_length=15, blank=True)),
                ('picture', models.ImageField(upload_to=b'profile-photos', blank=True)),
                ('owner', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
        migrations.AddField(
            model_name='carinventory',
            name='cartype',
            field=models.ForeignKey(to='CRSapp.CarType'),
            preserve_default=True,
        ),
    ]
