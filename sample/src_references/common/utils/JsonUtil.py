import json
import os
from pathlib import Path

CFG = Path("sample/data/config.json")
PARAS = Path("sample/data/quicparas.json")

def writeDict(tDict, saveUrl):
    saveUrl = Path(saveUrl).resolve()
    json_str = json.dumps(tDict, indent=4)
    try:
        with open(saveUrl, 'w', encoding='utf-8') as json_file:
            json_file.write(json_str)
    except IOError as error:
        print(f"写文件时发生错误: {error}")

def readDict(saveUrl):
    saveUrl = Path(saveUrl).resolve()
    try:
        with open(saveUrl, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"文件不存在: {saveUrl}")
    except LookupError:
        print("指定了未知的编码!")
    except UnicodeDecodeError:
        print("读取文件时解码错误!")

def readCfg():
    return readDict(CFG)

def readInCfg(key):
    data = readCfg()
    return data.get(key)

def saveInCfg(key, val):
    data = readCfg()
    if data.get(key) != val:
        data[key] = val
        writeDict(data, CFG)

def read(path):
    return readDict(path)

def readIn(path, key):
    data = readDict(path)
    return data.get(key)

def saveIn(path, key, val):
    data = readDict(path)
    data[key] = val
    writeDict(data, path)

def deleteIn(path, key):
    if not key:
        return
    data = readDict(path)
    data.pop(key, None)
    writeDict(data, path)
