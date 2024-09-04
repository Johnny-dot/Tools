import os
import hashlib

class DetectDuplicate:
    def __init__(self, paraVo):
        self.paraVo = paraVo
        self._inPath = paraVo.getVal('inputUrl')
        self._pendingResources = {}  # {file_size: {md5: [file_paths]}}

    def get_file_md5(self, file_path, block_size=65536):
        md5 = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for block in iter(lambda: f.read(block_size), b''):
                    md5.update(block)
        except IOError as e:
            print(f"Error reading file {file_path}: {e}")
            return None
        return md5.hexdigest()

    def find_duplicates(self):
        self._pendingResources.clear()
        total_size = 0
        duplicate_groups = 0

        for root, dirs, files in os.walk(self._inPath):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                except OSError as e:
                    print(f"Error getting size for file {file_path}: {e}")
                    continue

                file_md5 = self.get_file_md5(file_path)
                if file_md5 is None:
                    continue

                # Initialize the file size key if it doesn't exist
                if file_size not in self._pendingResources:
                    self._pendingResources[file_size] = {}

                if file_md5 in self._pendingResources[file_size]:
                    self._pendingResources[file_size][file_md5].append(file_path)
                else:
                    self._pendingResources[file_size][file_md5] = [file_path]

        duplicates = {}
        for file_size, md5_dict in self._pendingResources.items():
            for md5, paths in md5_dict.items():
                if len(paths) > 1:
                    total_size += file_size * len(paths)
                    duplicate_groups += 1
                    duplicates[md5] = {'paths': paths, 'size': file_size}

        return duplicates, duplicate_groups, total_size

    def main(self):
        # 主入口，返回检测到的重复文件及统计信息
        return self.find_duplicates()
