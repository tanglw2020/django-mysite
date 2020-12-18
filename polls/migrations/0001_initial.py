# Generated by Django 3.1.2 on 2020-12-18 13:17

from django.db import migrations, models
import django.db.models.deletion
import polls.wordFileModels


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChoiceQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(verbose_name='题干')),
                ('choice_1', models.CharField(default='', max_length=200, verbose_name='选项1')),
                ('choice_2', models.CharField(default='', max_length=200, verbose_name='选项2')),
                ('choice_3', models.CharField(default='', max_length=200, verbose_name='选项3')),
                ('choice_4', models.CharField(default='', max_length=200, verbose_name='选项4')),
                ('answer', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], max_length=2, verbose_name='答案')),
            ],
            options={
                'verbose_name': '选择题',
                'verbose_name_plural': '选择题',
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(verbose_name='创建时间')),
                ('exam_name', models.CharField(max_length=50, verbose_name='考试学期')),
                ('exam_type', models.CharField(choices=[('计算机等级考试一', '计算机等级考试一')], max_length=50, verbose_name='考试类型')),
            ],
            options={
                'verbose_name': '考试信息',
                'verbose_name_plural': '考试信息',
            },
        ),
        migrations.CreateModel(
            name='ExamPaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_type', models.CharField(choices=[('计算机等级考试一', '计算机等级考试一')], max_length=50, verbose_name='考试类型')),
                ('choice_question_list', models.CharField(default='', max_length=200, verbose_name='选择题')),
                ('system_question_id', models.PositiveIntegerField(default=0, verbose_name='系统操作题')),
                ('internet_question_id', models.PositiveIntegerField(default=0, verbose_name='上网题')),
                ('word_question_id', models.PositiveIntegerField(default=0, verbose_name='word操作题')),
                ('excel_question_id', models.PositiveIntegerField(default=0, verbose_name='excel操作题')),
                ('ppt_question_id', models.PositiveIntegerField(default=0, verbose_name='ppt操作题')),
                ('end_by_hand', models.BooleanField(default=False, verbose_name='是否已经手动结束')),
                ('delay_by_hand', models.PositiveIntegerField(default=0, verbose_name='手动延时(分钟)')),
                ('choice_question_answer', models.CharField(default='', max_length=200, verbose_name='选择题答案')),
                ('system_question_answer_file', models.CharField(default='', max_length=200, verbose_name='系统操作题答案')),
                ('internet_question_answer_file', models.CharField(default='', max_length=200, verbose_name='上网题答案')),
                ('word_question_answer_file', models.CharField(default='', max_length=200, verbose_name='word操作题答案')),
                ('excel_question_answer_file', models.CharField(default='', max_length=200, verbose_name='excel操作题答案')),
                ('ppt_question_answer_file', models.CharField(default='', max_length=200, verbose_name='ppt操作题答案')),
            ],
            options={
                'verbose_name': '试卷',
                'verbose_name_plural': '试卷',
            },
        ),
        migrations.CreateModel(
            name='WordDocxFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(blank=True, null=True, upload_to='uploads_docx/', validators=[polls.wordFileModels.validate_docx])),
            ],
            options={
                'verbose_name': '考试用Word文件',
                'verbose_name_plural': '考试用Word文件',
            },
        ),
        migrations.CreateModel(
            name='WordDocxFileTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(blank=True, null=True, upload_to='uploads_docx_test/', validators=[polls.wordFileModels.validate_docx])),
            ],
            options={
                'verbose_name': '内部测试用word文件',
                'verbose_name_plural': '内部测试用word文件',
            },
        ),
        migrations.CreateModel(
            name='WordQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(verbose_name='创建时间')),
                ('upload_docx', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.worddocxfile', verbose_name='上传Word文件(.docx)')),
                ('upload_docx_test', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.worddocxfiletest', verbose_name='内部测试用word文件.docx')),
            ],
            options={
                'verbose_name': 'Word操作题目',
                'verbose_name_plural': 'Word操作题目',
            },
        ),
        migrations.CreateModel(
            name='WordOperations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('para_text', models.TextField(verbose_name='要考查的段落内容')),
                ('char_edit_op', models.BooleanField(default=False, verbose_name='考查文字查找替换？')),
                ('char_edit_origin', models.CharField(blank=True, default='', max_length=200, verbose_name='原词')),
                ('char_edit_replace', models.CharField(blank=True, default='', max_length=200, verbose_name='替换为')),
                ('font_op', models.BooleanField(default=False, verbose_name='考查字体设置？')),
                ('font_name_ascii', models.CharField(blank=True, choices=[('Arial Black', 'Arial Black'), ('Bahnschrift', 'Bahnschrift'), ('Book Antiqua', 'Book Antiqua'), ('Dubai', 'Dubai'), ('Impact', 'Impact')], default='', max_length=200, verbose_name='英文字体')),
                ('font_name_chinese', models.CharField(blank=True, choices=[('黑体', '黑体'), ('华文仿宋', '华文仿宋'), ('楷体', '楷体'), ('幼圆', '幼圆'), ('微软雅黑', '微软雅黑'), ('隶书', '隶书')], default='', max_length=200, verbose_name='中文字体')),
                ('font_size', models.CharField(blank=True, choices=[('5', '5'), ('8', '8'), ('14', '14'), ('18', '18'), ('22', '22'), ('26', '26'), ('36', '36'), ('48', '48'), ('72', '72')], default='', max_length=200, verbose_name='字号(磅)')),
                ('font_bold', models.BooleanField(blank=True, default='', verbose_name='粗体')),
                ('font_italic', models.BooleanField(blank=True, default='', verbose_name='斜体')),
                ('font_underline', models.CharField(blank=True, choices=[('True', '普通下划线'), ('DOUBLE (3)', '双下划线'), ('THICK (6)', '粗下划线'), ('WAVY (11)', '波浪下划线')], default='', max_length=200, verbose_name='下划线')),
                ('font_color', models.CharField(blank=True, choices=[('C00000', '深红'), ('FF0000', '红色'), ('92D050', '浅绿'), ('00B050', '绿色'), ('00B0F0', '浅蓝'), ('0070C0', '蓝色'), ('7030A0', '紫色')], default='', max_length=200, verbose_name='字色(标准色)')),
                ('paraformat_op', models.BooleanField(default=False, verbose_name='考查段落格式设置？')),
                ('para_alignment', models.CharField(blank=True, choices=[('LEFT (0)', '左对齐'), ('CENTER (1)', '居中对齐'), ('RIGHT (2)', '右对齐'), ('JUSTIFY (3)', '两端对齐'), ('DISTRIBUTE (4)', '分散对齐')], default='', max_length=200, verbose_name='段落对齐')),
                ('para_left_indent', models.CharField(blank=True, choices=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35')], default='', max_length=200, verbose_name='左侧缩进(磅)')),
                ('para_right_indent', models.CharField(blank=True, choices=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35')], default='', max_length=200, verbose_name='右侧缩进(磅)')),
                ('para_first_line_indent', models.CharField(blank=True, choices=[('首行缩进', '缩进'), ('首行悬挂', '悬挂')], default='', max_length=200, verbose_name='首行缩进')),
                ('para_first_line_indent_size', models.CharField(blank=True, choices=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35')], default='', max_length=200, verbose_name='首行缩进距离(磅)')),
                ('para_space_before', models.CharField(blank=True, choices=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35')], default='', max_length=200, verbose_name='段前间距(磅)')),
                ('para_space_after', models.CharField(blank=True, choices=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35')], default='', max_length=200, verbose_name='段后间距(磅)')),
                ('para_line_spacing_rule', models.CharField(blank=True, choices=[('SINGLE (0)', '单倍行距'), ('ONE_POINT_FIVE (1)', '1.5倍行距'), ('DOUBLE (2)', '双倍行距'), ('MULTIPLE (5)', '多倍行距')], default='', max_length=200, verbose_name='行距规则')),
                ('para_line_spacing', models.CharField(blank=True, choices=[('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], default='', max_length=200, verbose_name='行距(行)')),
                ('page_break_before', models.BooleanField(default=False, verbose_name='段前分页')),
                ('keep_with_next', models.BooleanField(default=False, verbose_name='与下段同页')),
                ('keep_together', models.BooleanField(default=False, verbose_name='段中不分页')),
                ('widow_control', models.BooleanField(default=False, verbose_name='孤行控制')),
                ('style_op', models.BooleanField(default=False, verbose_name='考查样式设置？')),
                ('style_name', models.CharField(blank=True, choices=[('标题1', '标题1'), ('标题2', '标题2'), ('标题3', '标题3'), ('标题4', '标题4'), ('强调', '强调'), ('列表编号', '列表编号'), ('列表项目符号', '列表项目符号'), ('新样式1', '新样式1'), ('新样式2', '新样式2')], default='', max_length=200, verbose_name='样式名称')),
                ('style_font_name_ascii', models.CharField(blank=True, choices=[('Arial Black', 'Arial Black'), ('Bahnschrift', 'Bahnschrift'), ('Book Antiqua', 'Book Antiqua'), ('Dubai', 'Dubai'), ('Impact', 'Impact')], default='', max_length=200, verbose_name='英文字体')),
                ('style_font_name_chinese', models.CharField(blank=True, choices=[('黑体', '黑体'), ('华文仿宋', '华文仿宋'), ('楷体', '楷体'), ('幼圆', '幼圆'), ('微软雅黑', '微软雅黑'), ('隶书', '隶书')], default='', max_length=200, verbose_name='中文字体')),
                ('style_font_size', models.CharField(blank=True, choices=[('5', '5'), ('8', '8'), ('14', '14'), ('18', '18'), ('22', '22'), ('26', '26'), ('36', '36'), ('48', '48'), ('72', '72')], default='', max_length=200, verbose_name='字号')),
                ('style_font_bold', models.BooleanField(default=False, verbose_name='粗体')),
                ('style_font_italic', models.BooleanField(default=False, verbose_name='斜体')),
                ('style_font_underline', models.CharField(blank=True, choices=[('True', '普通下划线'), ('DOUBLE (3)', '双下划线'), ('THICK (6)', '粗下划线'), ('WAVY (11)', '波浪下划线')], default='', max_length=200, verbose_name='下划线')),
                ('style_font_color', models.CharField(blank=True, choices=[('C00000', '深红'), ('FF0000', '红色'), ('92D050', '浅绿'), ('00B050', '绿色'), ('00B0F0', '浅蓝'), ('0070C0', '蓝色'), ('7030A0', '紫色')], default='', max_length=200, verbose_name='字色(标准色)')),
                ('style_para_alignment', models.CharField(blank=True, choices=[('LEFT (0)', '左对齐'), ('CENTER (1)', '居中对齐'), ('RIGHT (2)', '右对齐'), ('JUSTIFY (3)', '两端对齐'), ('DISTRIBUTE (4)', '分散对齐')], default='', max_length=200, verbose_name='段落对齐')),
                ('style_para_left_indent', models.CharField(blank=True, choices=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35')], default='', max_length=200, verbose_name='左侧缩进(磅)')),
                ('style_para_right_indent', models.CharField(blank=True, choices=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35')], default='', max_length=200, verbose_name='右侧缩进(磅)')),
                ('style_para_first_line_indent', models.CharField(blank=True, choices=[('首行缩进', '缩进'), ('首行悬挂', '悬挂')], default='', max_length=200, verbose_name='首行缩进')),
                ('style_para_first_line_indent_size', models.CharField(blank=True, choices=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35')], default='', max_length=200, verbose_name='首行缩进距离(磅)')),
                ('style_para_space_before', models.CharField(blank=True, choices=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35')], default='', max_length=200, verbose_name='段前间距(磅)')),
                ('style_para_space_after', models.CharField(blank=True, choices=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35')], default='', max_length=200, verbose_name='段后间距(磅)')),
                ('style_para_line_spacing_rule', models.CharField(blank=True, choices=[('SINGLE (0)', '单倍行距'), ('ONE_POINT_FIVE (1)', '1.5倍行距'), ('DOUBLE (2)', '双倍行距'), ('MULTIPLE (5)', '多倍行距')], default='', max_length=200, verbose_name='行距规则')),
                ('style_para_line_spacing', models.CharField(blank=True, choices=[('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], default='', max_length=200, verbose_name='行距(行)')),
                ('style_page_break_before', models.BooleanField(default=False, verbose_name='段前分页')),
                ('style_keep_with_next', models.BooleanField(default=False, verbose_name='与下段同页')),
                ('style_keep_together', models.BooleanField(default=False, verbose_name='段中不分页')),
                ('style_widow_control', models.BooleanField(default=False, verbose_name='孤行控制')),
                ('image_op', models.BooleanField(default=False, verbose_name='考查图片插入？')),
                ('image_position_style', models.CharField(choices=[('嵌入文本行中', '嵌入文本行中')], default='嵌入文本行中', max_length=20, verbose_name='位置类型')),
                ('image_width', models.CharField(blank=True, choices=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35')], default='', max_length=200, verbose_name='图像宽(厘米)')),
                ('image_height', models.CharField(blank=True, choices=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35')], default='', max_length=200, verbose_name='图像高(厘米)')),
                ('upload_image_file', models.FileField(blank=True, null=True, upload_to='uploads_image/', validators=[polls.wordFileModels.validate_image], verbose_name='上传图片')),
                ('table_op', models.BooleanField(default=False, verbose_name='考查表格插入？')),
                ('table_alignment', models.CharField(choices=[('None', '左对齐'), ('CENTER (1)', '居中'), ('RIGHT (2)', '右对齐')], default='', max_length=10, verbose_name='对齐方式')),
                ('table_autofit', models.BooleanField(default=False, verbose_name='表格宽度自动调整？')),
                ('table_style', models.CharField(choices=[('Grid Table Light', '网格型浅色'), ('Plain Table 3', '无格式表格3'), ('Grid Table 2 Accent 1', '网格表2着色1'), ('Grid Table 2 Accent 1', '网格表5深色'), ('List Table 1 Light', '清单表1浅色'), ('List Table 6 Colorful', '清单表6彩色')], default='', max_length=30, verbose_name='表格样式')),
                ('word_question', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='polls.wordquestion', verbose_name='word操作大题')),
            ],
            options={
                'verbose_name': 'Word操作列表',
                'verbose_name_plural': 'Word操作列表',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=50, verbose_name='班级')),
                ('name', models.CharField(max_length=50, verbose_name='姓名')),
                ('student_id', models.CharField(max_length=50, verbose_name='学号')),
                ('exampage_list', models.CharField(max_length=50, verbose_name='试卷列表')),
                ('exam_info', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='polls.exam', verbose_name='考试编号(考试登录时填写)')),
            ],
            options={
                'verbose_name': '考生',
                'verbose_name_plural': '考生',
            },
        ),
    ]
