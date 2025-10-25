#!/usr/bin/env python3
"""
文件名迁移脚本：将过长的文件名重命名为智能截断格式

该脚本处理现有的长文件名文件，将其重命名为符合长度限制的格式。
同时更新 data.json 中的路径引用，确保数据一致性。
"""

import json
import logging
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from bookmark_ai_summary.bookmark_process_changes import (
    MAX_FILENAME_LENGTH, slugify
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class FilenameMigrator:
    def __init__(self, data_dir: str = "data", data_json_path: str = "data/data.json"):
        self.data_dir = Path(data_dir)
        self.data_json_path = Path(data_json_path)
        self.migration_log: List[Dict] = []

    def find_long_files(self) -> List[Path]:
        """查找所有过长的文件名"""
        long_files = []

        if not self.data_dir.exists():
            logging.warning(f"数据目录不存在: {self.data_dir}")
            return long_files

        for file_path in self.data_dir.rglob("*.md"):
            filename = file_path.name
            # 移除扩展名检查基础名称长度
            base_name = Path(filename).stem

            if len(base_name) > MAX_FILENAME_LENGTH:
                long_files.append(file_path)

        return sorted(long_files, key=lambda x: len(x.name), reverse=True)

    def generate_new_filename(self, old_path: Path) -> str:
        """为长文件名生成新的短文件名"""
        old_name = old_path.stem  # 不包含扩展名
        extension = old_path.suffix

        # 尝试从文件名提取原始标题
        # 文件名格式：YYYY-MM-DD-title.md 或 YYYY-MM-DD-title_raw.md
        parts = old_name.split('-', 3)  # 分割为最多4部分
        if len(parts) >= 4:
            date_prefix = '-'.join(parts[:3])  # 保留日期部分
            title_part = parts[3]

            # 移除 _raw 后缀
            if title_part.endswith('_raw'):
                title_part = title_part[:-4]
                raw_suffix = '_raw'
            else:
                raw_suffix = ''

            # 使用改进的 slugify 函数处理标题
            new_title = slugify(title_part)
            new_name = f"{date_prefix}-{new_title}{raw_suffix}{extension}"
        else:
            # 如果无法解析格式，直接对整个文件名应用 slugify
            new_base = slugify(old_name)
            new_name = f"{new_base}{extension}"

        return new_name

    def update_data_json(self, file_mapping: Dict[str, str]) -> bool:
        """更新 data.json 中的文件路径引用"""
        if not self.data_json_path.exists():
            logging.warning(f"data.json 文件不存在: {self.data_json_path}")
            return False

        try:
            with open(self.data_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            updated = False

            # 更新 bookmarks 数组中的文件路径
            if 'bookmarks' in data:
                for bookmark in data['bookmarks']:
                    file_path = bookmark.get('file_path', '')
                    if file_path in file_mapping:
                        bookmark['file_path'] = file_mapping[file_path]
                        updated = True
                        logging.info(f"更新书签路径: {file_path} -> {file_mapping[file_path]}")

            # 更新索引中的其他路径引用
            for key, value in data.items():
                if isinstance(value, str) and value in file_mapping:
                    data[key] = file_mapping[value]
                    updated = True

            if updated:
                # 备份原文件
                backup_path = self.data_json_path.with_suffix('.json.backup')
                shutil.copy2(self.data_json_path, backup_path)
                logging.info(f"已备份 data.json 到 {backup_path}")

                # 写入更新后的数据
                with open(self.data_json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                logging.info("已更新 data.json 文件")
                return True
            else:
                logging.info("data.json 无需更新")
                return True

        except Exception as e:
            logging.error(f"更新 data.json 失败: {e}")
            return False

    def rename_files(self, dry_run: bool = False) -> Dict[str, str]:
        """重命名文件并返回映射关系"""
        long_files = self.find_long_files()

        if not long_files:
            logging.info("没有找到需要重命名的长文件名文件")
            return {}

        logging.info(f"找到 {len(long_files)} 个需要重命名的文件")

        file_mapping = {}

        for old_path in long_files:
            new_name = self.generate_new_filename(old_path)
            new_path = old_path.parent / new_name

            # 记录相对路径用于更新 data.json
            old_relative = str(old_path.relative_to(Path.cwd()))
            new_relative = str(new_path.relative_to(Path.cwd()))

            logging.info(f"处理文件: {old_path.name} ({len(old_path.name)} 字符)")
            logging.info(f"新文件名: {new_name} ({len(new_name)} 字符)")

            if new_path.exists():
                logging.warning(f"目标文件已存在，跳过: {new_path}")
                continue

            if not dry_run:
                try:
                    # 创建备份
                    backup_path = old_path.with_suffix(old_path.suffix + '.backup')
                    shutil.copy2(old_path, backup_path)

                    # 重命名文件
                    old_path.rename(new_path)

                    file_mapping[old_relative] = new_relative

                    # 记录迁移信息
                    self.migration_log.append({
                        'old_path': old_relative,
                        'new_path': new_relative,
                        'old_name': old_path.name,
                        'new_name': new_name,
                        'backup_path': str(backup_path.relative_to(Path.cwd()))
                    })

                    logging.info(f"✓ 重命名成功: {old_path.name} -> {new_name}")

                except Exception as e:
                    logging.error(f"重命名失败 {old_path.name}: {e}")
            else:
                logging.info(f"[DRY RUN] 将重命名: {old_path.name} -> {new_name}")
                file_mapping[old_relative] = new_relative

        return file_mapping

    def save_migration_log(self) -> None:
        """保存迁移日志"""
        if not self.migration_log:
            return

        log_path = Path("filename_migration_log.json")
        try:
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': logging.Formatter().formatTime(logging.LogRecord(
                        '', 0, '', 0, '', (), None
                    )),
                    'total_files': len(self.migration_log),
                    'migrations': self.migration_log
                }, f, ensure_ascii=False, indent=2)
            logging.info(f"迁移日志已保存到 {log_path}")
        except Exception as e:
            logging.error(f"保存迁移日志失败: {e}")

    def migrate(self, dry_run: bool = False) -> bool:
        """执行完整的迁移过程"""
        logging.info("开始文件名迁移...")

        if dry_run:
            logging.info("=== DRY RUN 模式 ===")

        # 步骤1: 重命名文件
        file_mapping = self.rename_files(dry_run=dry_run)

        if not file_mapping:
            logging.info("没有文件需要重命名")
            return True

        # 步骤2: 更新 data.json
        if not dry_run:
            if self.update_data_json(file_mapping):
                # 步骤3: 保存迁移日志
                self.save_migration_log()
                logging.info("迁移完成!")
                return True
            else:
                logging.error("迁移失败: 无法更新 data.json")
                return False
        else:
            logging.info("DRY RUN 完成")
            return True

def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="迁移过长的文件名")
    parser.add_argument("--dry-run", action="store_true",
                       help="只显示将要进行的操作，不实际执行")
    parser.add_argument("--data-dir", default="data",
                       help="数据目录路径 (默认: data)")
    parser.add_argument("--data-json", default="data/data.json",
                       help="data.json 文件路径 (默认: data/data.json)")

    args = parser.parse_args()

    migrator = FilenameMigrator(
        data_dir=args.data_dir,
        data_json_path=args.data_json
    )

    success = migrator.migrate(dry_run=args.dry_run)

    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()