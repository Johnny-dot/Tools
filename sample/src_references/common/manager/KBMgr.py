from sample.src_references.common.manager.Manager import Manager
import sample.src_references.common.utils.InputUtil as InputUtil
import sample.src_references.common.utils.JsonUtil as JsonUtil

import threading
import time


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*kargs, **kargs)
        return _instance[cls]

    return _singleton


@Singleton
class KBMgr(Manager):
    def __init__(self) -> None:
        super().__init__()
        self.branchesUrl = {}
        self._progress = {}
        self._progressCallback = None
        self._proListCallback = None
        self._running = {}
        self._threads = {}
        self._min_duration = 2  # 设置每个阶段的最小持续时间（秒）

    def setBranchUrl(self, name, url):
        # self.branchesUrl[name] = url
        branches = JsonUtil.readInCfg("branches") or {}
        branches[name] = url
        JsonUtil.saveInCfg("branches", branches)

    def getBranchUrl(self, name):
        branches = JsonUtil.readInCfg("branches") or {}
        path = branches.get(name)
        return path
        # if name not in self.branchesUrl:
            # if path:
            #     return path
        #     else:
        #         url = InputUtil.InPutDirectory()
        #         JsonUtil.saveInCfg(name, url)
        #     self.setBranchUrl(name, url)
        # return self.branchesUrl[name]

    # 进度条
    def addGUIProCallback(self, progressCallback):
        self._progressCallback = progressCallback

    # 进度列表
    def addGUIProListCallback(self, proListCallback):
        self._proListCallback = proListCallback

    def registerProgress(self, uniqueKey, stages):
        if not self._progress.get(uniqueKey):
            # 初始化每个阶段的percent为0
            for stage in stages:
                stage['percent'] = 0
            self._progress[uniqueKey] = stages
            # self._running[uniqueKey] = True
            # self._threads[uniqueKey] = threading.Thread(target=self._simulateProgress, args=(uniqueKey,))
            # self._threads[uniqueKey].start()
        else:
            print(uniqueKey, '重复的进度id')

    def onProgressUpdated(self, uniqueKey, index):
        # 停止当前阶段的假进度更新
        self._running[uniqueKey] = False

        stages = self.getProListInfo(uniqueKey)
        if self._proListCallback:
            self._proListCallback(stages[index]['msg'])

        # 启动下一个阶段的假进度更新
        # if index < len(stages) - 1:
        #     self._running[uniqueKey] = True
        #     self._threads[uniqueKey] = threading.Thread(target=self._simulateProgress, args=(uniqueKey,))
        #     self._threads[uniqueKey].start()
        # else:
        #     self._running[uniqueKey] = False
        #     # 确保在最后一个阶段完成后，进度为100%
        #     if self._progressCallback:
        #         self._progressCallback(100)

    def getProgressNum(self, uniqueKey):
        stages = self.getProgress(uniqueKey) or []
        total_rate = sum(stage['rate'] for stage in stages)
        percent = sum(stage['percent'] for stage in stages)
        if total_rate > 0:
            percent = (percent / total_rate) * 100  # 转换为百分比
        return percent

    def getProgress(self, uniqueKey):
        return self._progress.get(uniqueKey)

    # 进度列表
    def getProListInfo(self, uniqueKey):
        stages = self.getProgress(uniqueKey) or []
        return stages

    def _simulateProgress(self, uniqueKey):
        stages = self.getProgress(uniqueKey)
        current_index = 0
        while self._running[uniqueKey] and current_index < len(stages):
            stage = stages[current_index]
            target_rate = stage['rate'] + self.getProgressNum(uniqueKey) - sum(
                s['percent'] for s in stages[:current_index])
            start_time = time.time()
            while self._running[uniqueKey] and stage['percent'] < stage['rate']:
                stage['percent'] = min(stage['rate'], stage['percent'] + 0.01)
                if self._progressCallback:
                    self._progressCallback(self.getProgressNum(uniqueKey))
                time.sleep(0.1)

            # 确保每个阶段至少运行 _min_duration 秒
            elapsed_time = time.time() - start_time
            if elapsed_time < self._min_duration:
                time.sleep(self._min_duration - elapsed_time)

            current_index += 1

    def stopProgress(self, uniqueKey):
        self._running[uniqueKey] = False
