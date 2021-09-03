from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django import forms
from django.utils.html import format_html, format_html_join
import datetime
from django.utils import timezone
import re
import os
import shutil
import zipfile
from pathlib import Path

from docx import Document
from .fileModels import *

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT  = BASE_DIR / 'media'

EXAM_TYPE_CHOICES = [
    ('1','计算等级考试1级'),
    ('2','计算等级考试2级'),
]

PERIOD_CHOICES = [
    ('1','90分钟'),
    ('2','120分钟'),
]

ANSWER_CHOICES = [
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
]


class Exam(models.Model):
    class Meta:
        verbose_name = '考试场次'
        verbose_name_plural = '考试场次'

    pub_date = models.DateTimeField('创建时间', 'date published', null=True, default=timezone.now)
    problem_type = models.CharField("试卷类型", max_length=20, choices=EXAM_TYPE_CHOICES, default='1')
    creator = models.CharField('创建人', max_length=200, default='--老师')
    info_text = models.CharField('考试信息', max_length=200, default='计算机等级考试1级')
    period = models.CharField("考试时长", max_length=5, choices=PERIOD_CHOICES, default='1')

    choice_question_num = models.IntegerField(verbose_name="选择题个数", default=20)
    choice_question_score = models.IntegerField(verbose_name="选择题分值", default=1)
    file_operation_score = models.IntegerField(verbose_name="系统操作题分值", default=10)
    email_score = models.IntegerField(verbose_name="上网题分值", default=10)
    word_score = models.IntegerField(verbose_name="Word操作题分值", default=20)
    excel_score = models.IntegerField(verbose_name="Excel操作题分值", default=20)
    ppt_score = models.IntegerField(verbose_name="PPT操作题分值", default=20)

    def __str__(self):
        return str(self.id) + ' ' +self.info_text

    def id_(self):
        return str(self.id)
    id_.short_description = '考试编号'

    def all_question_stat_(self):


        result_list = [
                        ['选择题'+str(self.choice_question_num)+'X'+str(self.choice_question_score)],
                        ['系统操作题1X'+str(self.file_operation_score)],
                        ['上网题1X'+str(self.email_score)],
                        ['Word操作题1X'+str(self.word_score)],
                        ['Excel操作题1X'+str(self.excel_score)],
                        ['PPT操作题1X'+str(self.ppt_score)],
                        ]
        return  format_html("<ul>") + \
                format_html_join(
                '\n', '<li style="color:black;">{}</li>',
                result_list
                ) \
                + format_html("</ul>")
    all_question_stat_.short_description = '考题统计'

    def exam_type_(self):
        return str(EXAM_TYPE_CHOICES[int(self.problem_type)-1][1])
    exam_type_.short_description = '考试类型'

    def period_(self):
        return str(PERIOD_CHOICES[int(self.period)-1][1])
    period_.short_description = '考试时长'

    def out_link_(self):
        return format_html('<a href="/exam/room/{}" target="_blank">点击查看</a>'.format(self.id))
    out_link_.short_description = '考场详情'


class Student(models.Model):
    class Meta:
        verbose_name = '考生'
        verbose_name_plural = '考生'
    class_name = models.CharField('班级',max_length=100, default='')
    student_name = models.CharField('姓名', max_length=20, default='')
    student_id = models.CharField('学号', max_length=20, default='')
    pass_word = models.CharField('密码', max_length=20, default='', blank=True)

    def __str__(self):
        return self.class_name+" "+self.student_name +" "+self.student_id


class StudentInfoImporter(models.Model):
    class Meta:
        verbose_name = '导入考生信息'
        verbose_name_plural = '导入考生信息'

    def __str__(self):
        return '导入考生信息'+str(self.id)

    upload_description_file = models.FileField(upload_to='upload_student_list/', null=True, blank=True, 
    validators=[validate_txtfile], verbose_name='上传考生信息文件[.txt]')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        print(self.upload_description_file, 'saved')
        with open(self.upload_description_file.path,'r', encoding='utf-8') as f:
            lines = [x.strip().replace('\t',' ').split(' ') for x in f.readlines()[:] if len(x)>0]
            class_name = ''
            for x in lines:
                if len(x)==1: 
                    class_name = x[0]
                    continue
                if len(x)>5 and (x[0] !='学号'):
                    Student.objects.get_or_create(class_name=class_name, student_id=x[0], student_name=x[1])
