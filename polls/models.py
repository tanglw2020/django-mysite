import os
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html, format_html_join
from docx import Document
from .choices import *
from .fileModels import *


# Create your models here.
class WordQuestion(models.Model):

    def __str__(self):
        return '题目'+str(self.id)+':Word文件'+str(self.upload_docx.id)

    class Meta:
        verbose_name = 'Word题目'
        verbose_name_plural = 'Word题目'

    def file_path(self):
        return self.upload_docx.upload.name
    file_path.short_description = '考查Word文件'

    def word_op_numb(self):
        op_numb = len(self.wordoperations_set.all())
        if op_numb != 5:
            return format_html(
            '<b style="color:red;">{}[不等于5]</b>',
            str(op_numb),
            )
        else:
            return '5'
    word_op_numb.short_description = '题目数量'

    def word_op_description(self):
        result_list = []
        for x in self.wordoperations_set.all():
            result_list.append(['black', x.operations_list()])

        return format_html_join(
                '\n', '<li style="color:{};">{}</li>',
                ((x[0], x[1]) for x in result_list)
                )
    word_op_description.short_description = '题目内容'

    def word_test_result(self):
        return self.upload_docx.upload.name
        # return self.upload_docx.upload.name + "::" + self.upload_docx_test.upload.name
    word_test_result.short_description = '测试文件评估结果'

    # def clean(self):
    #     op_list = [x for x in  self.wordoperations_set.all()]

    #     print(len(op_list))
    #     if len(op_list) != 5:
    #         raise ValidationError({'pub_date':_('Word操作题个数不等于5')})

    #########
    pub_date = models.DateTimeField('创建时间')

    upload_docx =  models.ForeignKey(
        WordDocxFile,
        on_delete=models.CASCADE, null=True,
        verbose_name='上传Word文件(.docx)'
    ) 

    upload_docx_test = models.ForeignKey(
        WordDocxFileTest,
        on_delete=models.CASCADE, null=True, blank=True, default='',
        verbose_name='内部测试用word文件.docx'
    )


# Create your models here.
class WordOperations(models.Model):

    class Meta:
        verbose_name = 'Word操作列表'
        verbose_name_plural = 'Word操作列表'

    def __str__(self):
        return 'Word操作'+str(self.id)

    def word_question_info(self):
        if self.word_question is not None:
            return self.word_question.__str__()
    word_question_info.short_description = '操作所属题目'

    def para_text_simple(self):
        return self.para_text[:10] +'...'+self.para_text[-10:]
    para_text_simple.short_description = '考查段落内容'


    def operations_list(self):
            op_list = []
            if self.char_edit_op:
                op_list.append('查找替换')
            if self.font_op:
                op_list.append('字体设置')
            if self.paraformat_op:
                op_list.append('段落设置')
            if self.style_op:
                op_list.append('样式设置')
            if self.image_op:
                op_list.append('图片插入')
            return '+'.join(op_list)
    operations_list.short_description = '涉及操作'

    def operation_description_all(self):
        description_list = [self.char_edit_description(), self.font_description(),
        self.paraformat_description(), self.style_description()]
        return '将段落"'+self.para_text_simple()+'"'+'，'.join([x for x in description_list if len(x)>0])+'。'
    operation_description_all.short_description = '题目文字描述'

    def char_edit_description(self):
        if self.char_edit_op:
            return '所有“'+self.char_edit_origin+'”替换成“'+self.char_edit_replace+'”'
        else:
            return ''
    char_edit_description.short_description = '查找替换文字描述'

    def font_description(self):
        if self.font_op:
            setting_list=[]
            if self.font_name_chinese !='': setting_list.append('中文'+self.font_name_chinese)
            if self.font_name_ascii !='':  setting_list.append('西文'+self.font_name_ascii)
            if self.font_size !='': setting_list.append('字号'+self.font_size)
            if self.font_color !='': setting_list.append(self.font_color)
            if self.font_bold==True: setting_list.append('粗体')
            if self.font_italic==True: setting_list.append('斜体')
            if self.font_underline !='': setting_list.append(self.font_underline)
            return '字体设置成'+'、'.join(setting_list)
        else:
            return ''
    font_description.short_description = '字体设置描述'

    def paraformat_description(self):
        if self.paraformat_op:
            setting_list=[]
            if self.para_alignment !='': setting_list.append(self.para_alignment)
            if self.para_left_indent !='': setting_list.append('左缩进'+self.para_left_indent+'磅')
            if self.para_right_indent !='': setting_list.append('右缩进'+self.para_right_indent+'磅')
            if self.para_first_line_indent !='' and self.para_first_line_indent_size !='': 
                setting_list.append(self.para_first_line_indent+self.para_first_line_indent_size+'磅')
            if self.para_space_before !='': setting_list.append('段前'+self.para_space_before+'磅')
            if self.para_space_after !='':  setting_list.append('段后'+self.para_space_before+'磅')
            if self.para_line_spacing_rule !='': 
                if self.para_line_spacing_rule in ('单倍行距','双倍行距','1.5倍行距'):
                    setting_list.append(self.para_line_spacing_rule)
                else:
                    setting_list.append(self.para_line_spacing+'倍行距')
            if self.para_firstchardropcap !='' and self.para_firstchardropcaplines !='': 
                setting_list.append('首字'+self.para_firstchardropcap+self.para_firstchardropcaplines+'磅')
            if self.page_break_before==True: setting_list.append('段前分页')
            if self.keep_with_next==True: setting_list.append('与下段同页')
            if self.keep_together==True: setting_list.append('段中不分页')
            if self.window_control==True: setting_list.append('孤行控制')

            return '段落格式设置成'+'、'.join(setting_list)
        else:
            return ''
    paraformat_description.short_description = '段落设置描述'

    def style_description(self):
        if self.style_op:
            style_des = ''
            style_des_add = []
            if self.style_name in ['新样式1', '新样式2']:
                style_des = '创建并应用“'+self.style_name+'”'
            else:
                style_des = '应用“'+self.style_name+'”'

            font_setting_list=[]
            if self.style_font_name_chinese !='': font_setting_list.append('中文'+self.style_font_name_chinese)
            if self.style_font_name_ascii !='':  font_setting_list.append('西文'+self.style_font_name_ascii)
            if self.style_font_size !='': font_setting_list.append('字号'+self.style_font_size)
            if self.style_font_color !='': font_setting_list.append(self.style_font_color)
            if self.style_font_bold==True: font_setting_list.append('粗体')
            if self.style_font_italic==True: font_setting_list.append('斜体')
            if self.style_font_underline !='': font_setting_list.append(self.style_font_underline)
            if len(font_setting_list)>0:
                style_des_add.append('其字体设置成'+'、'.join(font_setting_list))

            para_setting_list=[]
            if self.style_para_alignment !='': para_setting_list.append(self.style_para_alignment)
            if self.style_para_left_indent !='': para_setting_list.append('左缩进'+self.style_para_left_indent+'磅')
            if self.style_para_right_indent !='': para_setting_list.append('右缩进'+self.style_para_right_indent+'磅')
            if self.style_para_first_line_indent !='' and \
               self.style_para_first_line_indent_size !='': 
                para_setting_list.append(self.style_para_first_line_indent+self.style_para_first_line_indent_size+'磅')
            if self.style_para_space_before !='': para_setting_list.append('段前'+self.style_para_space_before+'磅')
            if self.style_para_space_after !='':  para_setting_list.append('段后'+self.style_para_space_before+'磅')
            if self.style_para_line_spacing_rule !='': 
                if self.style_para_line_spacing_rule in ('单倍行距','双倍行距','1.5倍行距'):
                    para_setting_list.append(self.style_para_line_spacing_rule)
                else:
                    para_setting_list.append(self.style_para_line_spacing+'倍行距')
            if self.style_para_firstchardropcap !='' and self.style_para_firstchardropcaplines !='': 
                para_setting_list.append('首字'+self.style_para_firstchardropcap+self.style_para_firstchardropcaplines+'磅')
            if self.style_page_break_before==True: para_setting_list.append('段前分页')
            if self.style_keep_with_next==True: para_setting_list.append('与下段同页')
            if self.style_keep_together==True: para_setting_list.append('段中不分页')
            if self.style_window_control==True: para_setting_list.append('孤行控制')

            if len(para_setting_list)>0:
                style_des_add.append('其段落格式设置成'+'、'.join(para_setting_list))
            return style_des+'('+'，'.join(style_des_add)+')'
        else:
            return ''
    style_description.short_description = '样式设置描述'

    def clean(self):
        if not (self.char_edit_op or self.font_op or self.paraformat_op or self.style_op or self.image_op):
            raise ValidationError(_('至少选择一个操作考查'))

        if (self.font_op or self.paraformat_op) and self.style_op:
            raise ValidationError(_('样式和单独的字体和段落格式不应同时设置'))

        error_dict = {}

        if self.char_edit_op and (self.char_edit_origin==''):
            error_dict['char_edit_origin'] = _('不能为空')
        if self.char_edit_op and (self.char_edit_replace==''):
            error_dict['char_edit_replace'] = _('不能为空')

        if self.font_op and \
        (self.font_name_ascii=='' and 
        self.font_name_chinese=='' and 
        self.font_size=='' and 
        self.font_underline=='' and 
        self.font_color=='' and
        self.font_bold==False and
        self.font_italic==False):
            error_dict['font_name_chinese'] = _('至少设定一个字体相关设置')
            error_dict['font_name_ascii'] = _('')
            error_dict['font_size'] = _('')
            error_dict['font_underline'] = _('')
            error_dict['font_color'] = _('')

        if self.paraformat_op and \
        (self.para_alignment=='' and 
        self.para_left_indent=='' and 
        self.para_right_indent=='' and 
        self.para_first_line_indent=='' and 
        self.para_first_line_indent_size=='' and 
        self.para_space_before=='' and 
        self.para_space_after=='' and 
        self.para_line_spacing_rule=='' and 
        self.para_line_spacing=='' and 
        self.para_firstchardropcap=='' and 
        self.para_firstchardropcaplines=='' and 
        self.page_break_before==False and
        self.keep_with_next==False and
        self.keep_together==False and
        self.window_control==False):
            error_dict['para_alignment'] = _('至少选择一个段落格式相关设置')
            error_dict['para_left_indent'] = _('')
            error_dict['para_right_indent'] = _('')
            error_dict['para_first_line_indent'] = _('')
            error_dict['para_first_line_indent_size'] = _('')
            error_dict['para_space_before'] = _('')
            error_dict['para_space_after'] = _('')
            error_dict['para_line_spacing_rule'] = _('')
            error_dict['para_line_spacing'] = _('')
            error_dict['para_firstchardropcap'] = _('')
            error_dict['para_firstchardropcaplines'] = _('')

        if self.paraformat_op and (self.para_first_line_indent=='' and self.para_first_line_indent_size!=''):
            error_dict['para_first_line_indent'] = _('不能为空')
            error_dict['para_first_line_indent_size'] = _('*')
        if self.paraformat_op and (self.para_first_line_indent !='' and self.para_first_line_indent_size==''):
            error_dict['para_first_line_indent'] = _('*')
            error_dict['para_first_line_indent_size'] = _('不能为空')

        if self.paraformat_op and (self.para_line_spacing_rule=='' and self.para_line_spacing!=''):
            error_dict['para_line_spacing_rule'] = _('不能为空')
            error_dict['para_line_spacing'] = _('*')
        if self.paraformat_op and (self.para_line_spacing_rule !='' and self.para_line_spacing==''):
            error_dict['para_line_spacing_rule'] = _('*')
            error_dict['para_line_spacing'] = _('不能为空')

        if self.paraformat_op and (self.para_firstchardropcap=='' and self.para_firstchardropcaplines!=''):
            error_dict['para_firstchardropcap'] = _('不能为空')
            error_dict['para_firstchardropcaplines'] = _('*')
        if self.paraformat_op and (self.para_firstchardropcap !='' and self.para_firstchardropcaplines==''):
            error_dict['para_firstchardropcap'] = _('*')
            error_dict['para_firstchardropcaplines'] = _('不能为空')


        if self.style_op and self.style_name=='':
            error_dict['style_name'] = _('内容不能为空')

        if self.style_op and self.style_name in ['新样式1', '新样式2'] and \
               (self.style_font_name_ascii=='' and 
                self.style_font_name_chinese=='' and 
                self.style_font_size=='' and 
                self.style_font_underline=='' and 
                self.style_font_color=='' and
                self.style_font_bold==False and
                self.style_font_italic==False and
                self.style_para_alignment=='' and 
                self.style_para_left_indent=='' and 
                self.style_para_right_indent=='' and 
                self.style_para_first_line_indent=='' and 
                self.style_para_first_line_indent_size=='' and 
                self.style_para_space_before=='' and 
                self.style_para_space_after=='' and 
                self.style_para_line_spacing_rule=='' and 
                self.style_para_line_spacing=='' and 
                self.style_para_firstchardropcap=='' and 
                self.style_para_firstchardropcaplines=='' and 
                self.style_page_break_before==False and
                self.style_keep_with_next==False and
                self.style_keep_together==False and
                self.style_window_control==False
                ):
            error_dict['style_name'] = _('至少为新样式设定一个具体设置')
            error_dict['style_font_name_chinese'] = _('')
            error_dict['style_font_name_ascii'] = _('')
            error_dict['style_font_size'] = _('')
            error_dict['style_font_underline'] = _('')
            error_dict['style_font_color'] = _('')
            error_dict['style_para_alignment'] = _('')
            error_dict['style_para_left_indent'] = _('')
            error_dict['style_para_right_indent'] = _('')
            error_dict['style_para_first_line_indent'] = _('')
            error_dict['style_para_first_line_indent_size'] = _('')
            error_dict['style_para_space_before'] = _('')
            error_dict['style_para_space_after'] = _('')
            error_dict['style_para_line_spacing_rule'] = _('')
            error_dict['style_para_line_spacing'] = _('')
            error_dict['style_para_firstchardropcap'] = _('')
            error_dict['style_para_firstchardropcaplines'] = _('')

        if self.style_op and \
        (self.style_para_first_line_indent=='' and 
         self.style_para_first_line_indent_size!=''):
            error_dict['style_para_first_line_indent'] = _('不能为空')
            error_dict['style_para_first_line_indent_size'] = _('*')

        if self.style_op and \
            (self.style_para_first_line_indent !='' and 
             self.style_para_first_line_indent_size==''):
            error_dict['style_para_first_line_indent'] = _('*')
            error_dict['style_para_first_line_indent_size'] = _('不能为空')

        if self.style_op and (self.style_para_line_spacing_rule=='' and self.style_para_line_spacing!=''):
            error_dict['style_para_line_spacing'] = _('*')
            error_dict['style_para_line_spacing_rule'] = _('不能为空')
        if self.style_op and (self.style_para_line_spacing_rule !='' and self.style_para_line_spacing==''):
            error_dict['style_para_line_spacing'] = _('不能为空')
            error_dict['style_para_line_spacing_rule'] = _('*')

        if self.style_op and (self.style_para_firstchardropcap=='' and self.style_para_firstchardropcaplines!=''):
            error_dict['style_para_firstchardropcap'] = _('不能为空')
            error_dict['style_para_firstchardropcaplines'] = _('*')
        if self.style_op and (self.style_para_firstchardropcap !='' and self.style_para_firstchardropcaplines==''):
            error_dict['style_para_firstchardropcap'] = _('*')
            error_dict['style_para_firstchardropcaplines'] = _('不能为空')

        # print('self.upload_image_file',  self.upload_image_file.name)
        if self.image_op and self.upload_image_file.name=='':
            error_dict['upload_image_file'] = _('必须上传图片(jpg,bmp,png)')
        
        if len(error_dict)>0:
            raise ValidationError(error_dict)


    word_question = models.ForeignKey(
        WordQuestion,
        on_delete=models.CASCADE, blank=True, default='',
        verbose_name='word操作大题'
    )

    para_text = models.TextField('要考查的段落内容')

    ############## 文字查找替换
    char_edit_op = models.BooleanField('是否考查文字查找替换？', default=False)
    char_edit_origin = models.CharField('原词', max_length=200, blank=True, default='')
    char_edit_replace = models.CharField('替换为', max_length=200, blank=True, default='')

    ############## 字体设置
    font_op = models.BooleanField('是否考查字体设置？', default=False)
    font_name_ascii = models.CharField('英文字体', choices=FONT_NAME_ASCII_CHOICES, max_length=200, blank=True, default='') 
    font_name_chinese = models.CharField('中文字体', choices=FONT_NAME_CHINESE_CHOICES, max_length=200, blank=True, default='')
    font_size = models.CharField('字号', choices=FONT_SIZE_CHOICES, max_length=200, blank=True, default='')
    font_bold = models.BooleanField('粗体', blank=True, default='')
    font_italic = models.BooleanField('斜体', blank=True, default='')
    font_underline = models.CharField('下划线', choices=FONT_UNDERLINE_CHOICES, max_length=200, blank=True, default='')
    font_color = models.CharField('字体颜色', choices=FONT_COLOR_CHOICES, max_length=200, blank=True, default='')

    ############## 段落格式设置
    paraformat_op = models.BooleanField('是否考查段落格式设置？', default=False)
    para_alignment = models.CharField('段落对齐', choices=PARA_ALIGNMENT_CHOICES, max_length=200, blank=True, default='')
    para_left_indent = models.CharField('左侧缩进(磅)', choices=INDENT_NUM_CHOICES, max_length=200, blank=True, default='')
    para_right_indent = models.CharField('右侧缩进(磅)', choices=INDENT_NUM_CHOICES, max_length=200, blank=True, default='')
    para_first_line_indent = models.CharField('首行缩进', choices=PARA_FIRST_LINE_INDENT_CHOICES, max_length=200, blank=True, default='')
    para_first_line_indent_size = models.CharField('首行缩进距离(磅)', choices=INDENT_NUM_CHOICES, max_length=200, blank=True, default='')

    para_space_before = models.CharField('段前间距(磅)',  choices=INDENT_NUM_CHOICES, max_length=200, blank=True, default='')
    para_space_after = models.CharField('段后间距(磅)',  choices=INDENT_NUM_CHOICES, max_length=200, blank=True, default='')
    para_line_spacing_rule = models.CharField('行距规则', choices=PARA_LINE_SPACING_RULE_CHOICES, max_length=200, blank=True, default='')
    para_line_spacing = models.CharField('行距(行)',  choices=LINE_NUM_CHOICES, max_length=200, blank=True, default='')

    para_firstchardropcap = models.CharField('首字下沉', choices=PARA_FIRSTCHARDROPCAP_CHOICES, max_length=200, blank=True, default='')
    para_firstchardropcaplines = models.CharField('下沉(行)',  choices=LINE_NUM_CHOICES, max_length=200, blank=True, default='')

    page_break_before = models.BooleanField('段前分页', default=False)
    keep_with_next = models.BooleanField('与下段同页', default=False)
    keep_together = models.BooleanField('段中不分页', default=False)
    window_control = models.BooleanField('孤行控制', default=False)

    ############## 样式设置
    style_op = models.BooleanField('是否考查样式设置？', default=False)
    style_name = models.CharField('样式名称', choices=STYLE_NAME_CHOICES, max_length=200, blank=True, default='') 
    style_font_name_ascii = models.CharField('英文字体', choices=FONT_NAME_ASCII_CHOICES, max_length=200, blank=True, default='') 
    style_font_name_chinese = models.CharField('中文字体', choices=FONT_NAME_CHINESE_CHOICES, max_length=200, blank=True, default='')
    style_font_size = models.CharField('字号', choices=FONT_SIZE_CHOICES, max_length=200, blank=True, default='')
    style_font_bold = models.BooleanField('粗体', default=False)
    style_font_italic = models.BooleanField('斜体', default=False)
    style_font_underline = models.CharField('下划线', choices=FONT_UNDERLINE_CHOICES, max_length=200, blank=True, default='')
    style_font_color = models.CharField('字体颜色', choices=FONT_COLOR_CHOICES, max_length=200, blank=True, default='')

    style_para_alignment = models.CharField('段落对齐', choices=PARA_ALIGNMENT_CHOICES, max_length=200, blank=True, default='')
    style_para_left_indent = models.CharField('左侧缩进(磅)',  choices=INDENT_NUM_CHOICES, max_length=200, blank=True, default='')
    style_para_right_indent = models.CharField('右侧缩进(磅)',  choices=INDENT_NUM_CHOICES, max_length=200, blank=True, default='')
    style_para_first_line_indent = models.CharField('首行缩进', choices=PARA_FIRST_LINE_INDENT_CHOICES, max_length=200, blank=True, default='')
    style_para_first_line_indent_size = models.CharField('首行缩进距离(磅)',  choices=INDENT_NUM_CHOICES, max_length=200, blank=True, default='')

    style_para_space_before = models.CharField('段前间距(磅)',   choices=INDENT_NUM_CHOICES, max_length=200, blank=True, default='')
    style_para_space_after = models.CharField('段后间距(磅)',   choices=INDENT_NUM_CHOICES, max_length=200, blank=True, default='')
    style_para_line_spacing_rule = models.CharField('行距规则', choices=PARA_LINE_SPACING_RULE_CHOICES, max_length=200, blank=True, default='')
    style_para_line_spacing = models.CharField('行距(行)',   choices=LINE_NUM_CHOICES, max_length=200, blank=True, default='')

    style_para_firstchardropcap = models.CharField('首字下沉', choices=PARA_FIRSTCHARDROPCAP_CHOICES, max_length=200, blank=True, default='')
    style_para_firstchardropcaplines = models.CharField('下沉(行)',   choices=LINE_NUM_CHOICES, max_length=200, blank=True, default='')

    style_page_break_before = models.BooleanField('段前分页', default=False)
    style_keep_with_next = models.BooleanField('与下段同页', default=False)
    style_keep_together = models.BooleanField('段中不分页', default=False)
    style_window_control = models.BooleanField('孤行控制', default=False)

    ############## 图片插入
    image_op = models.BooleanField('是否考查图片插入？', default=False)
    image_position_style = models.CharField('位置类型', choices=IMAGE_POSITION_STYLE_CHOICES, max_length=200, default='嵌入文本行中')
    image_width = models.CharField('图像宽(厘米)',   choices=INDENT_NUM_CHOICES, max_length=200, blank=True, default='')
    image_height = models.CharField('图像高(厘米)',   choices=INDENT_NUM_CHOICES, max_length=200, blank=True, default='')
    upload_image_file = models.FileField(upload_to='uploads_image/', null=True, blank=True, 
    validators=[validate_image], verbose_name='上传图片')

def validate_operation_list(value):
    operation_list = value.all()
    # if len(operation_list)<5:
    raise ValidationError(
            _('操作题数量不足5个'),
            params={'value': value.id},
        )

    # def save(self, *args, **kwargs):
    #     op_list = [x for x in  self.word_operation_list.all()]
    #     print(len(op_list))
    #     if len(op_list) < 5 :
            
    #         return # Yoko shall never have her own blog!
    #     else:
    #         super().save(*args, **kwargs)

    # def clean(self):

    #     op_list = [x for x in  self.word_operation_list.all()]
    #     op_err = [self.upload_docx.id==x.upload_docx.id  for x in  self.word_operation_list.all()]

    #     print(len(op_list))
    #     # if len(op_list) != 5:
    #         # raise ValidationError({'word_operation_list':_('Word操作题个数不等于5')})

    #     for i in range(len(op_err)):
    #         if(op_err[i]==False): raise ValidationError({'word_operation_list':_('第'+str(i+1)+'个操作题的Word文件不等于此处上传的Word文件')})
