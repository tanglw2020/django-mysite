from django.contrib import admin
import random

from .choiceQuestionModels import *
from .emailModels import EmailQuestion
from .fileOperationlModels import FileOperationQuestion
from .wordModels import WordQuestion
from .excelModels import ExcelQuestion
from .pptModels import PPTQuestion
from .examModels import *
from polls.textinputModels import *

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
        list_display = ('id', 'class_name', 'student_name', 'student_id', )
        search_fields = ['student_id']


class ExamAdmin(admin.ModelAdmin):
        list_display = ('id_', 'problem_type', 'info_text','all_question_stat_','out_link_',)


class ExamPaperAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'problem_type', 'student', 'exam', 'start_time_','end_time_')
        search_fields = ['student_id_local', 'exam_id_local']


class TextQuestionAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'content')

class WordQuestionAdmin(admin.ModelAdmin):
        # list_display = ('__str__','word_op_numb','word_op_description', 'word_test_result')
        list_display = ('__str__',
                        'operation_description_all', 
                        'test_', 
                        'docx_path_',
                        )
        
        fieldsets  = (
        ('上传Word文件', { 'fields': ('pub_date','upload_docx',)}), 
        ('要考查项目', { 'fields': (( 'char_edit_op','font_op','paraformat_op','style_op','image_op','table_op'),)}), 
        ('文字编辑', { 'classes': ('collapse',), 'fields': ('char_edit_text','char_edit_origin','char_edit_replace')}), 
        ('字体设置', { 'classes': ('collapse',),'fields': ('font_text', 'font_name_chinese', 'font_name_ascii','font_size',
                                 'font_color', 'font_underline',('font_bold','font_italic'),
                                )}), 
                                # ('para_firstchardropcap','para_firstchardropcaplines'),
        ('段落格式设置', { 'classes': ('collapse',), 'fields': ('paraformat_text', 'para_alignment', 
                                ('para_left_indent','para_right_indent'), 
                                ('para_space_before','para_space_after'),
                                ('para_line_spacing_rule','para_line_spacing'),
                                ('para_first_line_indent','para_first_line_indent_size'),
                                ('page_break_before','keep_with_next','keep_together','widow_control'),
                                )}), 
        ('样式设置', { 'classes': ( 'collapse',), 'fields': ('style_text', 'style_name', 
                                ('style_font_name_chinese','style_font_name_ascii','style_font_size'),
                                  'style_font_color', ('style_font_underline', 'style_font_bold','style_font_italic'),
                                'style_para_alignment', ('style_para_left_indent','style_para_right_indent'),
                                ('style_para_space_before','style_para_space_after'),
                                ('style_para_line_spacing_rule','style_para_line_spacing'),
                                ('style_para_first_line_indent','style_para_first_line_indent_size'),
                                ('style_page_break_before','style_keep_with_next','style_keep_together','style_widow_control'),
                                )}), 
        ('图像插入(默认原文档无图片)', { 'classes': ( 'collapse',), 'fields': ('image_text', 'upload_image_file',
                                'image_position_style',
                                ('image_width', 'image_height'), 
                                )}), 
        ('表格插入', { 'classes': ( 'collapse',), 'fields': ('table_text',
                                'table_autofit', 'table_alignment',  'table_style', 
                                )}), 
        )


class ChoiceQuestionAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'question_text', 'description',)
        list_display_links = ('question_text',)


class EmailQuestionAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'question_content',)


class FileOperationQuestionAdmin(admin.ModelAdmin):
        list_display = ('__str__', 'question_content','zipfile_path_')

        fieldsets = (
                ('在考生文件夹中创建文件夹[A]，并在[A]中新建文件[B]', {'fields':('new_folder_dir_A', 'new_file_B')}),
                ('在考生文件夹中删除[A]/[B]中的文件[C]', {'fields':('del_folder_A', 'del_folder_B','del_file_C')}),
                ('将考生文件夹中[A]/[B]文件的属性修改成[C]', {'fields':('modify_folder_A', 'modify_file_B','modify_file_attr')}),
                ('将考生文件夹中[A]/[B]重命名为[C]', {'fields':('rename_folder_A', 'rename_file_B','rename_file_C')}),
                ('将考生文件夹中[A]/[B]复制或移动到[C]', {'fields':('copy_folder_A', 'copy_file_B','copy_or_move','copy_folder_C')}),
        )


class ExcelQuestionAdmin(admin.ModelAdmin):

        list_display = ('__str__', 'question_content', 'test_', 'file_path_',)

        fieldsets = (
                ('上传题目所需excel文件', {'fields':('pub_date', 'upload_excel',)}),
                ('1 重命名工作表Sheet1', {'classes': ( 'collapse',),'fields':('rename_sheet_op', 'new_sheet_name')}),
                ('2 合并单元格', {'classes': ( 'collapse',),'fields':('merge_cell_op', 'merge_cell_position')}),
                ('3 设置单元格颜色', {'classes': ( 'collapse',),'fields':('color_cell_op', 'color_cell_position',
                        ('color_cell_font','color_cell_filling') )}),
                ('4 设置单元格条件格式', {'classes': ( 'collapse',),'fields':('conditional_formatting_op',
                        'conditional_formatting_position',
                        ('conditional_formatting_type',
                        'conditional_formatting_param'), 'conditional_formatting_coloring')}),
                ('5 单元格套用表格格式', {'classes': ( 'collapse',),'fields':('table_style_op', 
                        ('table_style_position','table_style_choice'))}),
                ('6 插入数据图表', {'classes': ( 'collapse',),'fields':('chart_op', 
                        ('chart_data_name','chart_data_position'),
                        ('chart_type','chart_tiltle'),'chart_position')}),
                ('7 双关键字排序', {'classes': ( 'collapse',),'fields':('sort_op', ('keyword_1','sort_type_1'), 
                        ('sort_data_position_1', 'sort_data_result_1'), 
                        ('keyword_2','sort_type_2'),
                        ('sort_data_position_2', 'sort_data_result_2'), 
                        )}),
                ('8 公式1', {'classes': ( 'collapse',),'fields':('formula_maxmin_op', 
                        'formula_maxmin_data_position',
                        ('formula_maxmin_result_position', 'formula_maxmin_result_regex'),
                        'formula_maxmin_description',
                        ) }),
                ('9 公式2', {'classes': ( 'collapse',),'fields':('formula_sumavg_op', 
                        'formula_sumavg_data_position',
                        ('formula_sumavg_result_position', 'formula_sumavg_result_regex'),
                        'formula_sumavg_description',
                ) }),
        )


class PPTQuestionAdmin(admin.ModelAdmin):

        list_display = ('__str__', 'question_content', 'test_', 'file_path_',)

        fieldsets = (
                ('上传题目所需ppt文件', {'fields':('pub_date', 'upload_pptx',)}),
                ('1 选择版式', 
                {'classes': ('collapse',),
                'fields':( 'slide_layout_op', 
                'slide_layout_target_slide',
                'slide_layout_name')}),
                ('2 修改文字内容', 
                {'classes': ('collapse',),
                'fields':( 'text_op', 
                'text_target_slide', 
                'text_target_shape_1', 'text_target_content_1', 
                'text_target_shape_2', 'text_target_content_2', 
                )}),
                ('3 修改字体格式', 
                {'classes': ('collapse',),
                'fields':( 'font_op', 
                'font_target_slide', 
                'font_target_shape', 'font_target_content', 
                ('font_name', 'font_size', 'font_color'),('font_bold', 'font_italic')
                )}),
                ('4 设置幻灯片背景格式', 
                {'classes': ('collapse',),
                'fields':( 'slide_background_op', 
                'slide_background_slide', 
                'slide_background_type',
                ('slide_background_back', 'slide_background_fore', ),
                )}),
                ('5 添加备注', 
                {'classes': ('collapse',),
                'fields':( 'notes_slide_op', 
                'notes_slide_target_slide', 
                'notes_slide_content',
                )}),
                ('6 插入表格及内容', 
                {'classes': ('collapse',),
                'fields':( 'table_op', 
                'table_target_slide', 
                'table_target_shape',('table_rows','table_columns'),
                'table_content',
                )}),
        )



admin.site.register(TextQuestion, TextQuestionAdmin)
admin.site.register(ChoiceQuestion, ChoiceQuestionAdmin)
admin.site.register(WordQuestion, WordQuestionAdmin)
admin.site.register(EmailQuestion, EmailQuestionAdmin)
admin.site.register(FileOperationQuestion, FileOperationQuestionAdmin)
admin.site.register(ExcelQuestion, ExcelQuestionAdmin)
admin.site.register(PPTQuestion, PPTQuestionAdmin)

admin.site.register(Exam, ExamAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(ExamPaper, ExamPaperAdmin)
admin.site.register([StudentInfoImporter, ChoiceQuestionImporter])

admin.site.site_title = "计算等级考试后台管理系统"
admin.site.site_header = "计算等级考试后台管理系统"