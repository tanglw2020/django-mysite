from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms
from django.utils.html import format_html, format_html_join
from django.utils import timezone

import datetime
import re
import os
import shutil
import zipfile
from pathlib import Path

from docx import Document
from polls.fileModels import *
from polls.choiceQuestionModels import ChoiceQuestion
from polls.emailModels import EmailQuestion
from polls.fileOperationlModels import FileOperationQuestion
from polls.wordModels import WordQuestion
from polls.excelModels import ExcelQuestion
from polls.pptModels import PPTQuestion
from polls.textinputModels import TextQuestion

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT  = BASE_DIR / 'media'

EXAM_TYPE_CHOICES = [
    ('1','计算机等级考试1级'),
    ('2','计算机等级考试2级'),
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
        verbose_name = '考试-考场信息'
        verbose_name_plural = '考试-考场信息'

    pub_date = models.DateTimeField('创建时间', 'date published', null=True, default=timezone.now)
    problem_type = models.CharField("试卷类型", max_length=20, choices=EXAM_TYPE_CHOICES, default='1')
    creator = models.CharField('创建人', max_length=200, default='--老师')
    info_text = models.CharField('考试信息', max_length=200, default='计算机等级考试1级')
    period = models.CharField("考试时长", max_length=5, choices=PERIOD_CHOICES, default='1')

    choice_question_num = models.IntegerField(verbose_name="选择题个数", default=20)
    choice_question_score = models.IntegerField(verbose_name="选择题分值", default=1)
    text_score = models.IntegerField(verbose_name="文字录入题分值", default=20)
    file_operation_score = models.IntegerField(verbose_name="操作系统题分值", default=10)
    email_score = models.IntegerField(verbose_name="上网题分值", default=10)
    word_score = models.IntegerField(verbose_name="Word操作题分值", default=20)
    excel_score = models.IntegerField(verbose_name="Excel操作题分值", default=10)
    ppt_score = models.IntegerField(verbose_name="PPT操作题分值", default=10)

    def __str__(self):
        return str(self.id) + ' ' +self.info_text

    def clean(self):
        score = self.choice_question_num*self.choice_question_score + \
            self.text_score + self.email_score + self.file_operation_score+ \
                self.word_score + self.excel_score + self.ppt_score
        if score != 100:
            raise ValidationError(_('总分值不等于100'))

    def id_(self):
        return str(self.id)
    id_.short_description = '考试编号'

    def all_question_stat_(self):
        result_list = []
        if self.choice_question_num and self.choice_question_score:
            result_list.append(['选择题'+str(self.choice_question_num)+' X '+str(self.choice_question_score)])
        if self.text_score:
            result_list.append(['文字录入题'+str(self.text_score)])
        if self.email_score:
            result_list.append(['上网题'+str(self.email_score)])
        if self.file_operation_score:
            result_list.append(['操作系统题'+str(self.file_operation_score)])
        if self.word_score:
            result_list.append(['Word操作题'+str(self.word_score)])
        if self.excel_score:
            result_list.append(['Excel操作题'+str(self.excel_score)])
        if self.ppt_score:
            result_list.append(['PPT操作题'+str(self.ppt_score)])

        return  format_html("<ul>") + \
                format_html_join(
                '\n', '<li style="color:black;">{}</li>',
                result_list
                ) \
                + format_html("</ul>")
    all_question_stat_.short_description = '题目分值统计'

    def exam_type_(self):
        return str(EXAM_TYPE_CHOICES[int(self.problem_type)-1][1])
    exam_type_.short_description = '考试类型'

    def period_(self):
        return str(PERIOD_CHOICES[int(self.period)-1][1])
    period_.short_description = '考试时长'

    def out_link_(self):
        return format_html('<a href="/exam/room/I-1iak_sdo123pf37lkn==Yl234kf1e4{}21oio32874ia78412j765s98fuo" target="_blank">点击查看</a>'.format(self.id))
    out_link_.short_description = '考场详情'


class Student(models.Model):
    class Meta:
        verbose_name = '考试-考生'
        verbose_name_plural = '考试-考生'
    class_name = models.CharField('班级',max_length=100, default='')
    student_name = models.CharField('姓名', max_length=20, default='')
    student_id = models.CharField('学号', max_length=20, default='')
    pass_word = models.CharField('密码', max_length=20, default='', blank=True)

    def __str__(self):
        return self.class_name+" "+self.student_name +" "+self.student_id


class ExamPaper(models.Model):
    class Meta:
        verbose_name = '考试-试卷'
        verbose_name_plural = '考试-试卷'

    def __str__(self):
        return '试卷'+str(self.id)

    problem_type = models.CharField("试卷类型", max_length=20, choices=EXAM_TYPE_CHOICES, default='1')
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE, null=True,
        verbose_name='所属考生'
    ) 
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE, null=True,
        verbose_name='所属考试'
    ) 

    start_time = models.DateTimeField('开考时间', null=True, blank=True, default=timezone.now)
    end_time = models.DateTimeField('交卷时间', null=True, blank=True, default=timezone.now)
    add_time = models.IntegerField("附加延时[分]", default=0)
    enabled = models.BooleanField("是否可以作答?", default=True)

    student_id_local = models.CharField('学号', max_length=20, default='')
    exam_id_local = models.CharField('考场号', max_length=20, default='')

    choice_questions = models.TextField("选择题列表", max_length=1000,  blank=True, default='')
    choice_question_answers = models.TextField("选择题答案列表", max_length=1000, blank=True,  default='')
    choice_question_results = models.TextField("选择题评分", max_length=1000, blank=True,  default='0')

    text_question = models.CharField("文字录入题", max_length=10, blank=True, default='')
    text_question_answer = models.TextField("文字录入题答案", blank=True, default='')
    text_question_result = models.CharField("文字录入题评分", max_length=10, blank=True, default='0')

    system_operation_question = models.CharField("系统操作题", max_length=1000, blank=True, default='')
    system_operation_answer = models.TextField("系统操作题答案", max_length=1000, blank=True, default='')
    system_operation_result = models.CharField("系统操作题评分", max_length=1000, blank=True, default='0')
    system_operation_submit_cnt = models.CharField("系统操作题提交次数", max_length=10, blank=True, default='0')

    email_question = models.CharField("上网题", max_length=10, blank=True, default='')
    email_answer = models.TextField("上网题答案", max_length=1000, blank=True, default='')
    email_result = models.CharField("上网题评分", max_length=10, blank=True, default='0')

    word_question = models.CharField("Word题", max_length=10, blank=True, default='')
    word_answer = models.TextField("Word题答案", max_length=1000, blank=True, default='')
    word_result = models.CharField("Word题评分", max_length=10, blank=True, default='0')
    word_submit_cnt = models.CharField("Word题提交次数", max_length=10, blank=True, default='0')
    
    excel_question = models.CharField("excel题", max_length=10, blank=True, default='')
    excel_answer = models.TextField("excel题答案", max_length=1000, blank=True, default='')
    excel_result = models.CharField("excel题评分", max_length=10, blank=True, default='0')
    excel_submit_cnt = models.CharField("Excel题提交次数", max_length=10, blank=True, default='0')

    ppt_question = models.CharField("ppt题", max_length=10, blank=True, default='')
    ppt_answer = models.TextField("ppt题答案", max_length=1000, blank=True, default='')
    ppt_result = models.CharField("ppt题评分", max_length=10, blank=True, default='0')
    ppt_submit_cnt = models.CharField("PPT题提交次数", max_length=10, blank=True, default='0')


    def start_time_(self):
        return (self.start_time.strftime("%Y-%m-%d %H:%M:%S"))
    start_time_.short_description = '开考时间'

    def end_time_(self):
        return (self.end_time.strftime("%Y-%m-%d %H:%M:%S"))
    end_time_.short_description = '结束时间'

    def text_questions_pk_(self):
        return TextQuestion.objects.get(pk=int(self.text_question))
    text_questions_pk_.short_description = 'pk文字录入题'

    def system_questions_pk_(self):
        return FileOperationQuestion.objects.get(pk=int(self.system_operation_question))
    system_questions_pk_.short_description = 'pk操作系统题'

    def email_questions_pk_(self):
        return EmailQuestion.objects.get(pk=int(self.email_question))
    system_questions_pk_.short_description = 'pk上网题'

    def word_questions_pk_(self):
        return WordQuestion.objects.get(pk=int(self.word_question))
    word_questions_pk_.short_description = 'pk Word题目'

    def excel_questions_pk_(self):
        return ExcelQuestion.objects.get(pk=int(self.excel_question))
    excel_questions_pk_.short_description = 'pk Excel题目'

    def ppt_questions_pk_(self):
        return PPTQuestion.objects.get(pk=int(self.ppt_question))
    ppt_questions_pk_.short_description = 'pk PPT题目'


    def base_path_(self):
        return os.path.join(MEDIA_ROOT, 'upload_exam_answer', str(self.id))

    def system_operation_answer_save_path_(self):
        return os.path.join(self.base_path_(), 'system-operation-{}'.format(self.system_operation_question))

    def word_answer_save_path_(self):
        return os.path.join(self.base_path_(), 'word-{}'.format(self.word_question))

    def excel_answer_save_path_(self):
        return os.path.join(self.base_path_(), 'excel-{}'.format(self.excel_question))

    def ppt_answer_save_path_(self):
        return os.path.join(self.base_path_(), 'ppt-{}'.format(self.ppt_question))

    def choice_question_answers_(self):
        return self.choice_question_answers.split(',')
    choice_question_answers_.short_description = '选择题答案'

    # def choice_questions_all_(self):
    #     choice_question_ids = [int(x) for x in self.choice_questions.split(',') if len(x)]
    #     choice_questions_all = []
    #     for i in choice_question_ids:
    #         choice_questions_all.append(ChoiceQuestion.objects.get(pk=i))
    #     return choice_questions_all
    # choice_questions_all_.short_description = '全部选择题'

    ## question_id start from 1 to n
    def choice_questions_pk_(self, question_id):
        question_database_id = int(self.choice_questions.split(',')[question_id-1])
        return ChoiceQuestion.objects.get(pk=question_database_id)
    choice_questions_pk_.short_description = 'pk选择题'

    def update_choice_question_answer_result_(self, question_id, choice_id):
        old_answers = self.choice_question_answers.split(',')
        old_answers[question_id-1] = str(choice_id)
        self.choice_question_answers = ','.join(old_answers)

        choice_question = self.choice_questions_pk_(question_id)
        if choice_question.answer == str(choice_id):
            score = '1'
        else:
            score = '0'
        old_answers = self.choice_question_results.split(',')
        old_answers[question_id-1] = score
        self.choice_question_results = ','.join(old_answers)
        self.save()

    def choice_question_result_stat(self):
        answers = [x for x in self.choice_question_answers.split(',') if x!='+']
        results = [x for x in self.choice_question_results.split(',') if x=='1']
        return self.exam.choice_question_num, len(answers), len(results)

    def total_score(self):
        _,_, choice_question_correct_num = self.choice_question_result_stat()
        return round(choice_question_correct_num*self.exam.choice_question_score 
                    + float(self.text_question_result)
                    + float(self.email_result)
                    + float(self.system_operation_result) 
                    + float(self.word_result) 
                    + float(self.excel_result) 
                    + float(self.ppt_result), 0)


class StudentInfoImporter(models.Model):
    class Meta:
        verbose_name = '考试-批量导入考生'
        verbose_name_plural = '考试-批量导入考生信息'

    def __str__(self):
        return '导入考生信息'+str(self.id)

    upload_description_file = models.FileField(upload_to='upload_import_files/', null=True, blank=True, 
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

