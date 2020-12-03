from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from docx import Document
import os

EXAM_TYPE_CHOICES = [
    ('计算机等级考试一','计算机等级考试一'),
]

class Exam(models.Model):

    pub_date = models.DateTimeField('创建时间')
    exam_name = models.CharField('考场名称',  max_length=50)
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
    
    exam_type = models.CharField('考试类型', choices = EXAM_TYPE_CHOICES, max_length=50)
    choicequestion_list = models.CharField('选择题', max_length=200, default='')
    systemquestion_id = models.PositiveIntegerField('系统操作题', default=0)
    internetquestion_id = models.PositiveIntegerField('上网题', default=0)
    wordquestion_id = models.PositiveIntegerField('word操作题', default=0)
    excelquestion_id = models.PositiveIntegerField('excel操作题', default=0)
    pptquestion_id = models.PositiveIntegerField('ppt操作题', default=0)

    class Meta:
        verbose_name = '试卷'
        verbose_name_plural = '试卷'

    def __str__(self):
        return  self.exam_type+'-'+str(self.id)
