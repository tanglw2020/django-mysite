# Generated by Django 3.1.2 on 2020-10-12 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20201012_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordquestion',
            name='upload',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
