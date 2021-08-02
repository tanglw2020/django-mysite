import os
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html, format_html_join

New_Folder_Name_Choice = [
    ('new12', 'new12'),
    ('new123', 'new123'),
    ('new2050', 'new2050'),
    ('new100', 'new100'),
    ('new101', 'new101'),
]

New_File_Name_Choice  = [
    ('nf11.txt', 'nf11.txt'),
    ('nf22.md', 'nf22.md'),
    ('nf33.dat', 'nf33.dat'),
    ('nf44.txt', 'nf44.txt'),
    ('nf55.cmd', 'nf55.cmd'),
]

Del_Folder_A_Choice = [
    ('dela4567', 'dela4567'),
    ('dela45', 'dela45'),
    ('delart', 'delart'),
    ('delavv', 'delavv'),
    ('delaxx', 'delaxx'),
    ('delacv', 'delacv'),
]

Del_Folder_B_Choice = [
    ('delb88', 'delb88'),
    ('delb77', 'delb77'),
    ('delbnn', 'delbnn'),
    ('delbmm', 'delbmm'),
    ('delbdd', 'delbdd'),
]

Del_File_C_Choice = [
    ('delfgg.txt', 'delfgg.txt'),
    ('delfww.dat', 'delfww.dat'),
    ('delfqq.txt', 'delfqq.txt'),
    ('delfzz.md', 'delfzz.md'),
]

################文件或文件夹操作
class FileOperationQuestion(models.Model):
    # 控制 表项显示文字，默认按 类名object（n）显示
    def __str__(self):
        return '文件操作题' + str(self.id) #题目序号

    # 内部标签，项目显示名  项目详细名等
    class Meta:
        verbose_name_plural = '文件操作题'  # 项目名
        verbose_name = '文件操作'  # 详细名称

    #包含小题数量
    def question_num(self):
        return 5
    question_num.short_description='小题数量'
    #题目内容
    def question_content(self):
        result_list = []
        result_list.append('在考生文件夹下的'+self.new_folder_dir_A+'文件夹中，新建文件'+self.new_file_B)
        result_list.append('在考生文件夹下的'+self.del_folder_A+'/'+self.del_folder_B+'文件夹中，删除文件'+self.del_file_C)
        # result_list.append('在考生文件夹下的'+self.folder_dir_ren+'文件夹中，将'+self.folder_or_file_ren+self.folder_or_filetype_ren+'重命名为'+self.folder_or_file_rendes+self.folder_or_filetype_rendes)
        # result_list.append('在考生文件夹下的' + self.folder_dir_mod + '文件夹中，将' + self.folder_or_file_mod + self.folder_or_filetype_mod+'的属性修改为'+self.folder_file_attmod)
        # result_list.append('在考生文件夹下的'+self.folder_dir_sea+'文件夹中，搜索'+self.folder_or_file_sea+self.folder_or_filetype_sea+'并将它复制到考生文件夹下的'+self.folder_sea+'文件中')
        # result_list.append('在考生文件夹下的'+self.folder_dir_cp+'文件夹中，将'+self.folder_or_file_cp+self.folder_or_filetype_cp+self.operation_cp+'到考生文件夹下的'+self.folder_cp+'文件夹中')

        return format_html("<ol>") + \
                format_html_join(
                '\n', '<li style="color:black;">{}</li>',
                ((x,) for x in result_list)
                ) \
                + format_html("</ol>")
    question_content.short_description = '题目内容'

    #新建文件（夹）
    # （题目示例：在考生文件夹中创建文件夹[A]，并在[A]中新建文件[B]）
    new_folder_dir_A = models.CharField('文件夹[A]', choices=New_Folder_Name_Choice, max_length=20,  default='')
    new_file_B = models.CharField('文件[B]', choices=New_File_Name_Choice, max_length=20,  default='')

    # 删除文件（夹）
    # （题目示例：在考生文件夹中删除[A]/[B]中的文件[C]）
    del_folder_A = models.CharField('文件夹[A]', choices=Del_Folder_A_Choice, max_length=20,  default='')
    del_folder_B = models.CharField('文件夹[B]', choices=Del_Folder_B_Choice, max_length=20,  default='')
    del_file_C = models.CharField('文件[C]', choices=Del_File_C_Choice, max_length=20,  default='')
    # 重命名文件（夹）
    # # isrenamefile = models.BooleanField('是否考查重命名文件（夹）？（题目示例：在[A]文件中，将[B][C]重命名为[D][E]）', default=True)
    # folder_dir_ren = models.CharField('[A]', choices=FolderAndFileName, max_length=20,  default='')
    # folder_or_file_ren = models.CharField('[B]', choices=FolderAndFileName, max_length=20,  default='')
    # folder_or_filetype_ren = models.CharField('[C]', choices=FileFolderType, max_length=20,  default='.txt')
    # folder_or_file_rendes = models.CharField('[D]', choices=FolderAndFileName, max_length=20,  default='')
    # folder_or_filetype_rendes = models.CharField('[E]', choices=FileFolderType, max_length=20,  default='.txt')
    # # 修改文件（夹）属性
    # # ismodifyfile = models.BooleanField('是否考查修改文件（夹）属性？（题目示例：在[A]文件中，将[B][C]的属性修改为[D]）', default=True)
    # folder_dir_mod = models.CharField('[A]', choices=FolderAndFileName, max_length=20,  default='')
    # folder_or_file_mod = models.CharField('[B]', choices=FolderAndFileName, max_length=20,  default='')
    # folder_or_filetype_mod = models.CharField('[C]', choices=FileFolderType, max_length=20,  default='.txt')
    # folder_file_attmod = models.CharField('[D]', choices=Attribute, max_length=20,  default='只读')
    # #搜索文件并复制
    # # issearchfile = models.BooleanField('是否考查搜索文件并复制？（题目示例：在[A]文件中，搜索[B][C]文件，并将[B]文件复制到[D]文件夹中）', default=True)
    # folder_dir_sea = models.CharField('[A]', choices=FolderAndFileName, max_length=20,  default='')
    # folder_or_file_sea = models.CharField('[B]', choices=FolderAndFileName, max_length=20,  default='')
    # folder_or_filetype_sea = models.CharField('[C]', choices=FileType, max_length=20,  default='.txt')
    # folder_sea = models.CharField('[D]', choices=FolderAndFileName, max_length=20,  default='')
    # #复制、移动文件（夹）
    # # iscopyfile = models.BooleanField('是否考查搜复制、移动操作？（题目示例：在[A]文件中，将[B][C]，[D]到[E]文件夹中）', default=True)
    # folder_dir_cp = models.CharField('[A]', choices=FolderAndFileName, max_length=20,  default='')
    # folder_or_file_cp = models.CharField('[B]', choices=FolderAndFileName, max_length=20,  default='')
    # folder_or_filetype_cp = models.CharField('[C]', choices=FileType, max_length=20,  default='.txt')
    # operation_cp = models.CharField('[D]', choices=OperationType, max_length=20,  default='复制')
    # folder_cp = models.CharField('[E]', choices=FolderAndFileName, max_length=20,  default='')
