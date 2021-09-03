from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from docx import Document
import os

def validate_image(value):
    extension = value.name.split('.')[-1]
    if extension not in ['jpg','jpeg','png','bmp']:
        raise ValidationError(
            _(value.name+'不是有效图片文件'),
            params={'value': value.name},
        )

def validate_docx(value):

    extension = value.name.split('.')[-1]
    if extension != 'docx':
        raise ValidationError(
            _(value.name+'不是docx文件'),
            params={'value': value.name},
        )

def validate_zipfile(value):
    extension = value.name.split('.')[-1]
    if extension not in ['zip',]:
        raise ValidationError(
            _(value.name+'不是zip压缩文件'),
            params={'value': value.name},
        )

def validate_txtfile(value):
    extension = value.name.split('.')[-1]
    if extension not in ['txt',]:
        raise ValidationError(
            _(value.name+'不是txt文件'),
            params={'value': value.name},
        )
        
    # try:
    #     doc = Document(file_path)
    # except:
    #     raise ValidationError(
    #         _(file_path+'不是有效的docx文件'),
    #         params={'value': file_path},
    #     )
        # print(file_path+'不是有效的docx文件')

# class WordDocxFile(models.Model):

#     upload = models.FileField(upload_to='uploads_docx/', null=True, blank=True, 
#     validators=[validate_docx])
#     class Meta:
#         verbose_name = '考试用Word文件'
#         verbose_name_plural = '考试用Word文件'
#     def __str__(self):
#         return 'Word文件'+str(self.id)+':'+self.upload.name

# class WordDocxFileTest(models.Model):
    
#     upload = models.FileField(upload_to='uploads_docx_test/', null=True, blank=True, 
#     validators=[validate_docx])

#     class Meta:
#         verbose_name = '内部测试用word文件'
#         verbose_name_plural = '内部测试用word文件'
#     def __str__(self):
#         return '测试Word文件'+str(self.id)+':'+self.upload.name
