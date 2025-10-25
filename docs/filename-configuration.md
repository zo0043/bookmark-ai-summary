# 文件名长度配置说明

## 配置参数

在 `src/bookmark_ai_summary/bookmark_process_changes.py` 中定义了以下配置常量：

```python
# -- 文件名长度配置 --
MAX_FILENAME_LENGTH = 80          # 最大文件名长度
HASH_LENGTH = 8                  # 哈希后缀长度
TRUNCATE_PREFIX_LENGTH = 50      # 保留前缀长度
TRUNCATE_SUFFIX_LENGTH = 20      # 保留后缀长度
SEPARATOR = "..."                # 截断分隔符
```

## 参数说明

### MAX_FILENAME_LENGTH
- **默认值**: 80
- **说明**: 文件名的最大字符长度（不含扩展名）
- **建议范围**: 60-100
- **注意**: 不同文件系统有不同的限制，建议保持在 255 字符以内

### HASH_LENGTH
- **默认值**: 8
- **说明**: 哈希后缀的长度，用于确保文件名唯一性
- **建议范围**: 6-12
- **权衡**:
  - 较短（4-6位）：可能产生冲突
  - 较长（10-12位）：占用更多空间，但冲突概率极低

### TRUNCATE_PREFIX_LENGTH
- **默认值**: 50
- **说明**: 截断时保留的文件名前缀长度
- **建议范围**: 30-60

### TRUNCATE_SUFFIX_LENGTH
- **默认值**: 20
- **说明**: 截断时保留的文件名后缀长度
- **建议范围**: 15-30

### SEPARATOR
- **默认值**: "..."
- **说明**: 截断部分的分隔符
- **可选值**: "...", "~", "---", "- truncated -"

## 截断逻辑

当文件名超过 `MAX_FILENAME_LENGTH` 时：

1. 计算可用长度：`MAX_FILENAME_LENGTH - len(SEPARATOR) - HASH_LENGTH`
2. 分配前缀和后缀长度：通常各占可用长度的一半
3. 构建新文件名：`{prefix}{SEPARATOR}{suffix}_{hash}`
4. 确保最终长度不超过限制

## 配置示例

### 保守配置（更短的文件名）
```python
MAX_FILENAME_LENGTH = 60
HASH_LENGTH = 6
TRUNCATE_PREFIX_LENGTH = 35
TRUNCATE_SUFFIX_LENGTH = 15
```

### 宽松配置（更长的文件名）
```python
MAX_FILENAME_LENGTH = 100
HASH_LENGTH = 8
TRUNCATE_PREFIX_LENGTH = 60
TRUNCATE_SUFFIX_LENGTH = 30
```

### 中文优化配置
```python
MAX_FILENAME_LENGTH = 75          # 中文字符占位较多
HASH_LENGTH = 6                  # 减少哈希长度
TRUNCATE_PREFIX_LENGTH = 45      # 平衡前后缀
TRUNCATE_SUFFIX_LENGTH = 20
SEPARATOR = "…-"                  # 使用中文省略号
```

## 文件名示例

假设原标题为：
```
【网站自荐】投资策略模拟器---通过直观可视化界面和详细数据分析，让用户深入了解各种投资策略优劣，从而做出更明智投资决策-·-issue-#5288-·-ruanyf-weekly
```

使用默认配置的结果：
```
【网站自荐】投资策略模拟器---通过直观可视化界面...-#5288-·-ruanyf-weekly_a1b2c3d4.md
```

长度：约 80 字符（含扩展名）

## 注意事项

1. **向后兼容**: 新配置只影响新生成的文件，现有文件需要通过迁移脚本处理
2. **唯一性保证**: 哈希机制确保即使相同前缀后缀也不会冲突
3. **可读性平衡**: 截断策略保留关键信息，同时控制长度
4. **系统兼容**: 80 字符长度确保在主流文件系统上正常工作

## 调整建议

根据实际使用情况调整：

- 如果发现文件名仍然过长 → 减少 `MAX_FILENAME_LENGTH`
- 如果发现文件名冲突 → 增加 `HASH_LENGTH`
- 如果可读性不够 → 调整 `TRUNCATE_*_LENGTH` 参数
- 如果特定语言表现不佳 → 修改 `SEPARATOR` 符号