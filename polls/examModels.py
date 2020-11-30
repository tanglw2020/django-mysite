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
    def __str__(self):
        return  self.exam_type+'-'+self.exam_name

    def exam_special_id(self):
        return  self.pub_date.date().isoformat()+'-'+str(self.id)
    exam_special_id.short_description = '考试编码(考生登录时填写)'



