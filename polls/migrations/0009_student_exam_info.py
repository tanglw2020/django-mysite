# Generated by Django 3.1.2 on 2020-11-30 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_exam'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='exam_info',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='polls.exam', verbose_name='考试信息'),
        ),
    ]