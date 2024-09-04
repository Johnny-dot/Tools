import os
import sample.src_references.common.utils.FolderUtil as FolderUtil

def writeDic(tDict, saveUrl, pattern):
    path = FolderUtil.getUrlInfo(saveUrl)[1]
    if not FolderUtil.exists(path):
        FolderUtil.createSafely(path)

    line = ''
    try:
        with open(saveUrl, 'w', encoding='utf-8') as file:
            for k,v in tDict.items():
                if not pattern:
                    pattern = '%s = "%s"\n'
                line = line + pattern%(k,v)
            file.write(line)
    except IOError as error:
        print(error)
        print('写文件时发生错误!')

def writeStr(str, saveUrl):
    path = FolderUtil.getUrlInfo(saveUrl)[1]
    if not FolderUtil.exists(path):
        FolderUtil.createSafely(path)

    try:
        with open(saveUrl, 'w', encoding='utf-8') as file:
            file.write(str)
    except IOError as error:
        print(error)
        print('写文件时发生错误!')

def readFile(url):
    lines = []
    try:
        with open(url, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except IOError as error:
        print(error)
        print('读取文件时发生错误!')
    return lines

import os

import os

def check_lowercase_filenames(directory_path, ignore_extensions=None):
    if ignore_extensions is None:
        ignore_extensions = []

    non_compliant_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension in ignore_extensions:
                continue  # 忽略指定类型的文件

            if not file.islower():
                non_compliant_files.append(os.path.join(root, file))

    if non_compliant_files:
        return False, non_compliant_files
    return True, []


