import os
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html, format_html_join


DesEmail=[
    ('lucy@hysf.edu', 'lucy@hysf.edu'),
    ('wukong@xiyou.com', 'wukong@xiyou.com'),
    ('bajie@xiyou.com', 'bajie@xiyou.com'),
    ('jiabaoyu@hongluo.cn', 'jiabaoyu@hongluo.cn'),
    ('xuebaochai@hongluo.cn', 'xuebaochai@hongluo.cn'),
    ('songjia@shuifu.cn', 'songjia@shuifu.cn'),
    ('wusong@shuifu.cn', 'wusong@shuifu.cn'),
    ('likui@shuifu.cn', 'likui@shuifu.cn'),
]

# Create your models here.
class EmailQuestion(models.Model):
    def __str__(self):
        return '电子邮件' + str(self.id)

    class Meta:
        db_table = 'email_table'  
        verbose_name_plural = '题目-电子邮件' 
        verbose_name = '题目-电子邮件题'  

    def question_content(self):
            result_list = []
            result_list.append('收件人：'+self.des_name+'.')
            result_list.append('抄送人：'+self.cop_name+'.')
            result_list.append('主  题：'+self.topic+'.')
            result_list.append('内  容：'+self.content+'.')
            return format_html("发送一封电子邮件，具体内容要求如下：\n") + format_html("<ul>") + \
                format_html_join(
                '\n', '<li style="color:black;">{}</li>',
                ((x,) for x in result_list)
                ) \
                + format_html("</ul>")
    question_content.short_description = '题目内容'

    des_name = models.CharField('收件人', choices=DesEmail, max_length=50,  default='')
    cop_name = models.CharField('抄 送', choices=DesEmail, max_length=50,  default='')
    topic = models.CharField('主  题', max_length=100, default='')
    content = models.TextField('内  容',  default='')

    # 提交前的判断
    def clean(self):
        # raise ValidationError('请完善未选择的项目。')
        # if self.des_name == '':
        #     raise ValidationError(_('收件人不能为空'))

        # if self.cop_name == '':
        #     raise ValidationError(_('抄送人不能为空'))

        # if self.topic == '':
        #     raise ValidationError(_('主题不能为空'))

        # if self.content == '':
        #     raise ValidationError(_('邮件内容不能为空'))

        if self.des_name == self.cop_name:
            raise ValidationError(_('抄送人不能和收件人相同'))


