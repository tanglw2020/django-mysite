import os
import re
import shutil
import zipfile
from pathlib import Path
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
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


Standard_Color_Maps = [
    ('FFC00000','深红'),
    ('FFFF0000','红色'),
    ('FFFFC000','橙色'),
    ('FFFFFF00','黄色'),
    ('FF92D050','浅绿'),
    ('FF00B050','绿色'),
    ('FF00B0F0','浅蓝'),
    ('FF0070C0','蓝色'),
    ('FF002060','深蓝'),
    ('FF7030A0','紫色'),
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
    pub_date = models.DateTimeField('创建时间', null=True, blank=True, )

    ## 
    upload_pptx = models.FileField(verbose_name='上传PPT文件', upload_to='upload_pptx/', 
        null=True, blank=True, validators=[validate_pptx])

    # 重命名工作表Sheet1
    # 题目示例：将Sheet1重命名new_sheet_name
    # rename_sheet_op = models.BooleanField('考查重命名工作表？', default=False)
    # new_sheet_name = models.CharField('工作表新名称', max_length=50, blank=True, default='数据汇总表')
