# Generated by Django 3.0.6 on 2020-05-06 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200505_2054'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='book',
            unique_together=set(),
        ),
    ]
