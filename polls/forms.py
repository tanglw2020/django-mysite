
from django import forms

class WordUploadForm(forms.Form):
    
    FONT_NAME_ASCII_CHOICES = [
        ('无', '无'),
        ('MS Gothic', 'MS Gothic'),
        ('MS Mincho', 'MS Mincho'),
        ('MS PMincho', 'MS PMincho'),
        ('MS UI Gothic', 'MS UI Gothic'),
        ('Yu Gothic', 'Yu Gothic'),
    ]

    file_upload =  forms.FileField()


class WordOpForm(forms.Form):

    FONT_NAME_ASCII_CHOICES = [
        ('无', '无'),
        ('MS Gothic', 'MS Gothic'),
        ('MS Mincho', 'MS Mincho'),
        ('MS PMincho', 'MS PMincho'),
        ('MS UI Gothic', 'MS UI Gothic'),
        ('Yu Gothic', 'Yu Gothic'),
    ]

    FONT_NAME_CHINESE_CHOICES = [
        ('无', '无'),
        ('宋体', '宋体'),
        ('黑体', '黑体'),
        ('华文仿宋', '华文仿宋'),
    ]

    FONT_SIZE_CHOICES = [
        ('一号','一号' ),
        ('二号','二号' ),
        ('三号','三号' ),
        ('四号','四号' ),
        ('五号','五号' ),
        ('六号','六号' ),
        ('七号','七号' ),
        ('八号','八号' ),
    ]

    FONT_COLOR_CHOICES = [
        ('无', '无'),
        ('红色', '红色'),
        ('黄色', '黄色'),
        ('绿色', '绿色'),
    ]

    FONT_UNDERLINE_CHOICES = [
        ('无', '无'),
        ('下划线', '下划线'),
        ('双下划线', '双下划线'),
        ('粗线', '粗线'),
    ]

    PARA_ALIGNMENT_CHOICES = [
        ('无', '无'),
        ('左对齐', '左对齐'),
        ('居中', '居中'),
        ('右对齐', '右对齐'),
        ('两端对齐', '两端对齐'),
        ('分散对齐', '分散对齐'),
    ]

    PARA_FIRST_LINE_INDENT_CHOICES = [
        ('无', '无'),
        ('首行', '首行'),
        ('悬挂', '悬挂'),
    ]

    PARA_LINE_SPACING_RULE_CHOICES = [
        ('无', '无'),
        ('单倍行距', '单倍行距'),
        ('多倍行距', '多倍行距'),
        ('固定值', '固定值'),
    ]

    PARA_FIRSTCHARDROPCAP_CHOICES = [
        ('无', '无'),
        ('下沉', '下沉'),
        ('下沉', '悬挂'),
    ]

    PARA_LINE_PAGE_CHOICES = [
        ('孤行控制', '孤行控制'),
        ('与下段同页', '与下段同页'),
        ('段中不分页', '段中不分页'),
        ('段前分页', '段前分页'),
    ]

    para_text = forms.CharField(label='要操作的段落内容',  widget=forms.Textarea)

    char_edit_op = forms.BooleanField(label='是否考查文字查找替换？', label_suffix='', required=False)
    char_edit_origin = forms.CharField(label='原词', required=False)
    char_edit_replace = forms.CharField(label='替换为', required=False)
    # char_edit_result = forms.CharField(label='文字编辑结果', widget=forms.Textarea)

    font_op = forms.BooleanField(label='是否考查字体设置？', label_suffix='', required=False)
    font_name_ascii = forms.ChoiceField(label='英文字体', required=False, 
        choices=FONT_NAME_ASCII_CHOICES) 
    font_name_chinese = forms.ChoiceField(label='中文字体', required=False,
        choices=FONT_NAME_CHINESE_CHOICES)
    font_size = forms.ChoiceField(label='字号', required=False, choices=FONT_SIZE_CHOICES)
    font_color = forms.ChoiceField(label='字体颜色', choices=FONT_COLOR_CHOICES, required=False)
    font_bold = forms.BooleanField(label='粗体', required=False)
    font_italic = forms.BooleanField(label='斜体', required=False)
    font_underline = forms.ChoiceField(label='下划线', choices=FONT_UNDERLINE_CHOICES, required=False)

    paraformat_op = forms.BooleanField(label='是否考查段落格式设置？', label_suffix='', required=False)
    para_alignment = forms.ChoiceField(label='段落对齐', choices=PARA_ALIGNMENT_CHOICES, required=False)
    para_left_indent = forms.CharField(label='左侧缩进(磅)', widget=forms.NumberInput, required=False, initial='10')
    para_right_indent = forms.CharField(label='右侧缩进(磅)', widget=forms.NumberInput, required=False, initial='10')
    para_first_line_indent = forms.ChoiceField(label='首行缩进', choices=PARA_FIRST_LINE_INDENT_CHOICES, required=False)
    para_first_line_indent_size = forms.CharField(label='首行缩进距离(磅)', widget=forms.NumberInput, required=False, initial='10')

    para_space_before = forms.CharField(label='段前间距(磅)', widget=forms.NumberInput, required=False, initial='10')
    para_space_after = forms.CharField(label='段后间距(磅)', widget=forms.NumberInput, required=False, initial='10')
    para_line_spacing_rule = forms.ChoiceField(label='行距规则', choices=PARA_LINE_SPACING_RULE_CHOICES, required=False)
    para_line_spacing = forms.CharField(label='行距(行)', widget=forms.NumberInput, required=False, initial='1.0')

    para_firstchardropcap = forms.ChoiceField(label='首字下沉', choices=PARA_FIRSTCHARDROPCAP_CHOICES, required=False)
    para_firstchardropcaplines = forms.CharField(label='下沉(行)', widget=forms.NumberInput, required=False, initial='3')

    para_line_page = forms.MultipleChoiceField(label='换行和分页', choices=PARA_LINE_PAGE_CHOICES, required=False,
    widget= forms.CheckboxSelectMultiple)
    # page_break_before 
    # keep_with_next 
    # keep_together 
    # widow_control