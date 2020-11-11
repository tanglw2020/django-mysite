from django.contrib import admin
from .wordModels import WordOperations, WordQuestion
from .wordFileModels import  WordDocxFile, WordDocxFileTest

# Register your models here.
class WordOperationsInline(admin.StackedInline):
    model = WordOperations
    extra = 0

    fieldsets  = (
        ('', { 'fields': ('para_text',('char_edit_op','font_op','paraformat_op','style_op','image_op'),)}), 
        ('文字编辑', { 'classes': ('collapse',), 'fields': ('char_edit_origin','char_edit_replace')}), 
        ('字体设置', { 'classes': ('collapse',),'fields': ( 'font_name_chinese', 'font_name_ascii','font_size',
                                 'font_color', 'font_underline',('font_bold','font_italic'),
                                )}), 
                                # ('para_firstchardropcap','para_firstchardropcaplines'),
        ('段落格式设置', { 'classes': ('collapse',), 'fields': ('para_alignment', 
                                ('para_left_indent','para_right_indent'), 
                                ('para_space_before','para_space_after'),
                                ('para_line_spacing_rule','para_line_spacing'),
                                ('para_first_line_indent','para_first_line_indent_size'),
                                ('page_break_before','keep_with_next','keep_together','widow_control'),
                                )}), 
        ('样式设置', { 'classes': ( 'collapse',), 'fields': ( 'style_name', 
                                ('style_font_name_chinese','style_font_name_ascii','style_font_size'),
                                  'style_font_color', ('style_font_underline', 'style_font_bold','style_font_italic'),
                                'style_para_alignment', ('style_para_left_indent','style_para_right_indent'),
                                ('style_para_space_before','style_para_space_after'),
                                ('style_para_line_spacing_rule','style_para_line_spacing'),
                                ('style_para_first_line_indent','style_para_first_line_indent_size'),
                                ('style_page_break_before','style_keep_with_next','style_keep_together','style_widow_control'),
                                )}), 
        ('图像插入', { 'classes': ( 'collapse',), 'fields': ('image_position_style',
                                ('image_width', 'image_height'), 
                                'upload_image_file'
                                )}), 
        )


class WordOperationsAdmin(admin.ModelAdmin):

    list_display = ('__str__', 'word_question_info',  'operations_list', 'operation_description_all')
    search_fields = ('id',)

    # 'collapse',
    fieldsets  = (
        ('段落内容', { 'fields': ('word_question', 'para_text',)}), 
        ('考查操作', { 'fields': ('char_edit_op','font_op','paraformat_op','style_op','image_op',)}), 
        ('文字编辑', { 'classes': ( 'extrapretty'), 'fields': ('char_edit_origin','char_edit_replace')}), 
        ('字体设置', { 'fields': ( ('font_name_chinese', 'font_name_ascii','font_size'),
                                 'font_color', ('font_underline','font_bold','font_italic'),
                                )}), 
        ('段落格式设置', { 'classes': ( 'extrapretty'), 'fields': ('para_alignment', 
                                ('para_left_indent','para_right_indent'), 
                                ('para_space_before','para_space_after'),
                                ('para_line_spacing_rule','para_line_spacing'),
                                ('para_first_line_indent','para_first_line_indent_size'),
                                ('para_firstchardropcap','para_firstchardropcaplines'),
                                ('page_break_before','keep_with_next','keep_together','widow_control'),
                                )}), 
        ('样式设置', { 'classes': ( 'extrapretty'), 'fields': ( 'style_name', 
                                ('style_font_name_chinese','style_font_name_ascii','style_font_size'),
                                  'style_font_color', ('style_font_underline', 'style_font_bold','style_font_italic'),
                                'style_para_alignment', ('style_para_left_indent','style_para_right_indent'),
                                ('style_para_space_before','style_para_space_after'),
                                ('style_para_line_spacing_rule','style_para_line_spacing'),
                                ('style_para_first_line_indent','style_para_first_line_indent_size'),
                                ('style_para_firstchardropcap','style_para_firstchardropcaplines'),
                                ('style_page_break_before','style_keep_with_next','style_keep_together','style_widow_control'),
                                )}), 
        ('图像插入', { 'classes': ( 'extrapretty'), 'fields': ('image_position_style',
                                ('image_width', 'image_height'), 
                                'upload_image_file'
                                )}), 
        )

class WordQuestionAdmin(admin.ModelAdmin):
        # filter_horizontal = ['word_operation_list']
        list_display = ('__str__','word_op_numb','word_op_description', 'word_test_result')

        inlines = [WordOperationsInline]

admin.site.register(WordOperations, WordOperationsAdmin)
admin.site.register(WordQuestion, WordQuestionAdmin)
admin.site.register([WordDocxFile,WordDocxFileTest])
