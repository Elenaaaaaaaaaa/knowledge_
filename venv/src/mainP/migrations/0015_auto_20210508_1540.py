# Generated by Django 3.1.7 on 2021-05-08 15:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainP', '0014_auto_20210508_1521'),
    ]

    operations = [

        migrations.AlterField(
            model_name='documents',
            name='doc_date',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Последние изменения'),
        ),
    ]
