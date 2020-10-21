from django.contrib import admin
from .models import WordOperations, WordQuestion, WordDocxFile, WordDocxFileTest
# Register your models here.

class WordOperationsAdmin(admin.ModelAdmin):

    list_display = ('id', 'para_text_simple', 'operations_list')

    # 'collapse',
    fieldsets  = (
        ('段落内容', { 'fields': ('para_text','pub_date')}), 
        ('文字编辑', { 'classes': ( 'extrapretty'), 'fields': ('char_edit_op','char_edit_origin','char_edit_replace')}), 
        ('字体设置', { 'fields': ('font_op', ('font_name_chinese', 'font_name_ascii','font_size'),
                                 'font_color', ('font_underline','font_bold','font_italic'),
                                )}), 
        ('段落格式设置', { 'classes': ( 'extrapretty'), 'fields': ('paraformat_op','para_alignment', 
                                ('para_left_indent','para_right_indent'), 
                                ('para_space_before','para_space_after'),
                                ('para_line_spacing_rule','para_line_spacing'),
                                ('para_first_line_indent','para_first_line_indent_size'),
                                ('para_firstchardropcap','para_firstchardropcaplines'),
                                ('page_break_before','keep_with_next','keep_together','window_control'),
                                )}), 
        ('样式设置', { 'classes': ( 'extrapretty'), 'fields': ('style_op', 'style_name', 
                                'style_font_name_chinese','style_font_name_ascii','style_font_size',
                                 'style_font_underline', 'style_font_color', ('style_font_bold','style_font_italic'),
                                'style_para_alignment', 'style_para_left_indent','style_para_right_indent',
                                'style_para_first_line_indent','style_para_first_line_indent_size',
                                'style_para_firstchardropcap','style_para_firstchardropcaplines',
                                'style_para_space_before','style_para_space_after',
                                'style_para_line_spacing_rule','style_para_line_spacing',
                                ('style_page_break_before','style_keep_with_next','style_keep_together','style_window_control'),
                                )}), 
        )

class WordQuestionAdmin(admin.ModelAdmin):
        filter_horizontal = ['word_operation_list']
        list_display = ('id', 'file_path','word_op_numb','word_op_description', 'word_test_result')

admin.site.register(WordOperations, WordOperationsAdmin)
admin.site.register(WordQuestion, WordQuestionAdmin)
admin.site.register(WordDocxFile)
admin.site.register(WordDocxFileTest)