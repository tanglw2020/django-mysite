import os
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html, format_html_join
from difflib import SequenceMatcher


class TextQuestion(models.Model):
    def __str__(self):
        return '文字录入' + str(self.id)

    class Meta:
        verbose_name_plural = '题目-文字录入' 
        verbose_name = '题目-文字录入'  

    def score_(self, input_text):
        if type(input_text)!= str: return 0.0
        if len(self.content)<1 or len(input_text)<1: return 0.0
        equel_size = 0.0
        for block in SequenceMatcher(None, input_text, self.content).get_matching_blocks():
            equel_size = equel_size + block[2]
        return equel_size / len(self.content)

    content = models.TextField('录入内容',  default='')



