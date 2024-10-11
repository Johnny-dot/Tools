import os
import sample.src_references.common.utils.TerminalUtil as TerminalUtil


def check_connection(repository_url, logger=None):
    """检查 SVN 仓库连接是否可用"""
    args = ["svn", "info", repository_url]
    result = TerminalUtil.runSvnCommand(args, logger)
    if result:
        logger.info(f"连接到 {repository_url} 成功。") if logger else print(f"连接到 {repository_url} 成功。")
        return True
    else:
        logger.error(f"无法连接到 {repository_url}") if logger else print(f"无法连接到 {repository_url}")
        return False


def getSvnInfo(item, repositoryUrl, logger=None):
    """获取 SVN 信息"""
    args = ["svn", "info", "--show-item", item, repositoryUrl]
    result = TerminalUtil.runSvnCommand(args, logger)
    if result:
        return result[0]
    return None


def updateSvn(repoPath, logger=None):
    """更新 SVN 仓库"""
    args = ["svn", "update", repoPath]
    result = TerminalUtil.runSvnCommand(args, logger)
    if result:
        return True
    return False


def commitSvn(repoPath, message, logger=None):
    """提交文件到 SVN 仓库"""
    args = ["svn", "commit", repoPath, "-m", message]
    result = TerminalUtil.runSvnCommand(args, logger)
    if result:
        logger.info(f"成功提交: {message}") if logger else print(f"成功提交: {message}")
        return True
    return False


def checkoutOrUpdate(repository_url, checkout_directory, logger=None):
    """检出或更新 SVN 仓库"""
    if os.path.exists(checkout_directory) and os.path.isdir(checkout_directory):
        logger.info(f"更新 {checkout_directory} 来自 {repository_url}") if logger else print(f"更新 {checkout_directory} 来自 {repository_url}")
        args = ["svn", "update", checkout_directory]
        return TerminalUtil.runSvnCommand(args, logger) is not None
    else:
        logger.info(f"检出 {repository_url} 到 {checkout_directory}") if logger else print(f"检出 {repository_url} 到 {checkout_directory}")
        args = ["svn", "checkout", repository_url, checkout_directory]
        return TerminalUtil.runSvnCommand(args, logger) is not None


def isUnderVersionControl(path, logger=None):
    """检查文件或目录是否在版本控制之下"""
    # 如果文件不存在，直接返回 False
    if not os.path.exists(path):
        if logger:
            logger.warning(f"文件或目录 {path} 不存在，无法检测是否在版本控制中。")
        return False

    # 预期的错误是文件未被版本控制
    expected_errors = ["W155010", "The node was not found"]
    args = ["svn", "info", path]
    result = TerminalUtil.runSvnCommand(args, logger, expected_errors=expected_errors)

    if result is None:
        # 文件未被版本控制，返回 False
        # if logger:
        #     logger.info(f"文件或目录 {path} 未被版本控制。")
        return False

    return True


def addToSvn(path, logger=None):
    """添加文件或目录到 SVN"""
    if os.path.isfile(path) or os.path.isdir(path):
        if not isUnderVersionControl(path, logger):
            args = ["svn", "add", path, "--force"]
            result = TerminalUtil.runSvnCommand(args, logger)
            if result:
                logger.info(f"添加 {path} 到 SVN 成功。")
            else:
                logger.critical(f"添加 {path} 到 SVN 失败。")
        else:
            pass
            # logger.info(f"{path} 已经在版本控制之下。")
    else:
        logger.warning(f"{path} 不是有效的文件或目录。")


def resolveConflicts(path, logger=None):
    """解决 SVN 冲突"""
    # 检查是否是有效的 SVN 工作目录
    args_info = ["svn", "info", path]
    info_result = TerminalUtil.runSvnCommand(args_info, logger)
    if not info_result:
        logger.warning(f"路径 {path} 不是有效的 SVN 工作目录，或者 SVN 仓库连接有问题。")
        return

    # 获取冲突的文件列表
    args = ["svn", "status", path]
    result = TerminalUtil.runSvnCommand(args, logger)

    if result is None:
        logger.info("SVN 状态为空，表示没有冲突或未提交的改动。")
        return
    else:
        logger.info(f"获取到的 SVN 状态结果: {result}")

    conflicts_found = False
    for line in result:
        if line.startswith('C'):  # 'C' 表示冲突
            conflicts_found = True
            conflict_path = line[8:].strip()
            # 解决冲突，使用 'theirs-full' 策略
            args_resolve = ["svn", "resolve", "--accept", "theirs-full", conflict_path]
            resolve_result = TerminalUtil.runSvnCommand(args_resolve, logger)
            if resolve_result:
                logger.info(f"使用 'theirs-full' 解决了 {conflict_path} 的冲突。")
            else:
                logger.critical(f"解决 {conflict_path} 的冲突失败。")

    if conflicts_found:
        logger.info("所有检测到的冲突已被解决。")
    else:
        logger.info("没有检测到需要解决的冲突。")



def hasChangesToCommit(path, logger=None):
    """检查是否有改动需要提交"""
    args = ["svn", "status", path]
    result = TerminalUtil.runSvnCommand(args, logger)
    if result:
        for line in result:
            if line and line[0] in ['A', 'M', 'D', '?']:
                return True
    return False


def getSvnLog(repository_url, num, logger=None):
    """获取 SVN 日志"""
    args = ["svn", "log", repository_url, "-l", str(num)]
    result = TerminalUtil.runSvnCommand(args, logger)

    if result:
        logs = []
        current_log = {}
        message_lines = []
        for line in result:
            line = line.strip()

            # 跳过空行和分隔符
            if not line or line.startswith('-----'):
                continue

            # 检查是否是新日志的起始行
            if line.startswith('r') and '|' in line:
                # 如果已经有未处理的日志，先保存
                if current_log and message_lines:
                    current_log['message'] = '\n'.join(message_lines).strip()
                    logs.append(current_log)
                    message_lines = []

                # 处理新的日志条目
                parts = line.split('|')
                if len(parts) >= 4:
                    date_str = parts[2].strip()

                    # 提取日期和时间部分，去掉时区和星期信息
                    date_time = ' '.join(date_str.split(' ')[:2])  # 保留日期和时间部分

                    current_log = {
                        'revision': parts[0].strip().lstrip('r'),  # 去掉'r'字符
                        'author': parts[1].strip(),
                        'date': date_time,  # 使用简化后的日期和时间
                    }
                else:
                    logger.warning(f"日志行格式不符合预期: {line}") if logger else print(
                        f"日志行格式不符合预期: {line}")
            else:
                # 将其视为当前日志的提交信息，过滤掉无用行
                if not line.startswith('-----'):
                    message_lines.append(line)

        # 处理最后一个日志条目
        if current_log and message_lines:
            current_log['message'] = '\n'.join(message_lines).strip()
            logs.append(current_log)

        return logs
    return None
