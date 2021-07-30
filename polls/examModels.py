from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from docx import Document
import os
import datetime

EXAM_TYPE_CHOICES = [
    ('计算机等级考试一','计算机等级考试一'),
]

class Exam(models.Model):

    pub_date = models.DateTimeField('创建时间')
    exam_name = models.CharField('考试学期',  max_length=50)
    exam_type = models.CharField('考试类型', choices = EXAM_TYPE_CHOICES, max_length=50)

    class Meta:
        verbose_name = '考试信息'
        verbose_name_plural = '考试信息'
    def exam_long_name(self):
        return  self.exam_type+'-'+self.exam_name
    exam_long_name.short_description = '考试名称'

    def __str__(self):
        return  self.pub_date.date().isoformat()+'-'+str(self.id)

    def special_id(self):
        return  str(self.id)
    special_id.short_description = '考试编号(考生登录时使用)'


class ExamPaper(models.Model):

    exam_type = models.CharField('考试类型', choices = EXAM_TYPE_CHOICES, max_length=50, default=EXAM_TYPE_CHOICES[0][0])

    student_id = models.CharField('学号', max_length=20, default='-')
    start_time = models.DateTimeField('开考时间')
    end_by_hand = models.BooleanField('是否已经手动结束')
    delay_by_hand = models.PositiveIntegerField('手动延时(分钟)', default=0)

    choice_question_list = models.CharField('选择题', max_length=200, default='-')
    system_question_id = models.PositiveIntegerField('系统操作题', default=0)
    internet_question_id = models.PositiveIntegerField('上网题', default=0)
    word_question_id = models.PositiveIntegerField('word操作题', default=0)
    excel_question_id = models.PositiveIntegerField('excel操作题', default=0)
    ppt_question_id = models.PositiveIntegerField('ppt操作题', default=0)

    choice_question_answer = models.CharField('选择题答案', max_length=200, default='-')
    current_choice_question_id = models.PositiveIntegerField('当前选择题', default=0)
    system_question_answer_file = models.CharField('系统操作题答案', max_length=200, default='-')
    internet_question_answer_file = models.CharField('上网题答案', max_length=200, default='-')
    word_question_answer_file = models.CharField('word操作题答案', max_length=200, default='-')
    excel_question_answer_file = models.CharField('excel操作题答案', max_length=200, default='-')
    ppt_question_answer_file = models.CharField('ppt操作题答案', max_length=200, default='-')

    class Meta:
        verbose_name = '试卷'
        verbose_name_plural = '试卷'

    def __str__(self):
        return  self.exam_type+'-'+str(self.id)
