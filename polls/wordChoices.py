

FONT_NAME_ASCII_CHOICES = [
    ('MS Gothic', 'MS Gothic'),
    ('MS Mincho', 'MS Mincho'),
    ('Yu Gothic', 'Yu Gothic'),
    ('Arial Black', 'Arial Black'),
    ('Bahnschrift', 'Bahnschrift'),
    ('Book Antiqua', 'Book Antiqua'),
    ('Calibri', 'Calibri'),
    ('Dubai', 'Dubai'),
    ('Impact', 'Impact'),
]

FONT_NAME_CHINESE_CHOICES = [
    ('宋体', '宋体'),
    ('黑体', '黑体'),
    ('华文仿宋', '华文仿宋'),
    ('楷体', '楷体'),
    ('幼圆', '幼圆'),
    ('微软雅黑', '微软雅黑'),
    ('隶书', '隶书'),
]

# FONT_SIZE_CHOICES = [
#     ('一号','一号' ),
#     ('小一','小一' ),
#     ('二号','二号' ),
#     ('小二','小二' ),
#     ('三号','三号' ),
#     ('小三','小三' ),
#     ('四号','四号' ),
#     ('小四','小四' ),
#     ('五号','五号' ),
#     ('小五','小五' ),
#     ('六号','六号' ),
#     ('小六','小六' ),
#     ('七号','七号' ),
#     ('小七','小七' ),
#     ('八号','八号' ),
#     ('小八','小八' ),
# ]

FONT_SIZE_CHOICES = [
    ('5','5' ),
    ('8','8' ),
    ('10','10' ),
    ('12','12' ),
    ('14','14' ),
    ('18','18' ),
    ('22','22' ),
    ('26','26' ),
    ('36','36' ),
    ('48','48' ),
    ('72','72' ),
]

FONT_COLOR_CHOICES = [
    ('红色', '红色'),
    ('黄色', '黄色'),
    ('绿色', '绿色'),
]

FONT_UNDERLINE_CHOICES = [
    ('True', '普通下划线'),
    ('DOUBLE (3)', '双下划线'),
    ('THICK (6)', '粗下划线'),
    ('WAVY (11)', '波浪下划线'),
]


PARA_ALIGNMENT_CHOICES = [
    ('LEFT (0)', '左对齐'),   ##  or 'None'
    ('CENTER (1)', '居中对齐'),
    ('RIGHT (2)', '右对齐'),
    ('JUSTIFY (3)', '两端对齐'),
    ('DISTRIBUTE (4)', '分散对齐'),
]

PARA_FIRST_LINE_INDENT_CHOICES = [
    ('首行缩进', '缩进'),
    ('首行悬挂', '悬挂'),
]

PARA_LINE_SPACING_RULE_CHOICES = [
    ('SINGLE (0)', '单倍行距'),
    ('ONE_POINT_FIVE (1)', '1.5倍行距'),
    ('DOUBLE (2)', '双倍行距'),
    # ('AT_LEAST (3)', '行距最小值'),   ##  单位 磅
    # ('EXACTLY (4)', '行距固定值'),    ##  单位 磅
    ('MULTIPLE (5)', '多倍行距'),
]

PARA_FIRSTCHARDROPCAP_CHOICES = [
    ('drop', '下沉'),
    ('margin', '悬挂'),
]

PARA_LINE_PAGE_CHOICES = [
    ('孤行控制', '孤行控制'),
    ('与下段同页', '与下段同页'),
    ('段中不分页', '段中不分页'),
    ('段前分页', '段前分页'),
]

STYLE_NAME_CHOICES = [
    ('标题1', '标题1'),
    ('标题2', '标题2'),
    ('标题3', '标题3'),
    ('标题4', '标题4'),
    ('强调', '强调'),
    ('列表编号', '列表编号'),
    ('列表项目符号', '列表项目符号'),
    ('新样式1', '新样式1'),
    ('新样式2', '新样式2'),
]

INDENT_NUM_CHOICES = [
    ('5','5'),
    ('10','10'),
    ('15','15'),
    ('20','20'),
    ('25','25'),
    ('30','30'),
    ('35','35'),
]

LINE_NUM_CHOICES = [
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
]


IMAGE_POSITION_STYLE_CHOICES = [
    ('嵌入文本行中','嵌入文本行中'),
]