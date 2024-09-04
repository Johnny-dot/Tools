import tkinter
from tkinter import filedialog

import sample.src_references.common.g.G as G

root = tkinter.Tk()
root.withdraw()


def inputWithMsg(msg):
    inputPara = input(msg)
    return inputPara

def InPutDirectory():
    if G._GUI:
        f_path = InPutDirectoryGUI()
    else:
        msg = '请输入文件夹路径'
        f_path = inputWithMsg(msg)

    return f_path

def InPutDirectoryGUI():
    return filedialog.askdirectory()

def InPutFilePathGUI():
    return filedialog.askopenfilename()