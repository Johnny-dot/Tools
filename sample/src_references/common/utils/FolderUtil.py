import shutil
import os
import errno
import stat
import time
import datetime

def exists(url):
    return os.path.exists(url)

def join(url, *args):
    return os.path.join(url, *args)

# 新建
def create(url):
    delete(url)
    os.makedirs(url)

def createSafely(url):
    if not exists(url):
        os.makedirs(url)

# 删除指定的路径
def delete(url):
    def remove_readonly(func, path, execinfo):
        e = execinfo[1]
        if e.errno == errno.ENOENT or not os.path.exists(path):
            return
        if e.errno == errno.EACCES:
            time.sleep(1)
            os.chmod(path, stat.S_IWRITE)
            func(path)
        elif e.errno == errno.EACCES or e.errno == errno.EBUSY:
            retries = 5
            for _ in range(retries):
                try:
                    time.sleep(1)
                    func(path)
                    break
                except PermissionError:
                    continue
            else:
                print(f"Failed to delete {path} after {retries} retries.")
    if os.path.exists(url):
        shutil.rmtree(url, onerror=remove_readonly)

def move(sUrl, tUrl):
    print(f"Moving {sUrl} to {tUrl}")
    shutil.move(str(sUrl), str(tUrl))

# 复制文件或目录到目标路径
def copy(sUrl, tUrl, progressCb=None):
    if not os.path.isabs(tUrl):
        tUrl = os.path.abspath(tUrl)
    print('copy %s to %s' % (sUrl, tUrl))

    def _copy_progress(src, dst):
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)  # 在目标目录存在时继续
        else:
            shutil.copy2(src, dst)
        if progressCb:
            _copy_progress.completed += 1
            progressCb(_copy_progress.total, _copy_progress.completed)

    _copy_progress.completed = 0
    _copy_progress.total = sum([len(files) for _, _, files in os.walk(sUrl)]) if os.path.isdir(sUrl) else 1

    if os.path.isdir(sUrl):
        shutil.copytree(sUrl, tUrl, copy_function=_copy_progress, dirs_exist_ok=True)
    else:
        _copy_progress(sUrl, tUrl)

# 获取某个路径下所有的文件信息
def getFilesInfo(rootDir):
    filesDict = {}
    for root, dirs, files in os.walk(rootDir):
        for file in files:
            filesDict[file] = os.path.join(root, file)
    return filesDict

# 获取路径的相关信息
def getUrlInfo(url):
    filename_noext, ext = os.path.splitext(url)
    path, filename = os.path.split(url)
    drivesign, path_splitdrive = os.path.splitdrive(path)

    return filename, path, filename_noext, ext, path_splitdrive, drivesign

def isDir(url):
    return os.path.isdir(url)

# 获取文件的上次修改时间
def getLastModifiedTime(url):
    if exists(url):
        # 获取上次修改时间并格式化为可读形式
        timestamp = os.path.getmtime(url)
        last_modified_time = datetime.fromtimestamp(timestamp)
        return last_modified_time.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return None
