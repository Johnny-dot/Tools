import os
import hashlib
import time
import json
import fnmatch

from sample.src_references.common.utils import FileUtil, FolderUtil


class DetectDuplicate:
    def __init__(self, paraVo):
        self.paraVo = paraVo
        self._inPath = paraVo.getVal('inputUrl')
        self._pendingResources = {}  # {file_size: {md5: [file_paths]}}
        self._match_pattern = paraVo.getVal('match_text')  # 获取匹配词

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

    def convert_size(self, size_bytes):
        """将字节转换为MB或GB的单位，按照Windows文件管理系统的显示规则。"""
        if size_bytes < 1024:
            return f"{size_bytes} Bytes"
        elif size_bytes < 1024 ** 2:
            return f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 ** 3:
            return f"{size_bytes / 1024 ** 2:.2f} MB"
        else:
            return f"{size_bytes / 1024 ** 3:.2f} GB"

    def file_matches_pattern(self, file_path):
        """检查文件路径是否与匹配词的通配符匹配。"""
        if not self._match_pattern:
            return True  # 如果没有设定匹配词，则不过滤，所有文件都匹配
        return fnmatch.fnmatch(file_path, self._match_pattern)

    def find_duplicates(self):
        self._pendingResources.clear()
        total_size = 0
        duplicate_groups = 0

        for root, dirs, files in os.walk(self._inPath):
            for file in files:
                file_path = os.path.join(root, file)

                # 检查文件是否符合通配符匹配词
                if not self.file_matches_pattern(file_path):
                    print(f"Not Matched: {file_path}")  # 调试输出
                    continue

                try:
                    file_size = os.path.getsize(file_path)
                except OSError as e:
                    print(f"Error getting size for file {file_path}: {e}")
                    continue

                file_md5 = self.get_file_md5(file_path)
                if file_md5 is None:
                    continue

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
                    duplicates[md5] = {
                        'paths': paths,
                        'size': file_size,
                        'formatted_size': self.convert_size(file_size)
                    }

        return duplicates, duplicate_groups, total_size

    def main(self):
        # 主入口，返回检测到的重复文件及统计信息
        duplicates, duplicate_groups, total_size = self.find_duplicates()

        # 按照 size 从大到小排序
        sorted_duplicates = dict(sorted(duplicates.items(), key=lambda x: x[1]['size'], reverse=True))

        # 获取输出路径
        output_path = self.paraVo.getFuncOutPath()

        # 使用当前时间戳生成唯一文件名
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = FolderUtil.join(output_path, f"duplicates_{timestamp}.json")

        # 将重复文件信息持久化为 JSON 格式
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(sorted_duplicates, f, ensure_ascii=False, indent=4)
        except IOError as error:
            print(f"写文件时发生错误! {error}")

        # 输出日志或提示
        print(f"检测到 {duplicate_groups} 组重复文件，总大小为 {total_size} 字节。")
        return duplicates, duplicate_groups, total_size
