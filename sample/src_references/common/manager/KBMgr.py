
from sample.src_references.common.manager.Manager import Manager
import sample.src_references.common.utils.JsonUtil as JsonUtil

from PySide6.QtCore import QTimer

class KBMgr(Manager):
    def __init__(self) -> None:
        super().__init__()
        self._progress = {}
        self._timers = {}  # 存储每个进度的 QTimer
        self.branchesUrl = {}
        self._progressCallback = None
        self._proListCallback = None
        self._min_duration = 2  # 每个阶段的最小持续时间（秒）

    def setBranchUrl(self, name, url):
        branches = JsonUtil.readInCfg("branches") or {}
        branches[name] = url
        JsonUtil.saveInCfg("branches", branches)

    def getBranchUrl(self, name):
        branches = JsonUtil.readInCfg("branches") or {}
        path = branches.get(name)
        return path

    # 设置进度条回调
    def addGUIProCallback(self, progressCallback):
        self._progressCallback = progressCallback

    # 设置进度列表回调
    def addGUIProListCallback(self, proListCallback):
        self._proListCallback = proListCallback

    def registerProgress(self, uniqueKey, stages):
        if uniqueKey in self._progress:
            print(f"{uniqueKey} 已存在，跳过注册")
            return
        for stage in stages:
            stage.setdefault("percent", 0)
        self._progress[uniqueKey] = stages

        # 创建定时器并启动平滑更新
        self._timers[uniqueKey] = QTimer()
        self._timers[uniqueKey].timeout.connect(lambda: self._simulateProgress(uniqueKey))
        self._timers[uniqueKey].start(50)  # 每 50 毫秒更新一次

    def getProgressNum(self, uniqueKey):
        stages = self._progress.get(uniqueKey) or []
        total_rate = sum(stage['rate'] for stage in stages)
        percent = sum(stage['percent'] for stage in stages)
        if total_rate > 0:
            percent = (percent / total_rate) * 100  # 转换为百分比
        return percent

    def getProListInfo(self, uniqueKey):
        stages = self._progress.get(uniqueKey) or []
        return stages

    def _simulateProgress(self, uniqueKey):
        stages = self._progress.get(uniqueKey, [])
        current_index = len(stages)  # 初始化为阶段总数，假定所有阶段已完成

        for index, stage in enumerate(stages):
            if stage['percent'] < stage['rate']:
                current_index = index
                break

        # 如果所有阶段完成，停止定时器
        if current_index >= len(stages):
            self._timers[uniqueKey].stop()  # 停止定时器
            self._timers.pop(uniqueKey, None)  # 删除定时器引用
            if self._progressCallback:
                self._progressCallback(100)  # 确保进度显示为100%
            return

        stage = stages[current_index]
        stage['percent'] = min(stage['percent'] + 0.5, stage['rate'])

        if self._progressCallback:
            self._progressCallback(self.getProgressNum(uniqueKey))

    def onProgressUpdated(self, uniqueKey, index):
        """更新阶段完成后的逻辑进度"""
        stages = self._progress.get(uniqueKey)
        if index < len(stages):
            stage = stages[index]
            stage['percent'] = stage['rate']  # 将阶段进度直接调整为目标
            if self._proListCallback:
                self._proListCallback(stage['msg'])

# 模块级单例
KBMgr = KBMgr()
