# Generated by Django 3.1.2 on 2020-10-21 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_auto_20201021_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordoperations',
            name='style_name',
            field=models.CharField(blank=True, choices=[('MS Gothic', 'MS Gothic'), ('MS Mincho', 'MS Mincho'), ('MS PMincho', 'MS PMincho'), ('MS UI Gothic', 'MS UI Gothic'), ('Yu Gothic', 'Yu Gothic')], max_length=200, verbose_name='样式名称'),
        ),
    ]
