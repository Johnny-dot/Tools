import sample.src_references.common.g.G as G
import sample.src_references.common.utils.JsonUtil as JsonUtil
import sample.src_references.common.utils.FolderUtil as FolderUtil
import sample.src_references.common.utils.TerminalUtil as TerminalUtil
from pathlib import Path
import os


class GMSerialize:
    _cfg = None  # 缓存配置文件

    def __init__(self, kb_vo) -> None:
        self.vo = kb_vo
        self.errors = []
        self.kbMgr = G.getG("KBMgr")
        self._uniqueKey = self.vo.getUniqueKey()
        self.workPath = self._load_config().get("environment").get('gmSerialize')

    @classmethod
    def _load_config(cls):
        if cls._cfg is None:
            cls._cfg = JsonUtil.readCfg()
        return cls._cfg

    def executeServer(self):
        logger = G.getG('LogMgr').getLogger(self._uniqueKey)
        try:
            # 构建可执行文件的完整路径
            command = str(Path(self.workPath) / 'fancy-server.exe')

            # 使用命令列表
            cmd_args = [command]

            logger.info("运行命令: %s", command)

            # 调用 run_command，并指定工作目录
            output, error = TerminalUtil.run_command(cmd_args, cwd=self.workPath)
            if error:
                logger.error("命令执行失败: %s", error)
            else:
                logger.info("命令执行成功")
            return output, error
        except Exception as e:
            error_msg = f"执行命令时发生异常: {e}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            return None, error_msg

    def processAllFiles(self):
        out, err = self.executeServer()
        if out:
            G.getG('LogMgr').getLogger(self._uniqueKey).info("Output: %s", out)
        if err:
            G.getG('LogMgr').getLogger(self._uniqueKey).error("Error: %s", err)

        outPath = Path(self.vo.getFuncOutPath())
        outPath.mkdir(parents=True, exist_ok=True)

        outputPath = Path(self.workPath) / "output"
        folder = Path(outputPath)
        for file in folder.glob('*.txt'):
            if file.is_file():
                target_path = Path(outPath) / file.name
                FolderUtil.move(file, target_path)

    def copySourceFiles(self, workDir):
        inputUrl = self.vo.getVal('inputUrl')
        FolderUtil.create(workDir)
        sourceItems = self.vo.getVal('sourceItems') if len(inputUrl) == 0 else {inputUrl: inputUrl}

        for _, path in sourceItems.items():
            FolderUtil.copy(path, workDir)

    def cleanDirectories(self):
        for sub_path in ["input", "output"]:
            path = Path(self.workPath) / sub_path
            if path.exists():
                for file in path.iterdir():
                    if file.is_file():
                        file.unlink()
                    elif file.is_dir():
                        FolderUtil.removeDirectory(file)
                G.getG('LogMgr').getLogger(self._uniqueKey).info(f"{sub_path} directory cleaned.")

    def main(self):
        stages = [
            {"msg": '初始化工作路径和配置', 'rate': 0.1},
            {"msg": '复制源文件到输入路径', 'rate': 0.3},
            {"msg": '执行服务器任务并处理文件', 'rate': 0.4},
            {"msg": '转移并清理资源文件', 'rate': 0.15},
            {"msg": '任务完成', 'rate': 0}
        ]

        self.cleanDirectories()

        self.kbMgr.registerProgress(self._uniqueKey, stages)
        self.kbMgr.onProgressUpdated(self._uniqueKey, 0)

        inPath = Path(self.workPath) / "input"
        self.copySourceFiles(inPath)
        self.kbMgr.onProgressUpdated(self._uniqueKey, 1)

        self.processAllFiles()
        self.kbMgr.onProgressUpdated(self._uniqueKey, 2)

        self.kbMgr.onProgressUpdated(self._uniqueKey, 3)

        if self.errors:
            G.getG('LogMgr').getLogger(self._uniqueKey).error("Errors found: %s", self.errors)
        else:
            G.getG('LogMgr').getLogger(self._uniqueKey).info("所有文件处理成功")

        self.kbMgr.onProgressUpdated(self._uniqueKey, 4)

        return self.errors
