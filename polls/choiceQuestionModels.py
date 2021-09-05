from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html, format_html_join

ANSWER_CHOICES = [
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
]

class ChoiceQuestion(models.Model):

    class Meta:
        verbose_name = '题目-选择题'
        verbose_name_plural = '题目-选择题'

    def __str__(self):
        return '选择题'+str(self.id)

    def description(self):
        choice_list = [
            ['white', 'A. '+ self.choice_1], 
            ['white', 'B. '+  self.choice_2], 
            ['white', 'C. '+  self.choice_3], 
            ['white', 'D. '+  self.choice_4], 
            ]
        choice_list[int(self.answer)-1][0] = 'Lime'

        return format_html("<ul>") + \
                format_html_join(
                '\n', '<li style="background-color:{};">{}</li>',
                ((x[0], x[1]) for x in choice_list)
                ) \
                + format_html("</ul>")
    description.short_description = '题目内容'

    question_text = models.TextField('题干')
    choice_1 = models.CharField('选项1', max_length=200,  default='')
    choice_2 = models.CharField('选项2', max_length=200,  default='')
    choice_3 = models.CharField('选项3', max_length=200,  default='')
    choice_4 = models.CharField('选项4', max_length=200,  default='')

    answer = models.CharField('答案', max_length=2, choices= ANSWER_CHOICES)

