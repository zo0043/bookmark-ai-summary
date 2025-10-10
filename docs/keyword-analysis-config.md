# 关键词分析系统配置指南

## 概述

关键词分析系统是 bookmark-ai-summary 的核心功能模块，自动从书签中提取关键词并生成深度分析报告。本文档提供详细的配置说明和使用指南。

## 核心功能

### 1. 关键词提取
- **技术**: 使用 OpenAI API 从书签标题和标签中提取 3-5 个核心关键词
- **策略**: 优先技术术语、框架名称、概念名词，避免泛化词汇
- **降级**: API 失败时使用已有标签作为关键词

### 2. 倒排索引构建
- **数据结构**: `关键词 -> 文章列表` 的映射关系
- **增量更新**: 仅处理新增书签，避免重复工作
- **持久化**: 保存到 `data/keyword_index.json`

### 3. 深度分析报告
- **频次过滤**: 仅分析出现频次 ≥ N 的关键词
- **内容分析**: 主题演变、核心观点、技术要点
- **对比分析**: 共同观点、差异化视角、互补性、阅读顺序

## 配置参数

### 核心常量 (keyword_analyzer.py)

```python
# 关键词索引文件路径
KEYWORD_INDEX_PATH = "bookmark-ai-summary/data/keyword_index.json"

# 关键词分析报告目录
KEYWORD_ANALYSIS_DIR = "bookmark-ai-summary/data/keyword_analysis"

# 分析索引文件路径
KEYWORD_ANALYSIS_SUMMARY = "bookmark-ai-summary/keyword_analysis_summary.md"

# 最小关键词频次阈值（低于此值不生成分析报告）
MIN_KEYWORD_FREQUENCY = 3

# 关键词长度限制
KEYWORD_MIN_LENGTH = 2  # 最小长度
KEYWORD_MAX_LENGTH = 20  # 最大长度

# 索引保存间隔（每N个书签保存一次中间结果）
INDEX_SAVE_INTERVAL = 10
```

### 命令行参数

#### 基本用法
```bash
# 增量更新（推荐日常使用）
python -m bookmark_ai_summary.run_keyword_analysis

# 强制重建全部索引
python -m bookmark_ai_summary.run_keyword_analysis --force-rebuild

# 自定义最小频次
python -m bookmark_ai_summary.run_keyword_analysis --min-frequency 5
```

#### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--force-rebuild` | flag | False | 强制重建关键词索引，忽略已有数据 |
| `--min-frequency` | int | 3 | 最小关键词频次，低于此值不生成报告 |

## 使用场景配置

### 1. 日常增量更新

**适用场景**: 每日/每周定期运行，处理新书签

**配置**:
```bash
python -m bookmark_ai_summary.run_keyword_analysis
```

**特点**:
- 仅处理新增书签，效率高
- 保持现有分析结果
- 增量成本极低

### 2. 全量重建

**适用场景**: 索引损坏、规则变更、首次运行

**配置**:
```bash
python -m bookmark_ai_summary.run_keyword_analysis --force-rebuild
```

**特点**:
- 处理所有历史书签
- 重建完整索引
- API 调用成本较高

### 3. 高质量分析

**适用场景**: 书签数量 > 200，需要更精准的分析

**配置**:
```bash
python -m bookmark_ai_summary.run_keyword_analysis --min-frequency 5
```

**特点**:
- 仅分析高频关键词
- 分析质量更高
- 减少噪音关键词

## 性能调优配置

### 1. API 调用优化

**批量处理策略**:
```python
# 修改 INDEX_SAVE_INTERVAL 调整保存频率
INDEX_SAVE_INTERVAL = 20  # 网络稳定时可增加
INDEX_SAVE_INTERVAL = 5   # 网络不稳定时可降低
```

**关键词提取优化**:
```python
# 修改 extract_keywords_from_bookmark() 中的 Prompt
prompt = f"""请从以下书签信息中提取 5-7 个最核心的关键词。
# 增加关键词数量，但注意成本增加
```

### 2. 内存优化

**适用场景**: 大量书签（>1000）

**策略**:
- 降低 `--min-frequency` 参数
- 分批处理，避免一次性加载过多摘要
- 定期清理低频关键词报告

### 3. 存储优化

**索引文件管理**:
```bash
# 查看索引统计
cat data/keyword_index.json | jq 'to_entries | length'  # 关键词总数
cat data/keyword_index.json | jq '.[] | length' | awk '{sum+=$1} END {print sum}'  # 文章总数

# 备份索引
cp data/keyword_index.json data/keyword_index.json.backup

# 清理低频关键词（手动）
# 编辑 keyword_index.json 删除不需要的条目
```

## LLM Prompt 配置

### 1. 关键词提取 Prompt

**位置**: `extract_keywords_from_bookmark()` 函数

**自定义示例**:
```python
prompt = f"""请从以下书签信息中提取关键词：

要求：
1. 提取 5-7 个关键词（增加数量）
2. 包含英文缩写（如 AI、LLM、API）
3. 输出格式：中文,English

标题：{bookmark.title}
标签：{tags_str}

输出示例：分布式系统,Consensus Algorithm,Raft,共识协议
"""
```

### 2. 深度分析 Prompt

**位置**: `analyze_keyword_theme()` 函数

**可调整维度**:
- 分析深度（简要 vs 详细）
- 输出结构（列表 vs 段落）
- 分析角度（技术 vs 业务）

### 3. 对比分析 Prompt

**位置**: `compare_articles()` 函数

**可调整维度**:
- 对比粒度（粗粒度 vs 细粒度）
- 阅读建议策略
- 互补性分析深度

## 自动化集成配置

### 1. 定时任务 (cron)

**设置**:
```bash
# 每周日凌晨 2 点执行
0 2 * * 0 cd /path/to/bookmark-ai-summary && python -m bookmark_ai_summary.run_keyword_analysis

# 每天凌晨 1 点执行（高频更新）
0 1 * * * cd /path/to/bookmark-ai-summary && python -m bookmark_ai_summary.run_keyword_analysis --min-frequency 2
```

### 2. GitHub Actions

**工作流文件**: `.github/workflows/keyword_analysis.yml`

```yaml
name: Weekly Keyword Analysis

on:
  schedule:
    - cron: '0 2 * * 0'  # 每周日 UTC 2:00
  workflow_dispatch:  # 支持手动触发

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.lock

      - name: Run Keyword Analysis
        run: python -m bookmark_ai_summary.run_keyword_analysis --min-frequency 3
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}

      - name: Commit results
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add data/keyword_analysis/ keyword_analysis_summary.md data/keyword_index.json
          git commit -m "Auto update keyword analysis" || exit 0
          git push
```

### 3. 主流程集成

**可选**: 集成到书签处理主流程

```python
# 在 bookmark_process_changes.py 的 main() 函数末尾添加
if __name__ == "__main__":
    process_bookmark_file()
    process_tag_summary()

    # 关键词分析（可选，推荐独立运行）
    # from keyword_analyzer import process_keyword_analysis
    # process_keyword_analysis(force_rebuild=False, min_frequency=3)
```

## 成本估算

### OpenAI API 调用成本（GPT-4）

| 操作 | Tokens/次 | 100个书签成本 | 说明 |
|------|-----------|---------------|------|
| 关键词提取 | ~200 | ~$0.6 | 每书签1次调用 |
| 深度分析 | ~3,000 | ~$0.9/关键词 | 10个关键词 |
| 对比分析 | ~3,000 | ~$0.9/关键词 | 10个关键词 |

**总成本**: 100个书签 → 10个关键词 ≈ **$2.4**

### 成本优化策略

1. **使用更便宜的模型**: GPT-3.5-turbo（成本降低 90%）
2. **增加频次阈值**: `--min-frequency 5` 减少分析的关键词数量
3. **增量更新**: 默认模式，避免重复处理
4. **批量处理**: 调整 `INDEX_SAVE_INTERVAL` 减少中断

## 故障排查

### 问题 1: 关键词提取失败

**现象**: 日志显示 "提取关键词失败"

**排查步骤**:
1. 检查环境变量: `echo $OPENAI_API_KEY`
2. 验证 API 有效性: 手动调用 OpenAI API
3. 检查网络连接

**解决方案**:
- 更新有效的 API Key
- 检查 API 额度和配额
- 系统会自动降级使用已有标签

### 问题 2: 索引文件损坏

**现象**: JSON 解析错误

**解决方案**:
```bash
# 恢复备份
cp data/keyword_index.json.backup data/keyword_index.json

# 或强制重建
rm data/keyword_index.json
python -m bookmark_ai_summary.run_keyword_analysis --force-rebuild
```

### 问题 3: 内存占用过高

**原因**: 一次性加载大量文章摘要

**解决方案**:
- 降低 `--min-frequency` 参数
- 减少单个关键词的文章数量
- 分批处理，避免高峰期运行

### 问题 4: 生成报告为空

**原因**: 没有满足频次条件的关键词

**解决方案**:
- 降低 `--min-frequency` 参数
- 增加书签数量
- 检查索引文件是否为空

## 监控和维护

### 1. 日志监控

**关键日志**:
```
找到 X 个高频关键词（≥N篇）
开始生成关键词分析报告: keyword (X篇文章)
索引构建完成，共处理 X 个新书签，总关键词数: Y
```

### 2. 文件监控

**定期检查**:
```bash
# 检查索引文件大小和更新时间
ls -lh data/keyword_index.json

# 检查分析报告数量
ls -1 data/keyword_analysis/*.md | wc -l

# 检查索引文件完整性
python -c "import json; print('Index valid:', len(json.load(open('data/keyword_index.json'))))"
```

### 3. 性能监控

**监控指标**:
- API 调用次数和成本
- 处理时间（书签数量 / 执行时间）
- 索引文件大小
- 生成报告数量

## 最佳实践

### 1. 运行策略
- **日常使用**: 增量更新模式
- **重要更新**: 全量重建前先备份
- **成本控制**: 合理设置频次阈值

### 2. 数据管理
- 定期备份索引文件
- 清理低质量分析报告
- 监控存储空间使用

### 3. 质量保证
- 定期检查分析报告质量
- 调优 Prompt 以适应领域特点
- 根据反馈调整关键词提取策略

## 版本兼容性

- **Python**: >= 3.8
- **依赖**: 与主项目一致
- **API**: OpenAI GPT-4 / GPT-3.5-turbo

## 更新日志

### v1.0 (当前版本)
- 基础关键词提取和分析功能
- 倒排索引构建
- 增量更新支持
- 命令行接口

### 计划功能
- 支持更多 LLM 模型
- 关键词关联分析
- 主题聚类
- 可视化报告