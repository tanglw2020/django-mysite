from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from docx import Document
import os

from .examModels import Exam

class Student(models.Model):

    exam_info = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE, blank=True, default='',
        verbose_name='考试编号(考试登录时填写)'
    )
    class_name = models.CharField('班级',  max_length=50)
    name = models.CharField('姓名',  max_length=50)
    student_id = models.CharField('学号',  max_length=50)

    class Meta:
        verbose_name = '考生'
        verbose_name_plural = '考生'

    def __str__(self):
        return str(self.class_name)+'-'+str(self.name)+'-'+self.student_id

    def exam_name(self):
        return self.exam_info.exam_name
    exam_name.short_description = '考试名称'

    def exam_id(self):
            return self.exam_info.id
    exam_id.short_description = '考试编号'


