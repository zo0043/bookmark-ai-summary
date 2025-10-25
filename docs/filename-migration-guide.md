# 文件名迁移指南

## 概述

本指南说明如何使用新的文件名优化功能迁移现有的长文件名文件。

## 问题现状

当前项目中存在超长文件名的文件，最长达到106字符：
```
2025-06-08-一人千面，永不降智！手把手教你如何通过mihomo强大的覆写功能，灵活配置代理与链式代理，制订相应...
```

## 解决方案

新的 `slugify()` 函数已实现智能截断 + 哈希后缀策略：
- 长度限制：80字符
- 智能截断：保留前50字符 + 后20字符 + "..." + 8位哈希
- 唯一性保证：通过MD5哈希避免冲突

## 迁移步骤

### 1. 创建备份

```bash
# 创建完整备份
python3 scripts/backup_long_filenames.py backup

# 列出所有备份
python3 scripts/backup_long_filenames.py list
```

### 2. 试运行迁移

```bash
# 只显示将要进行的操作，不实际执行
python3 scripts/migrate_long_filenames.py --dry-run
```

### 3. 执行迁移

```bash
# 实际执行迁移
python3 scripts/migrate_long_filenames.py

# 指定数据目录
python3 scripts/migrate_long_filenames.py --data-dir /path/to/data
```

### 4. 验证结果

迁移完成后，检查：
- 新文件名长度是否 ≤ 80字符
- data.json 文件是否正确更新
- 文件内容是否完整

## 迁移示例

### 原文件名
```
2025-06-08-一人千面，永不降智！手把手教你如何通过mihomo强大的覆写功能，灵活配置代理与链式代理，制订相应的分流规则，解决gpt降智，无限试用cursor---开发调优---linux-do_raw.md
```

### 迁移后
```
2025-06-08-一人千面，永不降智！手把手教你如何通过mihomo强大的覆写功能...-linux-do_raw_1a2b3c4d.md
```

## 回滚方法

如果迁移出现问题，可以使用以下方法回滚：

### 方法1：使用备份恢复
```bash
# 恢复到指定备份
python3 scripts/backup_long_filenames.py restore backup_2025_10_25_14-30-00
```

### 方法2：使用迁移日志回滚
```bash
# 根据迁移日志回滚
python3 scripts/backup_long_filenames.py rollback --log-file filename_migration_log.json
```

## 清理旧备份

```bash
# 保留最新的5个备份，删除其他
python3 scripts/backup_long_filenames.py cleanup --keep 5
```

## 注意事项

1. **停止写入操作**：迁移期间请停止任何对数据文件的写入操作
2. **磁盘空间**：确保有足够磁盘空间存储备份
3. **权限检查**：确保有权限读取和修改所有相关文件
4. **验证完整性**：迁移后务必验证文件完整性和数据一致性

## 测试验证

### 运行 slugify 函数测试
```bash
python3 scripts/test_slugify_standalone.py
```

### 手动验证文件名长度
```python
import os
from bookmark_ai_summary.bookmark_process_changes import slugify

# 测试长文件名
long_title = "这是一个很长的标题用来测试..."
print(f"原长度: {len(long_title)}")
result = slugify(long_title)
print(f"新长度: {len(result)}")
print(f"结果: {result}")
```

## 故障排除

### 问题1：导入模块错误
```
ModuleNotFoundError: No module named 'waybackpy'
```
**解决方案**：
```bash
# 安装依赖
pip install -r requirements.lock
# 或使用 rye
rye sync
```

### 问题2：文件名冲突
**现象**：迁移脚本提示目标文件已存在
**解决方案**：
1. 检查是否有重复的备份文件
2. 手动删除冲突的备份文件
3. 重新运行迁移

### 问题3：权限错误
**现象**：无法创建备份或重命名文件
**解决方案**：
```bash
# 检查文件权限
ls -la data/
# 修改权限（如果需要）
chmod -R 755 data/
```

## 配置调整

如需调整文件名长度限制，请编辑：
`src/bookmark_ai_summary/bookmark_process_changes.py`

```python
# -- 文件名长度配置 --
MAX_FILENAME_LENGTH = 80          # 调整此值
HASH_LENGTH = 8                  # 哈希后缀长度
TRUNCATE_PREFIX_LENGTH = 50      # 前缀长度
TRUNCATE_SUFFIX_LENGTH = 20      # 后缀长度
SEPARATOR = "..."                # 分隔符
```

调整后需重新运行迁移脚本。