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
        verbose_name = '考试-考场信息'
        verbose_name_plural = '考试-考场信息'

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
        verbose_name = '考试-考生'
        verbose_name_plural = '考试-考生'
    class_name = models.CharField('班级',max_length=100, default='')
    student_name = models.CharField('姓名', max_length=20, default='')
    student_id = models.CharField('学号', max_length=20, default='')
    pass_word = models.CharField('密码', max_length=20, default='', blank=True)

    def __str__(self):
        return self.class_name+" "+self.student_name +" "+self.student_id


class StudentInfoImporter(models.Model):
    class Meta:
        verbose_name = '考试-批量导入考生'
        verbose_name_plural = '考试-批量导入考生信息'

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

    choice_questions = models.TextField("选择题列表", max_length=1000,  blank=True, default='')
    choice_question_answers = models.TextField("选择题答案列表", max_length=1000, blank=True,  default='')
    choice_question_results = models.TextField("选择题评分", max_length=1000, blank=True,  default='')

    coding_questions = models.TextField("编程题列表", max_length=1000, blank=True, default='')
    coding_question_answers = models.TextField("编程题答案列表", max_length=1000, blank=True, default='')
    coding_question_results = models.TextField("编程题评分", max_length=1000, blank=True, default='')

    def start_time_(self):
        return (self.start_time)
    start_time_.short_description = '开考时间'

    def coding_question_answers_(self):
        return self.coding_question_answers.split(',')
    coding_question_answers_.short_description = '编程题答案'

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

    # def coding_questions_all_(self):
    #     coding_question_ids = [int(x) for x in self.coding_questions.split(',') if len(x)]
    #     coding_questions_all = []
    #     for i in coding_question_ids:
    #         coding_questions_all.append(CodingQuestion.objects.get(pk=i))
    #     return coding_questions_all
    # coding_questions_all_.short_description = '全部编程题'

    # ## question_id start from 1 to n
    # def choice_questions_pk_(self, question_id):
    #     question_database_id = int(self.choice_questions.split(',')[question_id-1])
    #     return ChoiceQuestion.objects.get(pk=question_database_id)
    # choice_questions_pk_.short_description = 'pk选择题'

    # def coding_questions_pk_(self, question_id):
    #     question_database_id = int(self.coding_questions.split(',')[question_id-1])
    #     return CodingQuestion.objects.get(pk=question_database_id)
    # coding_questions_pk_.short_description = 'pk编程题'

    def coding_output_path_(self, question_id):
        output_save_path = os.path.join(MEDIA_ROOT, 'upload_output','coding_output_{}_{}.txt'.format(self.id, question_id))
        return output_save_path
    coding_output_path_.short_description = '上传结果保存目录'

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

        # print(self.choice_question_results)

    def update_coding_question_answer_result_(self, coding_question_id, output_save_path):
        old_answers = self.coding_question_answers.split(',')
        old_answers[coding_question_id-1] = str(output_save_path)
        self.coding_question_answers = ','.join(old_answers)

        ## 
        coding_question = self.coding_questions_pk_(coding_question_id)
        answer_path = coding_question.upload_answer_file.path
        with open(answer_path, encoding='utf-8') as f:
            answers = [x.strip() for x in f.readlines()]
        with open(output_save_path, encoding='utf-8') as f:
            outputs = [x.strip() for x in f.readlines()]
        # print(outputs)
        min_len = min(len(answers), len(outputs))
        correct_cnt = 0
        for i in range(min_len):
            if answers[i] == outputs[i]: correct_cnt = correct_cnt + 1
        score = str(correct_cnt*1.0/len(answers))
        old_answers = self.coding_question_results.split(',')
        old_answers[coding_question_id-1] = score
        print(old_answers)
        self.coding_question_results = ','.join(old_answers)
        self.save()

    def coding_question_result_stat(self):
        answers = [x for x in self.coding_question_answers.split(',') if x!='+']
        results = [float(x) for x in self.coding_question_results.split(',')]
        sum = 0
        for i in range(len(results)):
            sum = sum + results[i]
        return self.exam.coding_question_num, len(answers), sum

    def coding_question_result_detail(self):
        answers = [x for x in self.coding_question_answers.split(',') if x!='+']
        results = [float(x) for x in self.coding_question_results.split(',')]
        return results

    def total_score(self):
        _,_, choice_question_correct_num = self.choice_question_result_stat()
        _,_, coding_question_correct_num = self.coding_question_result_stat()
        return choice_question_correct_num*self.exam.choice_question_score + coding_question_correct_num*self.exam.coding_question_score

