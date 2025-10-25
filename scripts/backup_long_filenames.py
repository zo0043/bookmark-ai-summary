#!/usr/bin/env python3
"""
文件名备份和恢复脚本

提供对文件名迁移过程的完整备份和回滚功能。
"""

import json
import logging
import shutil
import sys
from pathlib import Path
from typing import Dict, List

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class BackupManager:
    def __init__(self, backup_dir: str = "backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)

    def create_full_backup(self, data_dir: str = "data") -> str:
        """创建完整的备份"""
        data_path = Path(data_dir)
        if not data_path.exists():
            logging.error(f"数据目录不存在: {data_path}")
            return ""

        timestamp = logging.Formatter().formatTime(
            logging.LogRecord('', 0, '', 0, '', (), None)
        ).replace(' ', '_').replace(':', '-')

        backup_name = f"full_backup_{timestamp}"
        backup_path = self.backup_dir / backup_name

        try:
            shutil.copytree(data_path, backup_path)
            logging.info(f"完整备份已创建: {backup_path}")
            return str(backup_path)
        except Exception as e:
            logging.error(f"创建完整备份失败: {e}")
            return ""

    def restore_full_backup(self, backup_name: str, data_dir: str = "data") -> bool:
        """从完整备份恢复"""
        backup_path = self.backup_dir / backup_name
        data_path = Path(data_dir)

        if not backup_path.exists():
            logging.error(f"备份不存在: {backup_path}")
            return False

        try:
            # 先备份当前数据
            current_backup = self.create_full_backup(data_dir)
            if current_backup:
                logging.info(f"当前数据已备份到: {current_backup}")

            # 删除现有数据目录
            if data_path.exists():
                shutil.rmtree(data_path)

            # 恢复备份数据
            shutil.copytree(backup_path, data_path)
            logging.info(f"数据已从备份恢复: {backup_name}")
            return True
        except Exception as e:
            logging.error(f"恢复备份失败: {e}")
            return False

    def list_backups(self) -> List[Dict]:
        """列出所有可用的备份"""
        backups = []

        if not self.backup_dir.exists():
            return backups

        for item in self.backup_dir.iterdir():
            if item.is_dir():
                backups.append({
                    'name': item.name,
                    'path': str(item),
                    'size': self._get_dir_size(item),
                    'created': item.stat().st_ctime
                })

        return sorted(backups, key=lambda x: x['created'], reverse=True)

    def _get_dir_size(self, path: Path) -> int:
        """获取目录大小"""
        total_size = 0
        try:
            for item in path.rglob('*'):
                if item.is_file():
                    total_size += item.stat().st_size
        except Exception:
            pass
        return total_size

    def rollback_migration(self, migration_log: str = "filename_migration_log.json") -> bool:
        """根据迁移日志回滚迁移"""
        log_path = Path(migration_log)

        if not log_path.exists():
            logging.error(f"迁移日志不存在: {migration_log}")
            return False

        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                log_data = json.load(f)

            migrations = log_data.get('migrations', [])
            if not migrations:
                logging.info("没有需要回滚的迁移")
                return True

            logging.info(f"开始回滚 {len(migrations)} 个文件迁移...")

            # 先备份当前状态
            current_backup = self.create_full_backup()
            if current_backup:
                logging.info(f"当前状态已备份到: {current_backup}")

            restored_count = 0
            for migration in migrations:
                old_path = Path(migration['old_path'])
                backup_path = Path(migration['backup_path'])
                new_path = Path(migration['new_path'])

                try:
                    # 恢复原始文件
                    if backup_path.exists():
                        shutil.copy2(backup_path, old_path)
                        logging.info(f"✓ 恢复: {migration['new_name']} -> {migration['old_name']}")
                        restored_count += 1

                    # 删除新文件（如果存在且不是备份）
                    if new_path.exists() and not new_path.name.endswith('.backup'):
                        new_path.unlink()

                except Exception as e:
                    logging.error(f"恢复失败 {migration['new_name']}: {e}")

            # 恢复 data.json
            data_json_backup = Path("data/data.json.backup")
            data_json_path = Path("data/data.json")
            if data_json_backup.exists():
                shutil.copy2(data_json_backup, data_json_path)
                logging.info("✓ 已恢复 data.json")

            logging.info(f"回滚完成! 恢复了 {restored_count} 个文件")
            return True

        except Exception as e:
            logging.error(f"回滚失败: {e}")
            return False

    def cleanup_old_backups(self, keep_count: int = 5) -> int:
        """清理旧的备份，保留最新的几个"""
        backups = self.list_backups()
        if len(backups) <= keep_count:
            return 0

        # 删除最旧的备份
        old_backups = backups[keep_count:]
        deleted_count = 0

        for backup in old_backups:
            try:
                backup_path = Path(backup['path'])
                shutil.rmtree(backup_path)
                logging.info(f"已删除旧备份: {backup['name']}")
                deleted_count += 1
            except Exception as e:
                logging.error(f"删除备份失败 {backup['name']}: {e}")

        return deleted_count

def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="文件名备份和恢复管理")
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 创建备份
    backup_parser = subparsers.add_parser('backup', help='创建完整备份')
    backup_parser.add_argument('--data-dir', default="data", help='数据目录路径')

    # 恢复备份
    restore_parser = subparsers.add_parser('restore', help='从备份恢复')
    restore_parser.add_argument('backup_name', help='备份名称')
    restore_parser.add_argument('--data-dir', default="data", help='数据目录路径')

    # 列出备份
    list_parser = subparsers.add_parser('list', help='列出所有备份')

    # 回滚迁移
    rollback_parser = subparsers.add_parser('rollback', help='回滚文件名迁移')
    rollback_parser.add_argument('--log-file', default="filename_migration_log.json", help='迁移日志文件')

    # 清理备份
    cleanup_parser = subparsers.add_parser('cleanup', help='清理旧备份')
    cleanup_parser.add_argument('--keep', type=int, default=5, help='保留的备份数量')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    manager = BackupManager()

    if args.command == 'backup':
        backup_path = manager.create_full_backup(args.data_dir)
        if backup_path:
            print(f"备份创建成功: {backup_path}")
        else:
            sys.exit(1)

    elif args.command == 'restore':
        success = manager.restore_full_backup(args.backup_name, args.data_dir)
        if success:
            print(f"数据恢复成功: {args.backup_name}")
        else:
            sys.exit(1)

    elif args.command == 'list':
        backups = manager.list_backups()
        if backups:
            print("可用备份:")
            for backup in backups:
                created_time = logging.Formatter().formatTime(
                    logging.LogRecord('', 0, '', 0, '', (), None, backup['created'])
                )
                size_mb = backup['size'] / (1024 * 1024)
                print(f"  {backup['name']} - {created_time} - {size_mb:.1f}MB")
        else:
            print("没有找到备份")

    elif args.command == 'rollback':
        success = manager.rollback_migration(args.log_file)
        if success:
            print("迁移回滚成功")
        else:
            sys.exit(1)

    elif args.command == 'cleanup':
        deleted = manager.cleanup_old_backups(args.keep)
        print(f"已删除 {deleted} 个旧备份")

if __name__ == "__main__":
    main()