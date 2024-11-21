import os
import sys
import threading
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
LOG_FORMAT = '%(levelname)s - %(asctime)s - --[%(message)s]-- - %(filename)s - %(lineno)d'

class LogMgr(Manager.Manager):
    def __init__(self) -> None:
        super().__init__()
        self._lock = threading.Lock()
        nowdate = time.strftime("%y%m%d", time.localtime())
        self._loggers = {}
        self._logDir = os.path.abspath(LOG_PATH + nowdate)
        self._formatter = logging.Formatter(LOG_FORMAT)

    def setLoggerWidget(self, loggerWidget):
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
                type_ = uniqueKey.split('-')[0]
                if not FolderUtil.exists(self._logDir + '/' + type_):
                    FolderUtil.create(self._logDir + '/' + type_)
                file_handler = logging.FileHandler(self.getLogUrl(uniqueKey), encoding='utf-8')
                file_handler.setFormatter(self._formatter)
                logger.addHandler(file_handler)

            # 输出到QT日志
            if self._loggerWidget:
                self._loggerWidget.setFormatter(self._formatter)
                logger.addHandler(self._loggerWidget)

        return self._loggers[uniqueKey]


# 模块级单例
LogMgr = LogMgr()
