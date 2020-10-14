from django.contrib import admin
from .models import WordOperations, WordQuestion, WordDocxFile, WordDocxFileTest
# Register your models here.

class WordOperationsAdmin(admin.ModelAdmin):

    list_display = ('id', 'para_text_simple', 'operations_list')

    # 'collapse',
    fieldsets  = (
        ('段落内容', { 'fields': ('para_text','pub_date')}), 
        ('文字编辑', { 'classes': ( 'extrapretty'), 'fields': ('char_edit_op','char_edit_origin','char_edit_replace')}), 
        ('字体设置', { 'classes': ( 'extrapretty'), 'fields': ('font_op', 'font_name_chinese','font_name_ascii','font_size',
                                 'font_underline', 'font_color', ('font_bold','font_italic'),
                                )}), 
        ('段落格式设置', { 'classes': ( 'extrapretty'), 'fields': ('paraformat_op','para_alignment', 'para_left_indent','para_right_indent',
                                'para_first_line_indent','para_first_line_indent_size',
                                'para_firstchardropcap','para_firstchardropcaplines',
                                'para_space_before','para_space_after',
                                'para_line_spacing_rule','para_line_spacing',
                                ('page_break_before','keep_with_next','keep_together','window_control'),
                                )}), 
        )

class WordQuestionAdmin(admin.ModelAdmin):
        filter_horizontal = ['word_operation_list']
        list_display = ('id', 'file_path','word_op_numb','word_op_description', 'word_test_result')

admin.site.register(WordOperations, WordOperationsAdmin)
admin.site.register(WordQuestion, WordQuestionAdmin)
admin.site.register(WordDocxFile)
admin.site.register(WordDocxFileTest)