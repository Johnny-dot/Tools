from hashlib import md5

# 文件树快照
def fileTreeSnapshot(filesDict):
    tDict = {}
    for key, val in filesDict.items():
        md5v = generateMD5(val)
        lastone = val.split('\\')
        if tDict.get(lastone[-1]) == None:
            tDict[lastone[-1]] = {}

        tDict[lastone[-1]]["md5"] = md5v
        tDict[lastone[-1]]["path"] = val
    return tDict

def generateMD5(file):
    m = md5()
    try:
        with open(file, 'rb') as f:
            m.update(f.read())
            m.hexdigest()
            return m.hexdigest()
    except FileNotFoundError:
        print('无法打开指定的文件!')