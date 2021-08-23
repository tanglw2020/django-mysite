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

## 套用套用表格格式
Table_Style_Maps = [
    ('TableStyleLight9', '蓝色,表样式浅色9'),
    ('TableStyleLight12','金色,表样式浅色12'),
    ('TableStyleMedium4','白色,表样式中等深浅4'),
    ('TableStyleMedium8','浅灰色,表样式中等深浅8'),
    ('TableStyleDark3','褐色,表样式深色3'),
    ('TableStyleDark6','深蓝,表样式深色6'),
]

## 图表类型
Chart_Type_Choice = [
    ('barChart', '柱形图'),
    ('lineChart', '折线图'),
    ('pieChart', '饼图'),
    ('areaChart', '面积图'),
    ('scatterChart', 'XY散点图'),
    ('radarChart', '雷达图'),
]

Sort_Type_Choice = [
    ('升序','升序'),
    ('降序','降序'),
]


## conditional_formatting
## ["name", "type", "operator", "bottom", "percent", "aboveAverage"]
# {
# "greaterThan":["cellIs", "greaterThan", "None", "None", "None"],
# "lessThan":["cellIs", "lessThan", "None", "None", "None"],
# "equal":["cellIs", "equal", "None", "None", "None"],
# "duplicateValues":["duplicateValues", "None", "None", "None", "None"],
# "top10":["top10", "None", "None", "None", "None"],
# "top10p":["top10", "None", "None", "True", "None"],
# "tail10":["top10", "None", "True", "None", "None"],
# "tail10p":["top10", "None", "True", "True", "None"],
# "aboveAverage":["aboveAverage", "None", "None", "None", "None"],
# "belowAverage":["aboveAverage", "None", "None", "None", "False"] 
# }
Conditional_Formatting_Type_Choice = [
    ('greaterThan','突出显示单元格规则大于'),
    ('lessThan','突出显示单元格规则小于'),
    ('equal','突出显示单元格规则等于'),
    ('duplicateValues','突出显示单元格规则重复值'),
    ('top10','最前最后规则前10项'),
    ('top10p','最前最后规则前10%'),
    ('tail10','最前最后规则后10项'),
    ('tail10p','最前最后规则后10%'),
    ('aboveAverage','最前最后规则高于平均值'),
    ('belowAverage','最前最后规则低于平均值'),
]

Conditional_Formatting_Coloring_Choice = [
    ('浅红填充色深红色文本','浅红填充色深红色文本'), 
    ('黄填充色深黄色文本','黄填充色深黄色文本'), 
    ('绿填充色深绿色文本','绿填充色深绿色文本'), 
    ('红色边框','红色边框'), 
]

def is_cell_range_legal(p):
    reg = re.compile('([A-Z])(\d+):([A-Z])(\d+)')
    result = reg.match(p)
    if result is None:
        return False, '地址格式 [大写字母][数字]:[大写字母][数字]，比如A2:B5'
    else:
        p1,p2,p3,p4 = result.group(1), int(result.group(2)), result.group(3), int(result.group(4))
        if p1>p3 or p2>p4 or (p1==p3 and p2==p4):
            return False, '[起始地址] 应当小于 [结束地址]，比如A2:B5'
    
    return True, ''


####################### Excel 题目 #########################
class ExcelQuestion(models.Model):
    # 控制 表项显示文字，默认按类名object（n）显示
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
            error_dict['new_sheet_name'] = _('不能为空')

        if self.merge_cell_op:
            if self.merge_cell_position=='':
                error_dict['merge_cell_position'] = _('不能为空')
            else:
                is_legal, errors = is_cell_range_legal(self.merge_cell_position)
                if not is_legal:
                    error_dict['merge_cell_position'] = _(errors)

        if self.color_cell_op:
            if self.color_cell_position=='':
                error_dict['color_cell_position'] = _('不能为空')
            else:
                is_legal, errors = is_cell_range_legal(self.color_cell_position)
                if not is_legal:
                    error_dict['color_cell_position'] = _(errors)

            if self.color_cell_font == '':
                error_dict['color_cell_font'] = _('必须选择一种颜色')
            if self.color_cell_filling == '':
                error_dict['color_cell_filling'] = _('必须选择一种颜色')
            if self.color_cell_font and self.color_cell_font==self.color_cell_filling:
                error_dict['color_cell_font'] = _('文字和填充不能用相同颜色')
                error_dict['color_cell_filling'] = _('文字和填充不能用相同颜色')

        if self.chart_op:
            if self.chart_data_name == '': error_dict['chart_data_name'] = _('不能为空')
            if self.chart_type == '': error_dict['chart_type'] = _('不能为空')
            if self.chart_tiltle == '': error_dict['chart_tiltle'] = _('不能为空')

            if self.chart_data_position == '':
                error_dict['chart_data_position'] = _('不能为空')
            else:
                is_legal, errors = is_cell_range_legal(self.chart_data_position)
                if not is_legal:
                    error_dict['chart_data_position'] = _(errors)
                
            if self.chart_position == '':
                error_dict['chart_position'] = _('不能为空')
            else:
                is_legal, errors = is_cell_range_legal(self.chart_position)
                if not is_legal:
                    error_dict['chart_position'] = _(errors)

        if self.sort_op:
            if self.keyword_1 == '': error_dict['keyword_1'] = _('不能为空')
            if self.sort_type_1 == '': error_dict['sort_type_1'] = _('不能为空')
            if self.sort_data_result_1 == '': error_dict['sort_data_result_1'] = _('不能为空')
            if self.keyword_2 == '': error_dict['keyword_2'] = _('不能为空')
            if self.sort_type_2 == '': error_dict['sort_type_2'] = _('不能为空')
            if self.sort_data_result_2 == '': error_dict['sort_data_result_2'] = _('不能为空')
            
            if self.sort_data_position_1 == '': 
                error_dict['sort_data_position_1'] = _('不能为空')
            else:
                is_legal, errors = is_cell_range_legal(self.sort_data_position_1)
                if not is_legal:
                    error_dict['sort_data_position_1'] = _(errors)

            if self.sort_data_position_2 == '': 
                error_dict['sort_data_position_2'] = _('不能为空')
            else:
                is_legal, errors = is_cell_range_legal(self.sort_data_position_2)
                if not is_legal:
                    error_dict['sort_data_position_2'] = _(errors)

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

    # 设置单元格颜色和填充色
    # 题目示例：将工作表Start:End单元格文字设置成标准色X，填色设置成标准色Y
    color_cell_op = models.BooleanField('考查单元格颜色设置？', default=False)
    color_cell_position = models.CharField('单元格区域[Start:End]', max_length=20, blank=True, default='A2:A20')
    color_cell_font = models.CharField('文字颜色', choices=Standard_Color_Maps, max_length=20, blank=True, default='') 
    color_cell_filling = models.CharField('填充颜色', choices=Standard_Color_Maps, max_length=20, blank=True, default='') 


    # 设置单元格 条件格式
    # 题目示例：对工作表Start:End单元格区域应用条件格式
    conditional_formatting_op = models.BooleanField('考查单元格条件格式设置？', default=False)
    conditional_formatting_position = models.CharField('单元格区域[Start:End]', max_length=20, blank=True, default='A2:A20')
    conditional_formatting_type = models.CharField('条件类型', choices=Conditional_Formatting_Type_Choice, max_length=50, blank=True, default='')
    conditional_formatting_param = models.CharField('条件格式参数', max_length=10, blank=True, default='5')
    conditional_formatting_coloring = models.CharField('颜色选项', choices=Conditional_Formatting_Coloring_Choice, max_length=50, blank=True, default='')


    # 单元格 套用表格格式
    # 题目示例：将工作表Start:End单元格套用表格格式
    table_style_op = models.BooleanField('考查单元格套用表格格式？', default=False)
    table_style_position = models.CharField('单元格区域[Start:End]', max_length=20, blank=True, default='A2:A20')
    table_style_choice = models.CharField('套用表格格式', choices=Table_Style_Maps, max_length=20, blank=True, default='') 


    # 插入图表
    # 题目示例：为工作表数据列X建立曲线图表，
    # 图表标题为Y，将图表插入表格区域Z
    chart_op = models.BooleanField('考查插入图表？', default=False)
    chart_data_name = models.CharField('数据列名称', max_length=20, blank=True, default='平均升学率')
    chart_data_position = models.CharField('数据列位置', max_length=20, blank=True, default='F2:F50')
    chart_type = models.CharField('图表类型', choices=Chart_Type_Choice, max_length=20, blank=True, default='') 
    chart_tiltle = models.CharField('图表标题', max_length=20, blank=True, default='曲线图') 
    chart_position = models.CharField('图表插入区域[Start:End]', max_length=20, blank=True, default='G2:K20')

    # 双关键字排序
    # 题目示例：将表格按关键字1升序、关键字2降序排序
    sort_op = models.BooleanField('考查排序？', default=False)
    keyword_1 = models.CharField('主关键字', max_length=20, blank=True, default='')
    sort_type_1 = models.CharField('主关键字次序', choices=Sort_Type_Choice, max_length=20, blank=True, default='') 
    sort_data_position_1 = models.CharField('主关键字数据区域', max_length=20, blank=True, default='G3:G10')
    sort_data_result_1 = models.TextField('主关键字数据列最终排序结果', blank=True, default='')
    keyword_2 = models.CharField('次关键字', max_length=20, blank=True, default='')
    sort_type_2 = models.CharField('次关键字次序', choices=Sort_Type_Choice, max_length=20, blank=True, default='') 
    sort_data_position_2 = models.CharField('次关键字数据区域', max_length=20, blank=True, default='F3:F10')
    sort_data_result_2 = models.TextField('次关键字数据列最终排序结果', blank=True, default='')


    # 公式 max/min
    # 题目示例：用公式计算工作表[Start:End单元格/]的最大值/最小值，将计算公式写在X单元格
    formula_maxmin_op = models.BooleanField('考查公式max/min？', default=False)
    formula_maxmin_description = models.TextField('题目文字描述', 
        default='用公式计算工作表[Start:End单元格/]的最大值/最小值，将计算公式写在X单元格')
    formula_maxmin_data_position = models.CharField('数据区域[Start:End]', max_length=20, blank=True, default='A2:A20')
    formula_maxmin_result_position = models.CharField('公式填写在单元格', max_length=20, blank=True, default='') 
    formula_maxmin_result_regex = models.CharField('公式匹配模式', max_length=50, 
                blank=True, default='=MAX\(([A-Z])(\d+):([A-Z])(\d+)\)') 


    # 公式 sum/average
    # 题目示例：用公式计算工作表[Start:End单元格/]的总和/平均值，将计算公式写在X单元格
    formula_sumavg_op = models.BooleanField('考查公式sum/average？', default=False)
    formula_sumavg_description = models.TextField('题目文字描述', 
        default='用公式计算工作表[Start:End单元格/]的总和/平均值，将计算公式写在X单元格')
    formula_sumavg_data_position = models.CharField('数据区域[Start:End]', max_length=20, blank=True, default='A2:A20')
    formula_sumavg_result_position = models.CharField('公式填写在单元格', max_length=20, blank=True, default='') 
    formula_sumavg_result_regex = models.CharField('公式匹配模式', max_length=50, 
                blank=True, default='=SUM\(([A-Z])(\d+):([A-Z])(\d+)\)') 