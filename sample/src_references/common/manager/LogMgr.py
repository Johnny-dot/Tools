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

import threading

def Singleton(cls):
    _instance = {}
    _lock = threading.Lock()

    def _singleton(*args, **kargs):
        with _lock:
            if cls not in _instance:
                _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@Singleton
class LogMgr(Manager.Manager):
    def __init__(self, loggerWidget) -> None:
        super().__init__()
        self._lock = threading.Lock()
        nowdate = time.strftime("%y%m%d", time.localtime())
        self._loggers = {}
        self._logDir = os.path.abspath(LOG_PATH + nowdate)
        self._formatter = logging.Formatter(LOG_FORMAT)
        self._loggerWidget = loggerWidget


    def getLog(self, uniqueKey):
        return FileUtil.readFile(self.getLogUrl(uniqueKey))

    def getLogUrl(self, uniqueKey):
        type_ = uniqueKey.split('-')[0]
        id_ = uniqueKey.split('-')[1]
        return os.path.join(self._logDir, type_, f'{id_}.log')

    def getLogger(self, uniqueKey, logLevel=LOG_LEVEL):
        with self._lock:
            if uniqueKey in self._loggers:
                return self._loggers[uniqueKey]

            # 创建 Logger
            logger = logging.getLogger(uniqueKey)
            logger.setLevel(logLevel)
            logger.propagate = False  # 防止日志向上传播
            self._loggers[uniqueKey] = logger

        # 检查是否已经添加过 Handler
        if not logger.handlers:
        # 输出到控制台
            if LOG_ENABLED and LOG_TO_CONSOLE:
                stream_handler = logging.StreamHandler(sys.stdout)
                stream_handler.setFormatter(self._formatter)
                logger.addHandler(stream_handler)

            # 输出到文件
            if LOG_ENABLED and LOG_TO_FILE:
                # 添加 FileHandler
                type = uniqueKey.split('-')[0]
                if not FolderUtil.exists(self._logDir+'/'+type):
                    FolderUtil.create(self._logDir+'/'+type)
                file_handler = logging.FileHandler(self.getLogUrl(uniqueKey), encoding='utf-8')
                file_handler.setFormatter(self._formatter)
                logger.addHandler(file_handler)

            # 输出到QT日志
            if self._loggerWidget:
                self._loggerWidget.setFormatter(self._formatter)
                logger.addHandler(self._loggerWidget)

            return self._loggers[uniqueKey]


