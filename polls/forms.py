
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import datetime

from .examModels import *
from polls.fileModels import *

class StudentForm(forms.Form):
    exam_id = forms.IntegerField(label='考场编号')
    name = forms.CharField(label='姓名',  max_length=50)
    student_id = forms.IntegerField(label='学号')

    def clean(self):
        cleaned_data = super().clean()
        exam_id = cleaned_data['exam_id']
        student_id = str(cleaned_data['student_id'])

        if not Exam.objects.filter(id=exam_id).exists():
            self.add_error('exam_id', '考试编号不存在')
        if not Student.objects.filter(student_id=student_id).exists():
            self.add_error('student_id', '学号不存在')


class UploadZipFileForm(forms.Form):
    file = forms.FileField(label='upload-zip-file', validators=[validate_zipfile]) 

    # def clean(self):
    #     cleaned_data = super().clean()
    #     filename = cleaned_data['file']
        # if filename[-4:] != '.zip':
        #     # self.add_error('file', '只能上传.zip文件')
        #     raise ValidationError(_('只能上传.zip文件'))


class SendEmailForm(forms.Form):
    name1 = forms.CharField(label='收件人:',  max_length=200)
    name2 = forms.CharField(label='抄送人:',  max_length=200)
    topic = forms.CharField(label='主  题:',  max_length=200)
    content = forms.CharField(label='内  容:',  widget=forms.Textarea)