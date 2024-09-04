import os
import sys
import time
import logging

import sample.src_references.common.utils.FolderUtil as FolderUtil
import sample.src_references.common.utils.FileUtil as FileUtil
import sample.src_references.common.manager.Manager as Manager

# 日志根目录
LOG_PATH = 'sample/log/'
# 日志级别
LOG_LEVEL = 'DEBUG'
# 是否开启日志
LOG_ENABLED = True
# 是否输出到控制台
LOG_TO_CONSOLE = True
# 是否输出到文件
LOG_TO_FILE = True
# 每条日志输出格式
# LOG_FORMAT = '%(levelname)s - %(asctime)s - process: %(process)d - %(filename)s - %(name)s - %(lineno)d - %(module)s - %(message)s'
# LOG_FORMAT = '%(levelname)s - %(asctime)s - --[%(message)s]-- - %(filename)s - %(lineno)d - %(module)s - %(name)s'
LOG_FORMAT = '%(levelname)s - %(asctime)s - --[%(message)s]-- - %(filename)s - %(lineno)d'

def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton

@Singleton
class LogMgr(Manager.Manager):
    def __init__(self, loggerWidget) -> None:
        super().__init__()
        nowdate = time.strftime("%y%m%d", time.localtime())
        self._loggers = {}
        self._logDir = os.path.abspath(LOG_PATH + nowdate)
        self._loggerWidget = loggerWidget


    def getLog(self, uniqueKey):
        return FileUtil.readFile(self.getLogUrl(uniqueKey))

    def getLogUrl(self, uniqueKey):
        type = uniqueKey.split('-')[0]
        id = uniqueKey.split('-')[1]
        return r'%s/%s/%s.log'%(self._logDir, type, id)

    def getLogger(self, uniqueKey):
        if self._loggers.get(uniqueKey):
            # self._logger = loggers[uniqueKey]
            return self._loggers[uniqueKey]

        logger = logging.getLogger(uniqueKey)
        logger.setLevel(LOG_LEVEL)
        self._loggers[uniqueKey] = logger

        # 输出到控制台
        if LOG_ENABLED and LOG_TO_CONSOLE:
            stream_handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(LOG_FORMAT)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

        # 输出到文件
        if LOG_ENABLED and LOG_TO_FILE:
            # 添加 FileHandler
            type = uniqueKey.split('-')[0]
            if not FolderUtil.exists(self._logDir+'/'+type):
                FolderUtil.create(self._logDir+'/'+type)
            file_handler = logging.FileHandler(self.getLogUrl(uniqueKey), encoding='utf-8')
            formatter = logging.Formatter(LOG_FORMAT)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        # 输出到QT日志
        if self._loggerWidget:
            formatter = logging.Formatter(LOG_FORMAT)
            self._loggerWidget.setFormatter(formatter)
            logger.addHandler(self._loggerWidget)

        return self._loggers[uniqueKey]


