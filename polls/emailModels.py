import os
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html, format_html_join

TitleName=[
    ('感谢', '感谢'),
    ('hello', 'hello'),
    ('一路有你', '一路有你'),
    ('生日快乐', '生日快乐'),
    ('求职简历','求职简历')
]

DesEmail=[
    ('lucy@163.com', 'lucy@163.com'),
    ('llkk@163.com', 'llkk@163.com')
]

# Create your models here.
class EmailQuestion(models.Model):
    # 控制 表项显示文字，默认按 类名object（n）显示
    def __str__(self):
        return '电子邮件题' + str(self.id)

    # 内部标签，表名 项目显示名  项目详细名等
    class Meta:
        db_table = 'email_table'  # 表名
        verbose_name_plural = '电子邮件题'  # 项目名
        verbose_name = '电子邮件题'  # 详细名称

    # 题型
    # 建立选择下拉框
    des_name = models.CharField('收件方', choices=DesEmail, max_length=50, blank=True, default='')
    cop_name = models.CharField('抄送给', choices=DesEmail, max_length=50, blank=True, default='')
    topic = models.CharField('主  题', max_length=50, blank=True, default='')
    content = models.TextField('内  容',  default='')

    # 提交前的判断
    def clean(self):
        # raise ValidationError('请完善未选择的项目。')
        if self.des_name == '':
            raise ValidationError(_('收件人不能为空'))

        if self.cop_name == '':
            raise ValidationError(_('抄送人不能为空'))

        if self.topic == '':
            raise ValidationError(_('主题不能为空'))

        if self.content == '':
            raise ValidationError(_('邮件内容不能为空'))

        if self.des_name == self.cop_name:
            raise ValidationError(_('抄送人不能和收件人相同'))


