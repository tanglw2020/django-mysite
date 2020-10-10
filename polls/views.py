from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django import forms

class WordOpForm(forms.Form):

    FONT_NAME_ASCII_CHOICES = [
        (0, '无'),
        (1, 'MS Gothic'),
        (2, 'MS Mincho'),
        (3, 'MS PMincho'),
        (4, 'MS UI Gothic'),
        (5, 'Yu Gothic'),
    ]

    FONT_NAME_CHINESE_CHOICES = [
        (0, '无'),
        (1, '宋体'),
        (2, '黑体'),
        (3, '华文仿宋'),
    ]

    FONT_COLOR_CHOICES = [
        (0, '无'),
        (1, '红色'),
        (2, '黄色'),
        (3, '绿色'),
    ]

    FONT_UNDERLINE_CHOICES = [
        (0, '无'),
        (1, '下划线'),
        (2, '双下划线'),
        (3, '粗线'),
    ]

    PARA_ALIGNMENT_CHOICES = [
        (0, '无'),
        (1, '左对齐'),
        (2, '居中'),
        (3, '右对齐'),
        (4, '两端对齐'),
        (5, '分散对齐'),
    ]

    PARA_FIRST_LINE_INDENT_CHOICES =  [
        (0, '无'),
        (1, '首行'),
        (2, '悬挂'),
    ]

    PARA_LINE_SPACING_RULE_CHOICES = [
        (0, '无'),
        (1, '单倍行距'),
        (2, '多倍行距'),
        (3, '固定值'),
    ]

    PARA_FIRSTCHARDROPCAP_CHOICES = [
        (0, '无'),
        (1, '下沉'),
        (2, '悬挂'),
    ]

    para_line_page_CHOICES = [
        (1, '孤行控制'),
        (2, '与下段同页'),
        (3, '段中不分页'),
        (4, '段前分页'),
    ]

    para_text = forms.CharField(label='要操作的段落内容',  widget=forms.Textarea)

    char_edit_op = forms.BooleanField(label='是否考查文字编辑？')
    char_edit_result = forms.CharField(label='文字编辑结果', widget=forms.Textarea)

    font_op = forms.BooleanField(label='是否考查字体设置？')
    font_name_ascii = forms.ChoiceField(label='英文字体',
        choices=FONT_NAME_ASCII_CHOICES) 
    font_name_chinese = forms.ChoiceField(label='中文字体',
        choices=FONT_NAME_CHINESE_CHOICES)
    font_size = forms.CharField(label='字体大小(磅)', widget=forms.NumberInput)
    font_color = forms.ChoiceField(label='字体颜色', choices=FONT_COLOR_CHOICES)
    font_bold = forms.BooleanField(label='粗体')
    font_italic = forms.BooleanField(label='斜体')
    font_underline = forms.ChoiceField(label='下划线', choices=FONT_UNDERLINE_CHOICES)

    paraformat_op = forms.BooleanField(label='是否考查段落格式设置？')
    para_alignment = forms.ChoiceField(label='段落对齐', choices=PARA_ALIGNMENT_CHOICES)
    para_left_indent = forms.CharField(label='左侧缩进(磅)', widget=forms.NumberInput)
    para_right_indent = forms.CharField(label='右侧缩进(磅)', widget=forms.NumberInput)
    para_first_line_indent = forms.ChoiceField(label='首行缩进', choices=PARA_FIRST_LINE_INDENT_CHOICES)
    para_first_line_indent_size = forms.CharField(label='首行缩进距离(磅)', widget=forms.NumberInput)

    para_space_before = forms.CharField(label='段前间距(磅)', widget=forms.NumberInput)
    para_space_after = forms.CharField(label='段后间距(磅)', widget=forms.NumberInput)
    para_line_spacing_rule = forms.ChoiceField(label='行距规则', choices=PARA_LINE_SPACING_RULE_CHOICES)
    para_line_spacing = forms.CharField(label='行距(行)', widget=forms.NumberInput)

    para_firstchardropcap = forms.ChoiceField(label='首字下沉', choices=PARA_FIRSTCHARDROPCAP_CHOICES)
    para_firstchardropcaplines = forms.CharField(label='下沉(行)', widget=forms.NumberInput)

    para_line_page = forms.ChoiceField(label='换行和分页', choices=para_line_page_CHOICES,
    widget= forms.CheckboxSelectMultiple)
    # para_page_break_before = forms.BooleanField(label='')
    # para_keep_with_next = forms.BooleanField(label='')
    # para_keep_together = forms.BooleanField(label='')
    # para_widow_control = = forms.BooleanField(label='')




def index(request):
    action_list = ["查看题库",
    "录入选择题",
    "录入word操作题",
    "录入Excel操作题",
    "录入PPT操作题"
    ]
    context = {'action_list': action_list}
    return render(request, 'polls/index.html', context)


def input_word_operation(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = WordOpForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('polls:input_word_operation'))
    else:
        form = WordOpForm()

    word_action_list = ["字体字号",
    "段落格式",
    "插入图片",
    "style",
    ]
    
    context = {
        'word_action_list': word_action_list,
        'title': "Word操作题录入页面",
        'form': form
        }
    return render(request, 'polls/input_word_operation.html', context)
