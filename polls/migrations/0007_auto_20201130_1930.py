# Generated by Django 3.1.2 on 2020-11-30 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20201118_1549'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=50, verbose_name='班级')),
                ('name', models.CharField(max_length=50, verbose_name='姓名')),
                ('student_id', models.CharField(max_length=50, verbose_name='学号')),
            ],
            options={
                'verbose_name': '考生',
                'verbose_name_plural': '考生',
            },
        ),
        migrations.AlterField(
            model_name='wordoperations',
            name='table_alignment',
            field=models.CharField(choices=[('None', '左对齐'), ('CENTER (1)', '居中'), ('RIGHT (2)', '右对齐')], default='', max_length=10, verbose_name='对齐方式'),
        ),
        migrations.AlterField(
            model_name='wordoperations',
            name='table_style',
            field=models.CharField(choices=[('Grid Table Light', '网格型浅色'), ('Plain Table 3', '无格式表格3'), ('Grid Table 2 Accent 1', '网格表2着色1'), ('Grid Table 2 Accent 1', '网格表5深色'), ('List Table 1 Light', '清单表1浅色'), ('List Table 6 Colorful', '清单表6彩色')], default='', max_length=30, verbose_name='表格样式'),
        ),
    ]
