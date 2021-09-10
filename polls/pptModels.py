import os
import re
import shutil
import zipfile
from pathlib import Path
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.html import format_html, format_html_join


BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT  = BASE_DIR / 'media'


def find_2rd_item_in_maps(item, maps):
    for item1, item2 in maps:
        if item1 == item: 
            return item2

def validate_pptx(value):
    extension = value.name.split('.')[-1]
    if extension != 'pptx':
        raise ValidationError(
            _(value.name+'不是ppt文件(.pptx)'),
            params={'value': value.name},
        )


Standard_Color_Choices = [
    ('C00000','深红'),
    ('FF0000','红色'),
    ('FFC000','橙色'),
    ('FFFF00','黄色'),
    ('92D050','浅绿'),
    ('00B050','绿色'),
    ('00B0F0','浅蓝'),
    ('0070C0','蓝色'),
    ('002060','深蓝'),
    ('7030A0','紫色'),
]


Slide_Layout_Names = [
    ("标题幻灯片", "标题幻灯片"),
    ("标题和内容", "标题和内容"),
    ("节标题", "节标题"),
    ("两栏内容", "两栏内容"),
    ("比较", "比较"),
    ("仅标题", "仅标题"),
    # ("空白", "空白"),
    ("内容与标题", "内容与标题"),
    ("图片与标题", "图片与标题"),
    # ("标题和竖排文字", "标题和竖排文字"),
    # ("竖排标题与文本", "竖排标题与文本"),
]

Slide_Names = [
    ('0','第一页幻灯片'),
    ('1','第二页幻灯片'),
    ('2','第三页幻灯片'),
    ('3','第四页幻灯片'),
]

Background_Types = [
    ('SOLID (1)','纯色填充'),
    ('PATTERNED (2)','图案填充'),
]

Shape_Names = [
    ('标题','标题'),
    ('副标题','副标题'),
    ('内容','内容'),
    ('左侧内容','左侧内容'),
    ('右侧内容','右侧内容'),
]


FONT_NAME_CHOICES = [
    ('Arial Black', 'Arial Black'),
    ('Bahnschrift', 'Bahnschrift'),
    ('黑体', '黑体'),
    ('华文仿宋', '华文仿宋'),
    ('楷体', '楷体'),
    ('幼圆', '幼圆'),
    ('微软雅黑', '微软雅黑'),
    ('隶书', '隶书'),
]


FONT_SIZE_CHOICES = [
    ('26','26' ),
    ('36','36' ),
    ('48','48' ),
    ('72','72' ),
]

####################### PPT 题目 #########################
class PPTQuestion(models.Model):

    def __str__(self):
        return 'PPT操作' + str(self.id) 

    class Meta:
        db_table = 'ppt_table'  
        verbose_name_plural = '题目-PPT操作'  
        verbose_name = '题目-PPT操作' 

    def base_path_(self):
        return os.path.join(MEDIA_ROOT, 'upload_pptx', str(self.id))

    # 题目内容
    def question_content(self):
        pre_description = 'ppt.pptx:\n'
        result_list = []

        return format_html(pre_description) + \
                format_html("<ol>") + \
                format_html_join(
                '\n', '<li style="color:black;">{}</li>',
                ((x,) for x in result_list)
                ) \
                + format_html("</ol>")
    question_content.short_description = '题目内容'


    def file_path_(self):
        if self.upload_pptx:
            answer_file_path = self.upload_pptx.path
        else:
            answer_file_path = ''
        return answer_file_path
    file_path_.short_description = '文件地址'


    def score_(self, answer_file_path):
        result_list = []
        ## check the files
        # if answer_file_path and os.path.exists(answer_file_path):
        #     try:
        #         wb = load_workbook(answer_file_path)
        #         ws = wb.active 
        #     except:
        #         return ['文件打开异常']

        #     if self.rename_sheet_op:
        #         result = 'rename_sheet::'
        #         for name in wb.sheetnames:
        #             if name == self.new_sheet_name: 
        #                 result = result+name
        #                 break
        #         result_list.append(result)
        # else:
        #     result_list.append('Nothing to score')
        return result_list


    def test_(self):
        ## only for development
        if self.upload_pptx:
            answer_file_path = self.upload_pptx.path
        else:
            answer_file_path = ''
        return format_html("<ol>") + \
                format_html_join(
                '\n', '<li style="color:black;">{}</li>',
                ((x,) for x in self.score_(answer_file_path))
                ) \
                + format_html("</ol>")
    test_.short_description = '测试结果'


    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)  
        

    def clean(self):
        error_dict = {}

        # if self.rename_sheet_op:
        #     clean_empty_item(self.new_sheet_name, error_dict, 'new_sheet_name')

        if len(error_dict)>0:
            raise ValidationError(error_dict)


    #########
    pub_date = models.DateTimeField('创建时间', default=timezone.now)

    ## 
    upload_pptx = models.FileField(verbose_name='上传PPT文件[.pptx]', upload_to='upload_pptx/', 
         validators=[validate_pptx], null=True)

    # 选择版式
    # 题目示例：第X页幻灯片的版式改为“XXXX”。
    slide_layout_op = models.BooleanField('考查版式设置？', default=False)
    slide_layout_target_slide = models.CharField('要操作的幻灯片', choices=Slide_Names ,max_length=50, blank=True, default='0')
    slide_layout_name = models.CharField('版式名称', choices=Slide_Layout_Names ,max_length=50, blank=True, default='数据汇总表')


    # 修改文字内容
    text_op = models.BooleanField('考查修改文字内容？', default=False)
    text_target_slide = models.CharField('要操作的幻灯片', choices=Slide_Names ,max_length=50, blank=True, default='0')
    text_target_shape_1 = models.CharField('区域1', choices=Shape_Names ,max_length=50, blank=True, default='0')
    text_target_content_1 = models.TextField('区域1内容',  blank=True, default='大标题')
    text_target_shape_2 = models.CharField('区域2', choices=Shape_Names ,max_length=50, blank=True, default='0')
    text_target_content_2 = models.TextField('区域2内容',  blank=True, default='小标题')


    # 修改字体格式
    font_op = models.BooleanField('考查修改字体格式？', default=False)
    font_target_slide = models.CharField('要操作的幻灯片', choices=Slide_Names ,max_length=50, blank=True, default='0')
    font_target_shape = models.CharField('文字区域', choices=Shape_Names ,max_length=50, blank=True, default='0')
    font_target_content = models.TextField('文字内容', blank=True, default='')
    font_name = models.CharField('字体', choices=FONT_NAME_CHOICES ,max_length=50, blank=True,)
    font_size = models.CharField('字号[磅]', choices=FONT_SIZE_CHOICES ,max_length=50, blank=True,)
    font_color = models.CharField('颜色', choices=Standard_Color_Choices ,max_length=50, blank=True,)
    font_bold = models.BooleanField('是否粗体？', default=False)
    font_italic = models.BooleanField('是否斜体？', default=False)


    # 设置幻灯片背景格式
    # 题目示例：第X页幻灯片设置背景格式为"XX",标准色“XXXX”。
    slide_background_op = models.BooleanField('考查幻灯片背景格式？', default=False)
    slide_background_slide = models.CharField('要操作的幻灯片', choices=Slide_Names, max_length=50, blank=True, default='0')
    slide_background_type = models.CharField('背景类型',  choices=Background_Types, max_length=50, blank=True, default='')
    slide_background_fore = models.CharField('前景颜色',  choices=Standard_Color_Choices, max_length=50, blank=True,)
    slide_background_back = models.CharField('背景颜色',  choices=Standard_Color_Choices, max_length=50, blank=True,)


    # 添加备注
    # 题目示例：第X页幻灯片添加备注，内容为“XXXX”。
    notes_slide_op = models.BooleanField('考查添加备注页？', default=False)
    notes_slide_target_slide = models.CharField('要操作的幻灯片', choices=Slide_Names ,max_length=50, blank=True, default='0')
    notes_slide_content = models.TextField('备注内容',  blank=True, default='备注内容1')

    # 添加表格及内容

