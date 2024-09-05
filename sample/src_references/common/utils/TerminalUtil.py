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


def run(args, callback=None):
    result = subprocess.run(args, shell=True, capture_output=True, text=True)
    if callback:
        callback(result)
    out,err = result.stdout.strip(),result.stderr.strip()
    return out, err

def call(bat_path):
    print("run %s with" %(bat_path))
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


