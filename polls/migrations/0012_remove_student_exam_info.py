# Generated by Django 3.1.2 on 2020-11-30 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_auto_20201130_1956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='exam_info',
        ),
    ]
