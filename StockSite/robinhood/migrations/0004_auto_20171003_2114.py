# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 02:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robinhood', '0003_auto_20171003_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robinhooduser',
            name='token',
            field=models.BinaryField(),
        ),
    ]