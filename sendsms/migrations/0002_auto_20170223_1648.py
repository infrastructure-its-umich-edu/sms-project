# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendsms', '0001_squashed_0003_smsmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smsmessage',
            name='message',
            field=models.CharField(max_length=160, verbose_name=b'Message'),
        ),
    ]
