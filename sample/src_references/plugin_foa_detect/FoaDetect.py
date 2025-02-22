import sample.src_references.common.utils.JsonUtil as JsonUtil
import sample.src_references.common.utils.FolderUtil as FolderUtil
import sample.src_references.common.utils.TerminalUtil as TerminalUtil
from sample.src_references.common.manager.KBMgr import KBMgr
from sample.src_references.common.manager.LogMgr import LogMgr

from pathlib import Path

class FoaDetect:
    def __init__(self, kb_vo) -> None:
        self.vo = kb_vo
        self.errors = []
        self._uniqueKey = self.vo.getUniqueKey()
        # 获取工作环境
        cfg = JsonUtil.readCfg()
        self.workPath = cfg.get("environment").get('foaDetect')

    def foa2Fod(self, name, callback=None):
        try:
            command = [
                str(Path(self.workPath) / 'fancy3d-foa-tool.exe'),
                f"foa/{name}",
                "grouplist.txt"
            ]
            logger = LogMgr.getLogger(self._uniqueKey)
            logger.info("运行命令: %s", ' '.join(command))

            output, error = TerminalUtil.run_command(command, callback)
            if error:
                logger.error("命令执行失败: %s", error)
            else:
                logger.info("命令执行成功")
            return output, error
        except Exception as e:
            logger = LogMgr.getLogger(self._uniqueKey)
            logger.error("执行命令时发生异常: %s", e)
            return None, str(e)

    def dealAllFoas(self, inPath, outPath):
        folder = Path(inPath)
        for file_path in folder.rglob('*.foa'):
            if file_path.is_file():
                LogMgr.getLogger(self._uniqueKey).info(f"Found file: {file_path}")
                out, err = self.foa2Fod(file_path.name)
                if out:
                    LogMgr.getLogger(self._uniqueKey).info("Output: %s", out)
                if err:
                    LogMgr.getLogger(self._uniqueKey).error("Error: %s", err)
        for file in folder.rglob('*'):
            if file.is_file():
                if file.suffix in {'.txt'}:
                    target_path = Path(outPath) / file.name
                    FolderUtil.move(file, target_path)
                elif file.suffix in {'.foc', '.fod'}:
                    LogMgr.getLogger(self._uniqueKey).info(f"Deleting {file}")
                    file.unlink()  # 删除文件

    def checkAllTxt(self, path):
        folder = Path(path)
        for file in folder.rglob('*.txt'):
            if file.is_file():
                LogMgr.getLogger(self._uniqueKey).info("Checking file: %s", file)
                with file.open('r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        if i >= 4:  # 跳过前4行
                            splitArray = line.split('|')
                            file_path = splitArray[0].strip()
                            md5 = splitArray[1].strip()
                            start_offset = int(splitArray[2].strip()[1:])  # 去掉'#'并转换为整数
                            end_offset = int(splitArray[3].strip())
                            status = splitArray[4].strip()

                            if start_offset < 0 or end_offset < 0:
                                # LogMgr.getLogger(self._uniqueKey).error("Error found in %s: %s", file, line.strip())
                                self.errors.append(f"{file.name}: {line.strip()}")
                                break

    def dealSourceFiles(self, workDir):
        inputUrl = self.vo.getVal('inputUrl')
        FolderUtil.create(workDir)

        # 将源文件拷贝到目标路径
        if len(inputUrl) <= 0:
            sourceItems = self.vo.getVal('sourceItems')
            for dir, path in sourceItems.items():
                FolderUtil.copy(path, workDir)
        else:
            FolderUtil.copy(inputUrl, workDir)

    def main(self):
        stages = [
            {"msg": '初始化工作路径和配置', 'rate': 0.1},
            {"msg": '开始复制源文件到工作路径', 'rate': 0.25},
            {"msg": '扫描并处理 .foa 文件', 'rate': 0.4},
            {"msg": '转移并清理资源文件', 'rate': 0.15},
            {"msg": '检查并校验 .txt 文件', 'rate': 0.1},
            {"msg": '任务完成', 'rate': 0}
        ]

        KBMgr.registerProgress(self._uniqueKey, stages)

        # 初始化阶段
        KBMgr.onProgressUpdated(self._uniqueKey, 0)
        # 复制源文件到工作路径
        inPath = self.workPath + "/foa/"
        self.dealSourceFiles(inPath)
        KBMgr.onProgressUpdated(self._uniqueKey, 1)

        # 扫描并处理 .foa 文件
        outPath = self.vo.getFuncOutPath()
        Path(outPath).mkdir(parents=True, exist_ok=True)
        self.dealAllFoas(inPath, outPath)
        KBMgr.onProgressUpdated(self._uniqueKey, 2)

        # 转移并清理资源文件
        KBMgr.onProgressUpdated(self._uniqueKey, 3)

        # 检查并校验 .txt 文件
        self.checkAllTxt(outPath)
        KBMgr.onProgressUpdated(self._uniqueKey, 4)

        if not self.errors:
            LogMgr.getLogger(self._uniqueKey).info("检测全部合规")
        else:
            LogMgr.getLogger(self._uniqueKey).error("Errors found: %s", self.errors)
        # 停止假进度条并完成任务
        KBMgr.onProgressUpdated(self._uniqueKey, 5)

        return self.errors
