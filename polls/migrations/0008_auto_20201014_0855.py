# Generated by Django 3.1.2 on 2020-10-14 00:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20201014_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordquestion',
            name='upload_word',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.worddocxfile', verbose_name='测试文件.docx'),
        ),
    ]
