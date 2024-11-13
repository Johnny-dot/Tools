from pathlib import Path

import sample.src_references.common.g.G as G
import sample.src_references.common.utils.JsonUtil as JsonUtil
import sample.src_references.common.utils.FileUtil as FileUtil
import sample.src_references.common.utils.FolderUtil as FolderUtil
import sample.src_references.common.utils.TerminalUtil as TerminalUtil
class ResConvert:
    def __init__(self, kb_vo) -> None:
        self.vo = kb_vo
        self.kbMgr = G.getG("KBMgr")
        self._uniqueKey = self.vo.getUniqueKey()
        # 获取工作环境
        cfg = JsonUtil.readCfg()
        self.workPath = cfg.get("environment").get('resConvert')

    def convertEtc(self):
        cmd = str(Path(self.workPath) / 'fancy-dev.exe')
        args = ['-d', 'Etc.lua']  # 如果需要使用 "android_etc.lua"，请更改为 'android_etc.lua'
        command = [cmd] + args
        output, error = TerminalUtil.run_command(command)
        if error:
            print(f"执行失败: {error}")
        else:
            print("执行成功")

    def convertPvr(self):
        cmd = str(Path(self.workPath) / 'fancy-dev.exe')
        args = ['-d', 'Pvr.lua']
        command = [cmd] + args
        output, error = TerminalUtil.run_command(command)
        if error:
            print(f"执行失败: {error}")
        else:
            print("执行成功")

    def getFolderName(self):
        platform = self.vo.getVal('platform')
        folderName = 'temp'
        if platform == "android":
            folderName = 'etc'
        elif platform == "ios":
            folderName = 'pvr'
        elif platform == "mclient":
            folderName = 'mclient'
        else:
            G.getG('LogMgr').getLogger(self._uniqueKey).error('不支持的平台：%s' % platform)

        return folderName

    def dealSourceFiles(self):
        inputUrl = self.vo.getVal('inputUrl')
        folderName = self.getFolderName()
        workDir = '%s/%s'%(self.workPath, folderName)
        FolderUtil.create(workDir)
        # else
        # todo 微端
        
        # 将源文件拷贝到目标路径
        if len(inputUrl) <= 0:
            sourceItems = self.vo.getVal('sourceItems')
            for dir,path in sourceItems.items():
                FolderUtil.copy(path, workDir)
        else:
            FolderUtil.copy(inputUrl, workDir)

    def generateBuildConfig(self):
        convertconfig_url = self.workPath + "/convertconfig.lua"
        str = "_G.ConvertConfig = {\n" + "\tFolderIn = '%s/'\n"% self.getFolderName() + "\t,FolderOut = 'out_%s/'"% self.getFolderName()+ "\n}"

        FileUtil.writeStr(str, convertconfig_url)

    def dealOutPut(self):
        folderName = self.getFolderName()
        workDir = '%s/%s'%(self.workPath, folderName)

        outputUrl = self.vo.getVal('outputUrl')
        outputUrlExtra = self.vo.getVal('outputUrlExtra')
        if FolderUtil.exists(outputUrl) or FolderUtil.exists(outputUrlExtra):
            FolderUtil.copy(workDir, outputUrl)
            FolderUtil.copy(workDir, outputUrlExtra)
            G.getG('LogMgr').getLogger(self._uniqueKey).info('已将转换后的资源输出到指定路径')
        else:
            finalOutPath = self.vo.getFuncOutPath()
            FolderUtil.copy(workDir, finalOutPath)

        G.getG('LogMgr').getLogger(self._uniqueKey).info('资源转换成功')


    def convert(self):
        platform = self.vo.getVal('platform')
        G.getG('LogMgr').getLogger(self._uniqueKey).info('前置文件准备就绪,即将调起引擎转换资源,请耐心等待')
        if platform == "android":
            self.convertEtc()
        elif platform == "ios":
            self.convertPvr()
        else:
            G.getG('LogMgr').getLogger(self._uniqueKey).error('不支持的平台：%s' % platform)

    def main(self):
        stages = [
            {"msg":'开始复制源文件到工作路径', 'rate':0.3}
            ,{"msg":'开始转资源', 'rate':0.4}
            ,{"msg":'将已完成资源转移到目标路径', 'rate':0.3}
            ,{"msg":'完成'}
        ]
        self.kbMgr.registerProgress(self.vo.getUniqueKey(), stages)
        self.dealSourceFiles()
        self.generateBuildConfig()
        self.convert()
        self.dealOutPut()