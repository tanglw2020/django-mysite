# Generated by Django 3.1.2 on 2020-12-18 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_exampaper_student_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exampaper',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='开考时间'),
        ),
    ]
