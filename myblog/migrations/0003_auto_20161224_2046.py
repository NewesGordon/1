# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2016-12-24 12:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0002_auto_20161222_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogbody',
            name='blog_clicknum',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='blogbody',
            name='blog_ismarkdown',
            field=models.CharField(max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='blogbody',
            name='blog_like',
            field=models.IntegerField(null=True),
        ),
    ]