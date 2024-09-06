import sample.src_references.common.utils.TerminalUtil as TerminalUtil

def runSvnCommand(args):
    """通用 SVN 命令执行函数"""
    try:
        result = TerminalUtil.run(args)
        return result
    except Exception as e:
        print(f"执行 SVN 命令时出错: {e}")
        return None

def getSvnInfo(item, repositoryUrl):
    """获取 SVN 信息"""
    args = ["svn", "info", "--show-item", item, repositoryUrl]
    result = runSvnCommand(args)
    if result:
        return result[0]
    return None

def updateSvn(repoPath):
    """更新 SVN 仓库"""
    args = ["svn", "update", repoPath]
    result = runSvnCommand(args)
    if result:
        return result  # 返回更新后的输出
    return None

def commitSvn(repoPath, message):
    """提交文件到 SVN 仓库
    :param repoPath: 提交的文件或目录路径
    :param message: 提交时的日志信息
    """
    args = ["svn", "commit", repoPath, "-m", message]
    result = runSvnCommand(args)
    if result:
        return result  # 返回提交结果
    return None
