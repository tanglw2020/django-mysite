from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from docx import Document
from .choices import *

import os

# Create your models here.
class WordOperations(models.Model):

    class Meta:
        verbose_name = 'Word操作'
        verbose_name_plural = 'Word操作'

    def __str__(self):
        return str(self.id)+':'+self.operations_list()

    def para_text_simple(self):
        return self.para_text[:10] +'...'+self.para_text[-10:]
    para_text_simple.short_description = '考查段落内容'

    def operations_list(self):
            op_list = ''
            if self.char_edit_op:
                op_list += '#文字查找替换  '
            if self.font_op:
                op_list += '#字体设置  '
            if self.paraformat_op:
                op_list += '#段落格式设置  '
            return op_list
    operations_list.short_description = '操作列表'

    pub_date = models.DateTimeField('创建时间')
    para_text = models.TextField('要考查的段落内容')

    ############## 文字查找替换
    char_edit_op = models.BooleanField('是否考查文字查找替换？', default=False)
    char_edit_origin = models.CharField('原词', max_length=200, blank=True)
    char_edit_replace = models.CharField('替换为', max_length=200, blank=True)
    # char_edit_result = models.CharField('文字编辑结果', widget=models.Textarea, blank=True)

    ############## 字体设置
    font_op = models.BooleanField('是否考查字体设置？', default=False)
    font_name_ascii = models.CharField('英文字体', choices=FONT_NAME_ASCII_CHOICES, max_length=200, blank=True) 
    font_name_chinese = models.CharField('中文字体', choices=FONT_NAME_CHINESE_CHOICES, max_length=200, blank=True)
    font_size = models.CharField('字号', choices=FONT_SIZE_CHOICES, max_length=200, blank=True)
    font_bold = models.BooleanField('粗体', blank=True)
    font_italic = models.BooleanField('斜体', blank=True)
    font_underline = models.CharField('下划线', choices=FONT_UNDERLINE_CHOICES, max_length=200, blank=True)
    font_color = models.CharField('字体颜色', choices=FONT_COLOR_CHOICES, max_length=200, blank=True)

    ############## 段落格式设置
    paraformat_op = models.BooleanField('是否考查段落格式设置？', default=False)
    para_alignment = models.CharField('段落对齐', choices=PARA_ALIGNMENT_CHOICES, max_length=200, blank=True)
    para_left_indent = models.CharField('左侧缩进(磅)', choices=INDENT_NUM_CHOICES, max_length=200, blank=True)
    para_right_indent = models.CharField('右侧缩进(磅)', choices=INDENT_NUM_CHOICES, max_length=200, blank=True)
    para_first_line_indent = models.CharField('首行缩进', choices=PARA_FIRST_LINE_INDENT_CHOICES, max_length=200, blank=True)
    para_first_line_indent_size = models.CharField('首行缩进距离(磅)', choices=INDENT_NUM_CHOICES, max_length=200, blank=True)

    para_space_before = models.CharField('段前间距(磅)',  choices=INDENT_NUM_CHOICES, max_length=200, blank=True)
    para_space_after = models.CharField('段后间距(磅)',  choices=INDENT_NUM_CHOICES, max_length=200, blank=True)
    para_line_spacing_rule = models.CharField('行距规则', choices=PARA_LINE_SPACING_RULE_CHOICES, max_length=200, blank=True)
    para_line_spacing = models.CharField('行距(行)',  choices=LINE_NUM_CHOICES, max_length=200, blank=True)

    para_firstchardropcap = models.CharField('首字下沉', choices=PARA_FIRSTCHARDROPCAP_CHOICES, max_length=200, blank=True)
    para_firstchardropcaplines = models.CharField('下沉(行)',  choices=LINE_NUM_CHOICES, max_length=200, blank=True)

    page_break_before = models.BooleanField('段前分页', default=False)
    keep_with_next = models.BooleanField('与下段同页', default=False)
    keep_together = models.BooleanField('段中不分页', default=False)
    window_control = models.BooleanField('孤行控制', default=False)

    ############## 样式设置
    style_op = models.BooleanField('是否考样式设置？', default=False)
    style_name = models.CharField('样式名称', choices=STYLE_NAME_CHOICES, max_length=200, blank=True) 
    style_font_name_ascii = models.CharField('英文字体', choices=FONT_NAME_ASCII_CHOICES, max_length=200, blank=True) 
    style_font_name_chinese = models.CharField('中文字体', choices=FONT_NAME_CHINESE_CHOICES, max_length=200, blank=True)
    style_font_size = models.CharField('字号', choices=FONT_SIZE_CHOICES, max_length=200, blank=True)
    style_font_bold = models.BooleanField('粗体', default=False)
    style_font_italic = models.BooleanField('斜体', default=False)
    style_font_underline = models.CharField('下划线', choices=FONT_UNDERLINE_CHOICES, max_length=200, blank=True)
    style_font_color = models.CharField('字体颜色', choices=FONT_COLOR_CHOICES, max_length=200, blank=True)

    style_para_alignment = models.CharField('段落对齐', choices=PARA_ALIGNMENT_CHOICES, max_length=200, blank=True)
    style_para_left_indent = models.CharField('左侧缩进(磅)',  choices=INDENT_NUM_CHOICES, max_length=200, blank=True)
    style_para_right_indent = models.CharField('右侧缩进(磅)',  choices=INDENT_NUM_CHOICES, max_length=200, blank=True)
    style_para_first_line_indent = models.CharField('首行缩进', choices=PARA_FIRST_LINE_INDENT_CHOICES, max_length=200, blank=True)
    style_para_first_line_indent_size = models.CharField('首行缩进距离(磅)',  choices=INDENT_NUM_CHOICES, max_length=200, blank=True)

    style_para_space_before = models.CharField('段前间距(磅)',   choices=INDENT_NUM_CHOICES, max_length=200, blank=True)
    style_para_space_after = models.CharField('段后间距(磅)',   choices=INDENT_NUM_CHOICES, max_length=200, blank=True)
    style_para_line_spacing_rule = models.CharField('行距规则', choices=PARA_LINE_SPACING_RULE_CHOICES, max_length=200, blank=True)
    style_para_line_spacing = models.CharField('行距(行)',   choices=LINE_NUM_CHOICES, max_length=200, blank=True)

    style_para_firstchardropcap = models.CharField('首字下沉', choices=PARA_FIRSTCHARDROPCAP_CHOICES, max_length=200, blank=True)
    style_para_firstchardropcaplines = models.CharField('下沉(行)',   choices=LINE_NUM_CHOICES, max_length=200, blank=True)

    style_page_break_before = models.BooleanField('段前分页', default=False)
    style_keep_with_next = models.BooleanField('与下段同页', default=False)
    style_keep_together = models.BooleanField('段中不分页', default=False)
    style_window_control = models.BooleanField('孤行控制', default=False)

def validate_docx(value):

    extension = value.name.split('.')[-1]
    if extension != 'docx':
        raise ValidationError(
            _(value.name+'不是docx文件'),
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

class WordDocxFile(models.Model):

    upload = models.FileField(upload_to='uploads_docx/', null=True, blank=True, 
    validators=[validate_docx])
    class Meta:
        verbose_name = '考试用Word文件'
        verbose_name_plural = '考试用Word文件'
    def __str__(self):
        return self.upload.name

class WordDocxFileTest(models.Model):
    
    upload = models.FileField(upload_to='uploads_docx_test/', null=True, blank=True, 
    validators=[validate_docx])

    class Meta:
        verbose_name = '内部测试用word文件'
        verbose_name_plural = '内部测试用word文件'
    def __str__(self):
        return self.upload.name

# Create your models here.
class WordQuestion(models.Model):

    class Meta:
        verbose_name = 'Word题目'
        verbose_name_plural = 'Word题目'

    def file_path(self):
        return self.upload_docx.upload.name
    file_path.short_description = '文件'

    def word_op_numb(self):
            return len(self.word_operation_list.all())
    word_op_numb.short_description = '题目数量'

    def word_op_description(self):
            return [ x.operations_list()+'||' for x in self.word_operation_list.all()]
    word_op_description.short_description = '题目内容'

    def word_test_result(self):
            return self.upload_docx.upload.name + "::" + self.upload_docx_test.upload.name
    word_test_result.short_description = '测试结果'


    #########
    pub_date = models.DateTimeField('创建时间')

    upload_docx =  models.ForeignKey(
        WordDocxFile,
        on_delete=models.CASCADE, null=True,
        verbose_name='考试用Word文件(.docx)'
    )
    word_operation_list = models.ManyToManyField(WordOperations, blank=True,
    verbose_name='操作题目')

    upload_docx_test = models.ForeignKey(
        WordDocxFileTest,
        on_delete=models.CASCADE, null=True, blank=True,
        verbose_name='内部测试用word文件.docx'
    )