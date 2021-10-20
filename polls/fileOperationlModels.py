import os
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html, format_html_join

import re
import shutil
import zipfile
from pathlib import Path
from .ziptools import *
import win32con 
import win32api 

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT  = BASE_DIR / 'media'

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

Modify_Folder_A_Choice = [
    ('modify1', 'modify1'),
    ('modify2', 'modify2'),
    ('modify3', 'modify3'),
    ('modify4', 'modify4'),
    ('modify5', 'modify5'),
]

Modify_File_B_Choice = [
    ('modx1.txt', 'modx1.txt'),
    ('modx2.dat', 'modx2.dat'),
    ('modx3.txt', 'modx3.txt'),
    ('modx4.md', 'modx4.md'),
]

Modify_File_Attr_Choice = [
    ('只读','只读'),
    ('隐藏','隐藏'),
    ('只读和隐藏','只读和隐藏'),
]


Rename_Folder_A_Choice = [
    ('rename1001', 'rename1001'),
    ('rename2001', 'rename2001'),
    ('rename3001', 'rename3001'),
    ('rename4001', 'rename4001'),
]

Rename_File_B_Choice = [
    ('origin2021.txt', 'origin2021.txt'),
    ('origin2025.md', 'origin2025.md'),
    ('origin2031.dat', 'origin2031.dat'),
    ('origin2050.c', 'origin2050.c'),
    ('origin2091.js', 'origin2091.js'),
]
Rename_File_C_Choice = [
    ('des2021.txt', 'des2021.txt'),
    ('des2025.md', 'des2025.md'),
    ('des2031.dat', 'des2031.dat'),
    ('des2050.c', 'des2050.c'),
    ('des2091.js', 'des2091.js'),
]

Copy_Folder_A_Choice = [
    ('source999', 'source999'),
    ('source777', 'source777'),
    ('source666', 'source666'),
]
Copy_File_B_Choice = [
    ('copy2021.txt', 'copy2021.txt'),
    ('copy2025.md', 'copy2025.md'),
    ('copy2031.dat', 'copy2031.dat'),
    ('copy2050.c', 'copy2050.c'),
    ('copy2091.js', 'copy2091.js'),
]
Copy_Folder_C_Choice = [
    ('XXXX999', 'XXXX999'),
    ('UUUUU777', 'UUUUU777'),
    ('MMMMM666', 'MMMMM666'),
]
Copy_Or_Move_Choice = [
    ('复制', '复制'),
    ('移动', '移动'),
]


################文件或文件夹操作
class FileOperationQuestion(models.Model):
    # 控制 表项显示文字，默认按 类名object（n）显示
    def __str__(self):
        return '操作系统' + str(self.id) #题目序号

    # 内部标签，项目显示名  项目详细名等
    class Meta:
        verbose_name_plural = '题目-操作系统'  # 项目名
        verbose_name = '题目-操作系统'  # 详细名称


    def base_path_(self):
        return os.path.join(MEDIA_ROOT, 'system_operation_files',str(self.id))

    def zipfile_path_(self):
        return os.path.join(MEDIA_ROOT, 'system_operation_files',str(self.id),'exam_system_operation.zip')
    zipfile_path_.short_description='生成文件地址' 

    def upload_path_(self):
        return os.path.join(MEDIA_ROOT, 'upload_system_operations')

    #题目内容
    def question_content(self):
        result_list = []
        result_list.append('在文件夹下创建新文件夹'+self.new_folder_dir_A+'，并在此文件夹中新建文件'+self.new_file_B+'。')
        result_list.append('在文件夹下'+self.del_folder_A+'/'+self.del_folder_B+'文件夹中，删除文件'+self.del_file_C+'。')
        result_list.append('将文件夹下'+self.modify_folder_A+'中的文件'+self.modify_file_B+'的属性修改为'+self.modify_file_attr+'。')
        result_list.append('将文件夹下' + self.rename_folder_A + '中文件' + self.rename_file_B+'重命名为'+self.rename_file_C+'。')
        result_list.append('将文件夹下'+self.copy_folder_A+'中的文件'+self.copy_file_B+self.copy_or_move+'到文件夹'+self.copy_folder_C+'。')
        return format_html("<ol>") + \
                format_html_join(
                '\n', '<li style="color:black;">{}</li>',
                ((x,) for x in result_list)
                ) \
                + format_html("</ol>")
    question_content.short_description = '题目内容'

    def score_(self, answer_folder_path):
        result_list = []
        ## check the files
        if answer_folder_path and os.path.exists(answer_folder_path):
            
            ## create file
            targeted_path = os.path.join(answer_folder_path, self.new_folder_dir_A)
            targeted_file = os.path.join(answer_folder_path, self.new_folder_dir_A, self.new_file_B)
            result = ''
            if os.path.exists(targeted_file):
                result = (self.new_file_B)
            result_list.append(result)


            ## delete file
            targeted_path = os.path.join(answer_folder_path, self.del_folder_A, self.del_folder_B)
            targeted_file = os.path.join(answer_folder_path, self.del_folder_A, self.del_folder_B, self.del_file_C)
            result = ''
            if os.path.exists(targeted_path) and (not os.path.exists(targeted_file)):
                result = (self.del_file_C)
            result_list.append(result)


            ## modify file
            targeted_file = os.path.join(answer_folder_path, self.modify_folder_A, self.modify_file_B)
            result = ''
            if os.path.exists(targeted_file):
                attr = win32api.GetFileAttributes(targeted_file)
                is_read_only = attr & win32con.FILE_ATTRIBUTE_READONLY
                is_hidden = attr & win32con.FILE_ATTRIBUTE_HIDDEN
                print(is_read_only, is_hidden)
                if self.modify_file_attr == Modify_File_Attr_Choice[0][0] and is_read_only:
                    result = self.modify_file_B+'-is_read_only'
                elif self.modify_file_attr == Modify_File_Attr_Choice[1][0] and is_hidden:
                    result = self.modify_file_B+'-is_hidden'
                elif self.modify_file_attr == Modify_File_Attr_Choice[2][0] and is_read_only and is_hidden:
                    result = self.modify_file_B+'-is_hidden-is_read_only'
                result = self.modify_file_B+'-is_hidden-is_read_only'
            result_list.append(result)

            ## rename file
            targeted_file_1 = os.path.join(answer_folder_path, self.rename_folder_A, self.rename_file_B)
            targeted_file_2 = os.path.join(answer_folder_path, self.rename_folder_A, self.rename_file_C)
            result = ''
            if os.path.exists(targeted_file_2):
                result = self.rename_file_C
            result_list.append(result)

            ## cp or mv file
            targeted_file_1 = os.path.join(answer_folder_path, self.copy_folder_A, self.copy_file_B)
            targeted_file_2 = os.path.join(answer_folder_path, self.copy_folder_C, self.copy_file_B)
            result = ''
            if os.path.exists(targeted_file_2):
                result = (self.copy_file_B)
            result_list.append(result)
        return result_list

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  
        dir_path = self.base_path_()
        files_path = os.path.join(dir_path,'exam_system_operation')
        print(dir_path)
        if dir_path:
            if os.path.exists(dir_path): shutil.rmtree(dir_path)

            os.makedirs(files_path)

            ## del
            del_path = os.path.join(files_path, self.del_folder_A, self.del_folder_B)
            del_file = os.path.join(files_path, self.del_folder_A, self.del_folder_B, self.del_file_C)
            os.makedirs(del_path)
            with open(del_file,'w') as f:
                f.write('file for del operation\n')

            ## modify
            modify_path = os.path.join(files_path, self.modify_folder_A)
            modify_file = os.path.join(files_path, self.modify_folder_A, self.modify_file_B)
            os.makedirs(modify_path)
            with open(modify_file, 'w') as f:
                f.write('file for modify operation\n')

            ## rename
            rename_path = os.path.join(files_path, self.rename_folder_A)
            rename_file = os.path.join(files_path, self.rename_folder_A, self.rename_file_B)
            os.makedirs(rename_path)
            with open(rename_file, 'w') as f:
                f.write('file for rename operation\n')

            ## copy or move
            cp_path_A = os.path.join(files_path, self.copy_folder_A)
            cp_path_C = os.path.join(files_path, self.copy_folder_C)
            cp_file = os.path.join(files_path, self.copy_folder_A, self.copy_file_B)
            os.makedirs(cp_path_A)
            os.makedirs(cp_path_C)
            with open(cp_file, 'w') as f:
                f.write('file for copy or move operation\n')

            zip_path = self.zipfile_path_()
            if zip_path:
                if os.path.exists(zip_path): os.remove(zip_path)
                folder2zip(dir_path, 'exam_system_operation', zip_path)
            

    # 新建文件（夹）
    # 题目示例：在考生文件夹中创建文件夹[A]，并在[A]中新建文件[B]
    new_folder_dir_A = models.CharField('文件夹[A]', choices=New_Folder_Name_Choice, max_length=20,  default='')
    new_file_B = models.CharField('文件[B]', choices=New_File_Name_Choice, max_length=20,  default='')

    # 删除文件（夹）
    # 题目示例：在考生文件夹中删除[A]/[B]中的文件[C]
    del_folder_A = models.CharField('文件夹[A]', choices=Del_Folder_A_Choice, max_length=20,  default='')
    del_folder_B = models.CharField('文件夹[B]', choices=Del_Folder_B_Choice, max_length=20,  default='')
    del_file_C = models.CharField('文件[C]', choices=Del_File_C_Choice, max_length=20,  default='')
    
    # 修改文件（夹）属性
    # 题目示例：在[A]文件中，将[B]的属性修改为[D]
    modify_folder_A = models.CharField('文件夹[A]', choices=Modify_Folder_A_Choice, max_length=20,  default='')
    modify_file_B = models.CharField('文件[B]', choices=Modify_File_B_Choice, max_length=20,  default='')
    modify_file_attr = models.CharField('属性[C]', choices=Modify_File_Attr_Choice, max_length=20,  default='')
    
    # 重命名文件（夹）
    # 题目示例：在[A]文件中，将[B]重命名为[C]
    rename_folder_A = models.CharField('文件夹[A]', choices=Rename_Folder_A_Choice, max_length=20,  default='')
    rename_file_B = models.CharField('原文件名[B]', choices=Rename_File_B_Choice, max_length=20,  default='')
    rename_file_C = models.CharField('新文件名[C]', choices=Rename_File_C_Choice, max_length=20,  default='.txt')

    # 复制或移动
    # 题目示例：在[A]文件中[B]文件复制或移动到[C]文件夹中
    copy_folder_A = models.CharField('原文件夹[A]', choices=Copy_Folder_A_Choice, max_length=20,  default='')
    copy_file_B = models.CharField('文件[B]', choices=Copy_File_B_Choice, max_length=20,  default='')
    copy_folder_C = models.CharField('目标文件夹[C]', choices=Copy_Folder_C_Choice, max_length=20,  default='')
    copy_or_move = models.CharField('操作方法', choices=Copy_Or_Move_Choice, max_length=20,  default='')
    # folder_or_file_sea = models.CharField('[B]', choices=FolderAndFileName, max_length=20,  default='')
    # folder_or_filetype_sea = models.CharField('[C]', choices=FileType, max_length=20,  default='.txt')
    # folder_sea = models.CharField('[D]', choices=FolderAndFileName, max_length=20,  default='')
    