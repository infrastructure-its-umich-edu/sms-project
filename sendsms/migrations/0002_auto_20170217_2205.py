# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sendsms', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smsmessage',
            name='uuid',
        ),
        migrations.AddField(
            model_name='smsmessage',
            name='msgid',
            field=models.UUIDField(default=datetime.datetime(2017, 2, 17, 22, 5, 25, 156529, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
    ]
