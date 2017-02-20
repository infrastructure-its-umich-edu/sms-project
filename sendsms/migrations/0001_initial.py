# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SMSMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recipients', models.TextField(help_text=b'Multiple numbers should be seperated by semicolon(;)', verbose_name=b'Phone Numbers', validators=[django.core.validators.RegexValidator(regex=b'^(\\(?([2-9][0-8][0-9])\\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4});?)+$')])),
                ('uuid', models.UUIDField()),
                ('submit_time', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(max_length=145, verbose_name=b'Message')),
                ('sender', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
