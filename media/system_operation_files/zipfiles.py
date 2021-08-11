import os
from zipfile import ZipFile


def clean_subpath(base_len, path):
    arch_name = path[base_len:]
    while len(arch_name) and (arch_name[0]=='\\' or arch_name[0]=='/'):
        arch_name = arch_name[1:]
    return arch_name

## base_path/dir_name  ---->  zipfile_name
def folder2zip(base_path, dir_name, zipfile_name):
    base_len = len(base_path)
    folder = os.path.join(base_path, dir_name)
    with ZipFile(zipfile_name, 'w') as zfile:           
        for foldername, subfolders, files in os.walk(folder):   #遍历文件夹
            zfile.write(foldername, clean_subpath(base_len,foldername))
            for i in files:
                filename = os.path.join(foldername,i)
                zfile.write(filename, clean_subpath(base_len,filename))
        print('add zipfile {}'.format(zipfile_name))

dir_name = 'exam_system_operation'
base_path = os.path.abspath('./1')
zipfile_name = dir_name+'.zip'   
folder2zip(base_path, dir_name, zipfile_name)

# with ZipFile(zipfile_name) as myzip:
#     myzip.extractall('./4')

# for foldername, subfolders, files in os.walk(folder):
#     print(foldername, subfolders)
#     print(files)