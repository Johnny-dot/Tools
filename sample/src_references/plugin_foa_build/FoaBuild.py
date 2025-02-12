import os
import time
from pathlib import Path


import sample.src_references.Main as ToolsMain
import sample.src_references.common.vos.FoaBuildVO as KB_VO
import sample.src_references.common.utils.JsonUtil as JsonUtil
import sample.src_references.common.utils.FolderUtil as FolderUtil
import sample.src_references.common.utils.FileUtil as FileUtil
import sample.src_references.common.utils.SvnUtil as SvnUtil
import sample.src_references.common.utils.Md5Util as Md5Util
from sample.src_references.common.manager.LogMgr import LogMgr
from sample.src_references.common.utils import TerminalUtil
from sample.src_references.common.manager.KBMgr import KBMgr

ALL_BRANCHES_REPO = KB_VO.ALL_BRANCHES_REPO


class FoaBuild:
    def __init__(self, kb_vo) -> None:
        self.vo = kb_vo
        self._uniqueKey = self.vo.getUniqueKey()
        self.logger = LogMgr.getLogger(self._uniqueKey)
        self.logger.info(self._uniqueKey)

    # 1.将所选分支res与快照配置比对出差异文件
    # 2.转差异资源并更新至分支里target_res
    # 3.更新快照文件
    def autoConvertRes(self):
        def diffResMove(path):
            filePath = FolderUtil.getUrlInfo(path)[4]
            resBaseUrl = filePath.split('res', 1)
            outPath = self.vo.getFuncOutPath() + 'res' + resBaseUrl[1]
            if not FolderUtil.exists(outPath):
                FolderUtil.create(outPath)
            FolderUtil.copy(path, outPath)

        def getConvertResVo(inUrl, outUrl1, outUrl2):
            buildDict = {}
            buildDict['inputUrl'] = inUrl
            buildDict['outputUrl'] = outUrl1
            buildDict['outputUrlExtra'] = outUrl2
            buildDict['opt'] = 'RES_CONVERT'
            buildDict['platform'] = self.vo.getVal("platform")
            vo = ToolsMain.inputByDict(buildDict)
            vo.setFuncOutPath(self.vo.getFuncOutPath())
            vo.setUniqueKey(self._uniqueKey)
            return vo

        snapshotPath = self.vo.getVal('snapshotPath')
        if FolderUtil.exists(snapshotPath):
            self.logger.info('已勾选自动转资源,开始自动流程')
            self.logger.info('快照文件有效,正在对比差异文件')

            # 1.与快照配置比对出差异文件
            comparedDict = JsonUtil.readDict(snapshotPath)
            targetResPath = self.XAUrl + '/res'
            targetDict = Md5Util.fileTreeSnapshot(FolderUtil.getFilesInfo(targetResPath))

            # 是否对比出差异文件
            ifDiff = False
            for key, val in targetDict.items():
                md5 = val.get('md5')
                path = val.get('path')
                data = comparedDict.get(key)
                oMd5 = data.get('md5') if data else None
                if not oMd5:
                    # 新增
                    ifDiff = True
                    diffResMove(path)
                    self.logger.info('新增内容:%s' % path)
                elif md5 != oMd5:
                    ifDiff = True
                    # 差异
                    diffResMove(path)
                    self.logger.info('差异内容:%s' % path)
                else:
                    # 相同
                    pass

            if not ifDiff:
                self.logger.info('资源文件未对比出差异,即将跳过转资源')
                return

            # 2.转差异资源
            inUrl = self.vo.getFuncOutPath() + '/res'
            if self.vo.getVal_Lua("platform") == "android":
                outUrl1 = self.XAUrl + '/' + "res_etc"
                outUrl2 = self.XAUrl + '/' + "res_etc" + '_bf'
            else:
                outUrl1 = self.XAUrl + '/' + "res_pvr"
                outUrl2 = self.XAUrl + '/' + "res_pvr" + '_bf'

            self.logger.info('已对比出差异文件,准备进行转换并自动更正至对应分支资源')
            resVo = getConvertResVo(inUrl, outUrl1, outUrl2)
            ToolsMain.main(resVo)

            # 3.更新快照文件
            self.logger.info('更新资源同步完成,准备更新文件快照')
            snapshotBinding = JsonUtil.readInCfg('snapshot_binding') or {}
            branches = self.vo.getVal("branches")
            bindingInfo = snapshotBinding.get(branches)
            if bindingInfo:
                targetResPath = self.XAUrl + '/res'
                filesDict = FolderUtil.getFilesInfo(targetResPath)
                fileMd5Map = Md5Util.fileTreeSnapshot(filesDict)
                snapshot_environment = JsonUtil.readInCfg('environment').get('snapshot')
                branch_platform = f'{branches}_{self.platform}'
                snapshot_cfg_path = FolderUtil.join(snapshot_environment, branch_platform)
                newSnapshotCfgPath = f"{snapshot_cfg_path}/snapshot_{time.strftime('%Y%m%d%H%M%S')}.json"

                JsonUtil.writeDict(fileMd5Map, newSnapshotCfgPath)
                bindingInfo['snapshot_%s' % self.platform] = newSnapshotCfgPath
                snapshotBinding[branches] = bindingInfo
                JsonUtil.saveInCfg('snapshot_binding', snapshotBinding)
                self.logger.info(f'文件快照更新完成,新快照文件为:{newSnapshotCfgPath}')

    def initWorkEnv(self):
        # 获取工作环境
        cfg = JsonUtil.readCfg()
        if self.vo.getVal_Lua("tag") == 'mclient':
            self.workPath = cfg.get("environment").get('mclient')
        elif str(self.vo.getVal_Lua("is64")) == "false":
            self.workPath = cfg.get("environment").get('Android32')
        elif str(self.vo.getVal_Lua("is64")) == "true":
            self.workPath = cfg.get("environment").get('Android64')
        else:
            self.workPath = cfg.get("environment").get('build')

        # 确定分支
        branches = self.vo.getVal_Lua("branches")
        self.XAUrl = KBMgr.getBranchUrl(branches)
        result = SvnUtil.updateSvn(self.XAUrl)
        self.logger.info(f"更新分支 {branches} 结果: {result}")

        # 分支最新版本
        repoUrl = ALL_BRANCHES_REPO.get(branches)
        self.svnNumber = SvnUtil.getSvnInfo("revision", repoUrl)

        # 出包平台
        self.platform = self.vo.getVal_Lua("platform")
        self.platformRes = self.XAUrl + '/' + self.vo.getVal_Lua("res_target")

        # foa tag
        self.tag = self.vo.getVal_Lua("tag")

        # 将所选分支的 code/pack_simulate/nodod.lua 和 pack2.lua 复制到工作目录
        code_path = os.path.join(self.XAUrl, 'code')
        target_files = ['nodod.lua', 'pack2.lua']

        for file_name in target_files:
            source_file = os.path.join(code_path, 'pack_simulate', file_name)
            destination_file = os.path.join(self.workPath, file_name)

            if FolderUtil.exists(source_file):
                # 如果目标文件已经存在，检测差异
                if FolderUtil.exists(destination_file):
                    diff, error = FileUtil.compare_file_contents(destination_file, source_file)
                    if diff:
                        print(f"当前文件名: {file_name}")  # 调试代码，检查 file_name 的值
                        if file_name == 'nodod.lua':
                            self.logger.info("检测到首包变更，此次变更的内容为：")
                        elif file_name == 'pack2.lua':
                            self.logger.info("检测到二包变更，此次变更的内容为：")

                        for line in diff:
                            self.logger.info(line.strip())
                    else:
                        self.logger.info("首包和二包的配置文件无变更")

                # 复制文件
                FolderUtil.copy(source_file, destination_file)
                self.logger.info(f"复制文件 {file_name} 到工作目录 {self.workPath}")
            else:
                self.logger.warning(f"文件 {file_name} 不存在于路径 {source_file}")

    def checkCode(self):
        code_path = os.path.join(self.XAUrl, 'code')
        res_path = os.path.join(self.XAUrl, 'res')

        # 检查Lua代码的语法
        is_syntax_correct, syntax_errors = TerminalUtil.check_code_syntax(code_path)
        if not is_syntax_correct:
            self.logger.warning("Lua syntax errors found in the following files:")
            for file_path, error_message in syntax_errors:
                self.logger.warning(f"File: {file_path}, Error: {error_message}")
            return syntax_errors, False

        # 检查code文件夹中的文件名是否小写
        is_correct_code, incorrect_files_code = FileUtil.check_lowercase_filenames(code_path)
        if not is_correct_code:
            self.logger.warning("Filename check failed in code folder. The following files are not lowercase:")
            for file_path in incorrect_files_code:
                self.logger.warning(f"File: {file_path}")

        # # 检查res文件夹中的文件名是否小写
        # is_correct_res, incorrect_files_res = FileUtil.check_lowercase_filenames(res_path, ignore_extensions=['.mp3', '.ogg'])
        # if not is_correct_res:
        #     self.logger.warning("Filename check failed in res folder. The following files are not lowercase:")
        #     for file_path in incorrect_files_res:
        #         self.logger.warning(f"File: {file_path}")

        # 如果任一检查不通过，则返回False
        if not is_correct_code:
            self.logger.warning("Filename check did not pass. Please review the errors above.")
            return incorrect_files_code, False

        self.logger.info("Code check passed.")

        return [], True

    def getBat(self, php):
        if self.vo.getVal_Lua("tag") == 'mclient':
            version_code = (
                f"php package.php bigversion={self.vo.getVal_Lua('bigversion')} "
                f"platform={self.vo.getVal_Lua('platform')} tag={self.vo.getVal_Lua('tag')} "
                f"use_localserverlist={self.vo.getVal_Lua('use_localserverlist')} "
                f"path={self.XAUrl} sysversion={self.vo.getVal_Lua('sysversion')} toapple=false "
                f"svnnumber={self.svnNumber} nowtime={self._uniqueKey.split('-')[1]} "
            )
            return version_code
        elif str(self.vo.getVal_Lua("is64")) in ['false', 'true']:
            version_code = (
                f"php {php} toapple={self.vo.getVal_Lua('isAppleStoreReview')} istoiran={self.vo.getVal_Lua('istoiran')} "
                f"platform={self.vo.getVal_Lua('platform')} bigversion={self.vo.getVal_Lua('bigversion')} sandbox={self.vo.getVal_Lua('sandbox')} "
                f"isdebug={self.vo.getVal_Lua('isdebug')} tag={self.vo.getVal_Lua('tag')} testapp={self.vo.getVal_Lua('istestapp')} "
                f"use_sdk={self.vo.getVal_Lua('use_sdk')} use_localserverlist={self.vo.getVal_Lua('use_localserverlist')} "
                f"lang={self.vo.getVal_Lua('lang')} path={self.XAUrl} sysversion={self.vo.getVal_Lua('sysversion')} "
                f"is64={self.vo.getVal_Lua('is64')} svnnumber={self.svnNumber} nowtime={self._uniqueKey.split('-')[1]} "
            )
            return version_code
        else:
            pathfc = 'fancy-dev.cfg'
            version_code = (
                f"del %cd%\\{pathfc}\necho build.lua -d>%cd%\\{pathfc}\nphp {php} "
                f"platform={self.vo.getVal_Lua('platform')} isdebug={self.vo.getVal_Lua('isdebug')} "
                f"bigversion={self.vo.getVal_Lua('bigversion')} tag={self.vo.getVal_Lua('tag')} "
                f"lang=zh use_sdk={self.vo.getVal_Lua('use_sdk')} "
                f"use_localserverlist={self.vo.getVal_Lua('use_localserverlist')} toapple=false "
                f"path={self.XAUrl} flag=old svnnumber={self.svnNumber} nowtime={self._uniqueKey.split('-')[1]} "
            )
            return version_code

    # 处理两份version
    def generateBuildConfig(self):
        # if self.vo.getVal_Lua("tag") == 'zs':
        #     php = 'build_foa_20151013.php'
        # elif self.vo.getVal_Lua("tag") == 'zsys' or self.vo.getVal_Lua("tag") == 'ajmzs':
        #     php = 'build_foa_20151013yasuo.php'
        # elif self.vo.getVal_Lua("tag") == 'zsbx':
        #     php = 'build_foa_20151013包小.php'
        # elif self.vo.getVal_Lua("tag") == 'zsfb':
        #     php = 'build_foa_20170808分包.php'
        # else:
        php = 'build_foa_20151013.php'

        batContent = self.getBat(php)
        batOutPath = os.path.join(self.workPath, "temp.bat")
        FileUtil.writeStr(batContent, batOutPath)

    # 执行打包指令
    def build(self):
        inPath = os.path.abspath(self.workPath)
        bat_out_path = os.path.join(inPath, "temp.bat")
        cwd = self.workPath
        # 使用 run_command 来执行打包命令，并传递工作目录 cwd
        output, error = TerminalUtil.run_command(bat_out_path, cwd=cwd)
        if error:
            self.logger.error(f"Error during build: {error}")
        else:
            self.logger.info(f"Build output: {output}")

    def getFoaDetectVO(self):
        sourceItems = {}
        outDir = os.path.join(self.workPath, "output", f"{self.platform}_{self.tag}_{self.svnNumber}")
        folder = Path(outDir)
        for file in folder.rglob('*'):
            if file.is_file():
                if file.suffix in {'.txt'}:
                    sourceItems[file.name] = str(file)

        buildDict = {}
        buildDict['opt'] = 'FOA_DETECT'
        buildDict['sourceItems'] = sourceItems
        vo = ToolsMain.inputByDict(buildDict)
        vo.setFuncOutPath(self.vo.getFuncOutPath())
        vo.setUniqueKey(self._uniqueKey)
        return vo

    def checkFoa(self):
        foaDetectVo = self.getFoaDetectVO()
        return ToolsMain.main(foaDetectVo)

    def dealOutPut(self):
        nowdate = self._uniqueKey.split('-')[1]
        inPath = os.path.abspath(os.path.join(self.workPath, f"output/{self.platform}_{self.tag}_{self.svnNumber}_{nowdate}"))
        finalOutPath = os.path.join(self.vo.getFuncOutPath(), f"{self.platform}_{self.tag}_{self.svnNumber}_{nowdate}")
        FolderUtil.copy(inPath, finalOutPath)
        FolderUtil.delete(inPath)

    def dealExtraOutPut(self):
        outPath1 = self.vo.getVal("outPath1")
        outPath2 = self.vo.getVal("outPath2")
        sourcePath = Path(self.vo.getFuncOutPath()) / f"{self.platform}_{self.tag}_{self.svnNumber}_{self._uniqueKey.split('-')[1]}"
        def copy_foa_files(source, destination):
            if not destination.exists():
                destination.mkdir(parents=True, exist_ok=True)

            for foa_file in source.rglob("*"):
                if foa_file.suffix in [".foa", ".text"]:
                    dest_file = destination / foa_file.relative_to(source)
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    FolderUtil.copy(foa_file, dest_file)

        if FolderUtil.exists(outPath1):
            outPath1 = Path(self.vo.getVal("outPath1"))  # 转换为 Path 对象
            copy_foa_files(sourcePath, outPath1)

        if FolderUtil.exists(outPath2):
            outPath2 = Path(self.vo.getVal("outPath2"))
            copy_foa_files(sourcePath, outPath2)

    def cleanTemp(self):
        inPath = os.path.abspath(self.workPath)
        tempPath = os.path.join(inPath, "temp")
        FolderUtil.delete(tempPath)

    def main(self):
        stages = [
            {"msg": '初始化工作环境', 'rate': 0.1},
            {"msg": '检测代码是否合规', 'rate': 0.1},
            {"msg": '自动转换资源', 'rate': 0.2},
            {"msg": '生成打包配置', 'rate': 0.1},
            {"msg": '执行打包命令', 'rate': 0.3},
            {"msg": '校验FOA是否合规', 'rate': 0.1},
            {"msg": '转移FOA至outpath', 'rate': 0.1},
            # {"msg": '清理临时文件', 'rate': 0.1}
        ]

        # 注册进度条
        KBMgr.registerProgress(self.vo.getUniqueKey(), stages)

        # 初始化工作环境
        self.initWorkEnv()
        KBMgr.onProgressUpdated(self._uniqueKey, 0)
        self.logger.info("初始化工作环境")

        # 检测代码是否合规
        syntax_errors, isCorrect = self.checkCode()
        if not isCorrect: return syntax_errors, False
        KBMgr.onProgressUpdated(self._uniqueKey, 1)
        self.logger.info("检测代码是否合规完成")

        # 自动转换资源
        self.autoConvertRes()
        KBMgr.onProgressUpdated(self._uniqueKey, 2)
        self.logger.info("自动转换资源完成")

        # 生成打包配置
        self.generateBuildConfig()
        KBMgr.onProgressUpdated(self._uniqueKey, 3)
        self.logger.info("生成打包配置完成")

        # 执行打包命令
        self.build()
        KBMgr.onProgressUpdated(self._uniqueKey, 4)
        self.logger.info("执行打包命令完成")

        foaErrors = self.checkFoa()
        KBMgr.onProgressUpdated(self._uniqueKey, 5)
        self.logger.info("校验FOA是否合规完成")
        if foaErrors:
            return foaErrors, False

        # 转移FOA至outpath
        self.dealOutPut()
        self.dealExtraOutPut()
        KBMgr.onProgressUpdated(self._uniqueKey, 6)
        self.logger.info("转移FOA至outpath完成")

        # 构建完成
        # self.cleanTemp()
        # KBMgr.onProgressUpdated(self._uniqueKey, 7)
        # self.logger.info("清理临时文件完成")

        return foaErrors, True
