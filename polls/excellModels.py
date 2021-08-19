import os
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html, format_html_join

import re
import shutil
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT  = BASE_DIR / 'media'

New_Folder_Name_Choice = [
    ('new12', 'new12'),
]

def is_cell_range_legal(p):
    reg = re.compile('([A-Z])(\d+):([A-Z])(\d+)')
    result = reg.match(p)
    if result is None:
        return False, '地址应该符合格式 [大写字母][数字]:[大写字母][数字]，比如A2:B5'
    else:
        p1,p2,p3,p4 = result.group(1), int(result.group(2)), result.group(3), int(result.group(4))
        if p1>p3 or p2>p4 or (p1==p3 and p2==p4):
            return False, '[起始地址] 应当小于 [结束地址]，比如A2:B5'
    
    return True, ''


####################### Excel 题目 #########################
class ExcelQuestion(models.Model):
    # 控制 表项显示文字，默认按 类名object（n）显示
    def __str__(self):
        return 'Excel操作题' + str(self.id) 

    class Meta:
        verbose_name_plural = 'Excel操作题'  
        verbose_name = 'Excel操作题' 

    #包含小题数量
    def question_num(self):
        return 5
    question_num.short_description='小题数量'

    def base_path_(self):
        return os.path.join(MEDIA_ROOT, 'system_operation_files',str(self.id))

    #题目内容
    def question_content(self):
        result_list = []
        result_list.append('在考生文件夹下创建文件夹'+'，并在此文件夹中新建文件'+'.')

        return format_html("<ol>") + \
                format_html_join(
                '\n', '<li style="color:black;">{}</li>',
                ((x,) for x in result_list)
                ) \
                + format_html("</ol>")
    question_content.short_description = '题目内容'

    def score_(self, answer_folder_path):
        result_list = []
        ## check the files
        if answer_folder_path and os.path.exists(answer_folder_path):
            result_list.append('Nothing to score')
        return result_list

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  
        
    def clean(self):
        error_dict = {}

        if self.rename_sheet_op and self.new_sheet_name=='':
            error_dict['new_sheet_name'] = _('必须填写工作表新名称')

        if self.merge_cell_op:
            if self.merge_cell_position=='':
                error_dict['merge_cell_position'] = _('必须填写单元格区域')
            else:
                is_legal, errors = is_cell_range_legal(self.merge_cell_position)
                if not is_legal:
                    error_dict['merge_cell_position'] = _(errors)

        
        if len(error_dict)>0:
            raise ValidationError(error_dict)

    # 重命名工作表Sheet1
    # 题目示例：将Sheet1重命名new_sheet_name
    rename_sheet_op = models.BooleanField('考查重命名工作表？', default=False)
    new_sheet_name = models.CharField('工作表新名称', max_length=50, blank=True, default='数据汇总表')

    # 合并单元格
    # 题目示例：将工作表Start:End单元格合并为一个单元格，内容水平居中
    merge_cell_op = models.BooleanField('考查合并单元格？', default=False)
    merge_cell_position = models.CharField('合并单元格区域[Start:End]', max_length=20, blank=True, default='A1:F1')

    