from django.db import models
from .choices import *

# Create your models here.
class WordOperations(models.Model):

    def para_text_simple(self):
        return self.para_text[:10] +'...'+self.para_text[-10:]

    def operations_list(self):
            op_list = '考查：'
            if self.char_edit_op:
                op_list += '#文字查找替换  '
            if self.font_op:
                op_list += '#字体设置  '
            if self.paraformat_op:
                op_list += '#段落格式设置  '
            return op_list
    para_text_simple.short_description = '考查内容'
    operations_list.short_description = '操作列表'

    pub_date = models.DateTimeField('创建时间')
    para_text = models.TextField('要考查的段落内容', max_length=2000)

    char_edit_op = models.BooleanField('是否考查文字查找替换？', blank=True)
    char_edit_origin = models.CharField('原词', max_length=200, blank=True)
    char_edit_replace = models.CharField('替换为', max_length=200, blank=True)
    # char_edit_result = models.CharField('文字编辑结果', widget=models.Textarea, blank=True)

    font_op = models.BooleanField('是否考查字体设置？', blank=True)
    font_name_ascii = models.CharField('英文字体', choices=FONT_NAME_ASCII_CHOICES, max_length=200, blank=True) 
    font_name_chinese = models.CharField('中文字体', choices=FONT_NAME_CHINESE_CHOICES, max_length=200, blank=True)
    font_size = models.CharField('字号', choices=FONT_SIZE_CHOICES, max_length=200, blank=True)
    font_bold = models.BooleanField('粗体', blank=True)
    font_italic = models.BooleanField('斜体', blank=True)
    font_underline = models.CharField('下划线', choices=FONT_UNDERLINE_CHOICES, max_length=200, blank=True)
    font_color = models.CharField('字体颜色', choices=FONT_COLOR_CHOICES, max_length=200, blank=True)

    paraformat_op = models.BooleanField('是否考查段落格式设置？', blank=True)
    para_alignment = models.CharField('段落对齐', choices=PARA_ALIGNMENT_CHOICES, max_length=200, blank=True)
    para_left_indent = models.DecimalField('左侧缩进(磅)', max_digits=3, decimal_places=1, default=10.0, blank=True)
    para_right_indent = models.DecimalField('右侧缩进(磅)', max_digits=3, decimal_places=1, default=10.0, blank=True)
    para_first_line_indent = models.CharField('首行缩进', choices=PARA_FIRST_LINE_INDENT_CHOICES, max_length=200, blank=True)
    para_first_line_indent_size = models.DecimalField('首行缩进距离(磅)', max_digits=3, decimal_places=1, default=10.0, blank=True)

    para_space_before = models.DecimalField('段前间距(磅)',  max_digits=3, decimal_places=1, default=10.0, blank=True)
    para_space_after = models.DecimalField('段后间距(磅)',  max_digits=3, decimal_places=1, default=10.0, blank=True)
    para_line_spacing_rule = models.CharField('行距规则', choices=PARA_LINE_SPACING_RULE_CHOICES, max_length=200, blank=True)
    para_line_spacing = models.DecimalField('行距(行)',  max_digits=3, decimal_places=1, default=1.0, blank=True)

    para_firstchardropcap = models.CharField('首字下沉', choices=PARA_FIRSTCHARDROPCAP_CHOICES, max_length=200, blank=True)
    para_firstchardropcaplines = models.DecimalField('下沉(行)',  max_digits=3, decimal_places=1, default=3.0, blank=True)

    para_line_page = models.BooleanField('是否考查分页设置？', default=False, blank=True)
    page_break_before = models.BooleanField('段前分页', default=False, blank=True)
    keep_with_next = models.BooleanField('与下段同页', default=False, blank=True)
    keep_together = models.BooleanField('段中不分页', default=False, blank=True)
    window_control = models.BooleanField('孤行控制', default=False, blank=True)


# Create your models here.
class WordQuestion(models.Model):

    pub_date = models.DateTimeField('创建时间')
    word_operation_list = models.ManyToManyField(WordOperations, blank=True)