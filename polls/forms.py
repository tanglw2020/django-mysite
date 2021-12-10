
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
    student_id = forms.CharField(label='学号', max_length=50)

    def clean(self):
        cleaned_data = super().clean()
        exam_id = cleaned_data['exam_id']
        student_id = str(cleaned_data['student_id'])

        if not Exam.objects.filter(id=exam_id).exists():
            self.add_error('exam_id', '考试编号不存在')
        if not Student.objects.filter(student_id=student_id).exists():
            self.add_error('student_id', '学号不存在')


class StudentFormSecondLogin(forms.Form):
    exam_id = forms.IntegerField(label='考场编号')
    name = forms.CharField(label='姓名',  max_length=50)
    student_id = forms.CharField(label='学号', max_length=50)
    password = forms.CharField(label='登录密码', max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))

    def clean(self):
        cleaned_data = super().clean()
        exam_id = cleaned_data['exam_id']
        student_id = str(cleaned_data['student_id'])
        password = str(cleaned_data['password'])

        if not Exam.objects.filter(id=exam_id).exists():
            self.add_error('exam_id', '考试编号不存在')
            return
        if not Student.objects.filter(student_id=student_id).exists():
            self.add_error('student_id', '学号不存在')
            return
        if Exam.objects.get(id=exam_id).passwd_second_login != password:
            self.add_error('password', '密码错误')


class UploadWordForm(forms.Form):
    file = forms.FileField(label='upload-word-file', validators=[validate_docx, validate_file_size]) 

class UploadExcelForm(forms.Form):
    file = forms.FileField(label='upload-excel-file', validators=[validate_xlsx, validate_file_size]) 

class UploadPPTForm(forms.Form):
    file = forms.FileField(label='upload-ppt-file', validators=[validate_pptx, validate_file_size]) 

class UploadZipFileForm(forms.Form):
    file = forms.FileField(label='upload-zip-file', validators=[validate_zipfile, validate_file_size]) 


class SendEmailForm(forms.Form):
    name1 = forms.CharField(label='收件人:',  max_length=200)
    name2 = forms.CharField(label='抄送人:',  max_length=200)
    topic = forms.CharField(label='主  题:',  max_length=200)
    content = forms.CharField(label='内  容:',  widget=forms.Textarea(attrs={'cols': '80', 'rows': '5'}))

class TextInputForm(forms.Form):
    content = forms.CharField(label='',  widget=forms.Textarea(attrs={'cols': 130, 'rows': 16}))