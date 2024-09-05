import subprocess
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
        result = subprocess.run(['luac', '-p', file_path], capture_output=True, text=True)
        if result.returncode != 0:
            return False, result.stderr
        return True, ""
    except Exception as e:
        return False, str(e)

def check_code_syntax(code_path):
    non_compliant_files = []
    for root, dirs, files in os.walk(code_path):
        for file in files:
            if file.endswith('.lua'):
                file_path = os.path.normpath(os.path.join(root, file))
                is_valid, error_message = check_lua_syntax(file_path)
                if not is_valid:
                    non_compliant_files.append((file_path, error_message))

    if non_compliant_files:
        return False, non_compliant_files
    return True, []

