import os
from sample.src_references.common.g import G
from sample.src_references.common.utils import JsonUtil, FolderUtil, SvnUtil


class BranchCover:
    def __init__(self, paraVo) -> None:
        self.paraVo = paraVo
        self._uniqueKey = paraVo.getUniqueKey()
        # 获取工作环境
        cfg = JsonUtil.readCfg()
        self.workPath = cfg.get("environment").get('branchCover')
        self.logger = G.getG('LogMgr').getLogger(self._uniqueKey)

    def cover(self):
        pass

    def main(self):
        source_repository_url = self.paraVo.getVal('source_repository_url')
        destination_repository_url = self.paraVo.getVal('destination_repository_url')
        commit_message = self.paraVo.getVal('commit_message')
        temp_directory = self.workPath

        FolderUtil.createSafely(temp_directory)
        src_checkout_dir = FolderUtil.join(temp_directory, 'src_checkout')
        dest_checkout_dir = FolderUtil.join(temp_directory, 'dest_checkout')

        self.logger.info("源仓库检出目录: %s", src_checkout_dir)
        self.logger.info("目标仓库检出目录: %s", dest_checkout_dir)

        # 检查源仓库连接
        if not SvnUtil.check_connection(source_repository_url):
            self.logger.error("源仓库连接失败。")
            return  # 终止流程

        # 检查目标仓库连接
        if not SvnUtil.check_connection(destination_repository_url):
            self.logger.error("目标仓库连接失败。")
            return  # 终止流程

        # 检出源仓库代码到临时目录
        self.logger.info("开始检出或更新源仓库")
        if not SvnUtil.checkoutOrUpdate(source_repository_url, src_checkout_dir, self.logger):
            self.logger.error("检出或更新源仓库失败。")
            return

        # 显示源仓库日志
        logs_src = SvnUtil.getSvnLog(source_repository_url, 3, self.logger)
        if logs_src:
            for log in logs_src:
                self.logger.info(
                    f'源仓库版本: {log["revision"]}, 作者: {log["author"]}, 日期: {log["date"]}, 提交信息: {log["message"]}'
                )
        else:
            self.logger.warning("未获取到源仓库日志。")

        # 检出目标仓库代码到本地目录
        self.logger.info("开始检出或更新目标仓库")
        if not SvnUtil.checkoutOrUpdate(destination_repository_url, dest_checkout_dir, self.logger):
            self.logger.error("检出或更新目标仓库失败。")
            return

        # 显示目标仓库日志
        logs_dest = SvnUtil.getSvnLog(destination_repository_url, 3, self.logger)
        if logs_dest:
            for log in logs_dest:
                self.logger.info(
                    f'目标仓库版本: {log["revision"]}, 作者: {log["author"]}, 日期: {log["date"]}, 提交信息: {log["message"]}'
                )
        else:
            self.logger.warning("未获取到目标仓库日志。")

        # 将源仓库的更改内容复制到目标仓库的检出目录
        self.logger.info("复制源仓库的更改到目标仓库目录")
        FolderUtil.copy(src_checkout_dir, dest_checkout_dir, None, ['.svn'])

        # 添加新文件到SVN
        self.logger.info("开始添加新文件到SVN")
        for root, dirs, files in os.walk(dest_checkout_dir):
            # 忽略 .svn 目录
            dirs[:] = [d for d in dirs if d != '.svn']
            for name in files:
                file_path = FolderUtil.join(root, name)
                SvnUtil.addToSvn(file_path, self.logger)
            for name in dirs:
                dir_path = FolderUtil.join(root, name)
                SvnUtil.addToSvn(dir_path, self.logger)

        # 解决更新过程中可能出现的冲突
        self.logger.info("开始解决SVN冲突")
        SvnUtil.resolveConflicts(dest_checkout_dir, self.logger)

        # 检查是否有改动需要提交
        if not SvnUtil.hasChangesToCommit(dest_checkout_dir, self.logger):
            self.logger.warning("没有需要提交的改动,合并取消。")
            return

        # 提交本地修改到目标仓库
        self.logger.info("开始提交修改到目标仓库")
        commit_result = SvnUtil.commitSvn(dest_checkout_dir, commit_message, self.logger)
        if not commit_result:
            self.logger.error("提交到目标仓库失败。")
            return

        # 更新本地工作副本到目标仓库最新版本
        self.logger.info("更新目标仓库到最新版本")
        if not SvnUtil.updateSvn(dest_checkout_dir, self.logger):
            self.logger.error("更新目标仓库失败。")
            return

        self.logger.info("提交后目标仓库最新日志:")
        # 显示目标仓库最新日志
        logs_dest_after_commit = SvnUtil.getSvnLog(destination_repository_url, 1, self.logger)
        if logs_dest_after_commit:
            for log in logs_dest_after_commit:
                self.logger.info(
                    f'目标仓库版本: {log["revision"]}, 作者: {log["author"]}, 日期: {log["date"]}, 提交信息: {log["message"]}'
                )
        else:
            self.logger.warning("未获取到提交后的目标仓库日志。")
