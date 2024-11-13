import subprocess
from pathlib import Path
import os
import pyperclip

def run_command(cmd_args, callback=None, cwd=None):
    """
    运行命令并实时打印输出。
    cmd_args 可以是字符串（命令）或列表（命令及参数）。
    返回 (output, error)，其中 output 是命令输出，error 是错误信息。
    """
    try:
        if isinstance(cmd_args, list):
            process = subprocess.Popen(
                cmd_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=cwd  # 指定工作目录
            )
        else:
            process = subprocess.Popen(
                cmd_args,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=cwd  # 指定工作目录
            )

        output_lines = []

        # 实时读取输出
        for line in process.stdout:
            line = line.strip()
            print(line)
            output_lines.append(line)

        # 等待进程结束
        process.wait()

        # 触发回调函数（如果有）
        if callback:
            callback()

        # 检查返回码
        if process.returncode != 0:
            return None, '\n'.join(output_lines)
        else:
            return '\n'.join(output_lines), None

    except Exception as e:
        return None, f"执行失败: {e}"

def run_svn_command(args, logger=None, expected_errors=None):
    """
    通用 SVN 命令执行函数，允许预期的错误。
    """
    try:
        command_str = ' '.join(args)

        # 运行 SVN 命令
        result = subprocess.run(args, capture_output=True, text=True)

        if result.returncode != 0:
            error_msg = result.stderr.strip()

            # 检查是否为预期的错误
            if expected_errors and any(err in error_msg for err in expected_errors):
                if logger:
                    logger.info(f"预期的 SVN 错误: {error_msg}，命令: {command_str}")
                return None  # 预期错误不视为失败

            # 未预期的错误
            if logger:
                logger.critical(f"SVN 命令执行失败: {error_msg}，命令: {command_str}")
            return None

        return result.stdout.splitlines()  # 返回命令输出

    except Exception as e:
        if logger:
            logger.error(f"执行 SVN 命令时发生异常: {e}，命令: {command_str}")
        return None


def call_script(bat_path):
    """
    运行指定的批处理脚本。
    """
    print(f"运行脚本: {bat_path}")
    subprocess.run(bat_path, shell=True)


def clipboard_copy(text):
    """
    将文本复制到剪贴板。
    """
    pyperclip.copy(text)


def clipboard_paste():
    """
    从剪贴板粘贴文本。
    """
    return pyperclip.paste()


def check_lua_syntax(file_path):
    """
    检查单个 Lua 文件的语法。
    """
    try:
        result = subprocess.run(['luac', '-p', file_path], capture_output=True, text=True)
        if result.returncode != 0:
            return False, result.stderr.strip()
        return True, ""
    except Exception as e:
        return False, str(e)


def check_code_syntax(code_path):
    """
    检查指定路径下所有 Lua 文件的语法。
    """
    code_path = Path(code_path)
    non_compliant_files = []

    for file_path in code_path.rglob('*.lua'):
        is_valid, error_message = check_lua_syntax(str(file_path))
        if not is_valid:
            non_compliant_files.append((str(file_path), error_message))

    if non_compliant_files:
        return False, non_compliant_files
    return True, []


def open_in_explorer(file_path):
    """
    使用 Windows 资源管理器打开并选中指定的文件。
    """
    file_path = os.path.abspath(file_path)
    try:
        subprocess.run(f'explorer /select,"{file_path}"', shell=True)
    except Exception as e:
        return False, f"无法打开文件资源管理器: {str(e)}"
