from django.contrib import admin
from .models import WordOperations, WordQuestion
# Register your models here.

class WordOperationsAdmin(admin.ModelAdmin):
    fieldsets  = (
        ('段落内容', { 'fields': ('para_text',)}), 
        ('文字编辑', { 'fields': ('char_edit_op','char_edit_origin','char_edit_replace')}), 
        ('字体设置', { 'fields': ('font_op', 'font_name_chinese','font_name_ascii','font_size',
                                 'font_underline', 'font_color', ('font_bold','font_italic'),
                                )}), 
        ('段落格式设置', { 'fields': ('paraformat_op','para_alignment', 'para_left_indent','para_right_indent',
                                'para_first_line_indent','para_first_line_indent_size',
                                'para_firstchardropcap','para_firstchardropcaplines',
                                'para_space_before','para_space_after',
                                'para_line_spacing_rule','para_line_spacing',
                                ('page_break_before','keep_with_next','keep_together','window_control'),
                                )}), 

        )

admin.site.register(WordOperations, WordOperationsAdmin)
admin.site.register(WordQuestion)