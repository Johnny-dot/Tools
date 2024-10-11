import logging
import subprocess
from pathlib import Path
import pyperclip
import sys
import os

def Popen(cmd, arg, callback=None):
    print("run %s with %s" %(cmd,arg))

    with subprocess.Popen(cmd + ' ' + arg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
        try:
            while p.poll() is None:
                line = p.stdout.readline().strip()
                print(line)

            print('Execution Finished')
            if callback:callback()
        except OSError as e:  # Including KeyboardInterrupt, wait handled that.
            print("Execution Failed:", e, file=sys.stderr)


def runSvnCommand(args, logger=None, expected_errors=None):
    """通用 SVN 命令执行函数，允许预期的错误"""
    try:
        # 将命令和参数记录到日志中
        command_str = ' '.join(args)

        # if logger:
        #     logger.debug(f"执行 SVN 命令: {command_str}")

        result = subprocess.run(args, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            error_msg = result.stderr.strip()

            # 检查错误信息是否属于预期的错误
            if expected_errors and any(err in error_msg for err in expected_errors):
                # if logger:
                #     logger.info(f"预期的 SVN 错误: {error_msg}，命令: {command_str}")
                return None  # 预期错误时返回 None，但不记录为失败

            # 未预期的错误，记录为 CRITICAL
            if logger:
                logger.critical(f"SVN 命令执行失败: {error_msg}，命令: {command_str}")
            return None

        return result.stdout.splitlines()  # 返回命令输出
    except Exception as e:
        if logger:
            logger.error(f"执行 SVN 命令时发生异常: {e}，命令: {command_str}")
        return None


def run(cmd, arg, callback=None):
    print(f"run {cmd} with {arg}")
    with subprocess.Popen(cmd + ' ' + arg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
        try:
            while p.poll() is None:
                line = p.stdout.readline().strip()
                print(line.decode('utf-8') if isinstance(line, bytes) else line)

            print('Execution Finished')
            if callback:
                callback()
        except OSError as e:  # Including KeyboardInterrupt, wait handled that.
            print("Execution Failed:", e, file=sys.stderr)


def call(bat_path):
    print(f"run {bat_path} with")
    subprocess.call(bat_path, shell=True)


def ClipboardCopy(str):
    pyperclip.copy(str)


def ClipboardPaste():
    return pyperclip.paste()


def check_lua_syntax(file_path):
    try:
        # 使用as_posix()确保路径为POSIX风格（即使在Windows上也使用/分隔符）
        file_path = Path(file_path).as_posix()
        result = subprocess.run(['luac', '-p', file_path], capture_output=True, text=True)
        if result.returncode != 0:
            return False, result.stderr
        return True, ""
    except Exception as e:
        return False, str(e)


def check_code_syntax(code_path):
    non_compliant_files = []
    code_path = Path(code_path)  # 使用Path处理
    for root, dirs, files in os.walk(code_path):
        for file in files:
            if file.endswith('.lua'):
                # 使用Path来处理路径，并转换为POSIX风格
                file_path = Path(root) / file
                file_path = file_path.resolve().as_posix()  # 转换为绝对路径并使用POSIX分隔符

                is_valid, error_message = check_lua_syntax(file_path)
                if not is_valid:
                    non_compliant_files.append((file_path, error_message))

    if non_compliant_files:
        return False, non_compliant_files
    return True, []


def openInExplorer(file_path):
    """
    使用 Windows 资源管理器打开并选中指定的文件。
    """
    # 需要将路径中的特殊字符进行转义，以确保路径正确
    file_path = os.path.abspath(file_path).replace('/', '\\')
    try:
        # 使用 explorer 命令打开文件资源管理器并选中指定文件
        subprocess.Popen(f'explorer /select,"{file_path}"', shell=True)
    except Exception as e:
        return False, f"无法打开文件资源管理器: {str(e)}"
