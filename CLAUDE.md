# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个基于 AI 的智能书签摘要系统，自动化处理从 [bookmark-collection](https://github.com/zo0043/bookmark-collection) 收集的书签。系统使用 Jina Reader 提取网页内容，并通过 LLM 生成结构化摘要。

## 核心工作流程

### 主流程（bookmark_process_changes.py）

1. **监测书签变化**：从 bookmark-collection 仓库的 README.md 中读取最新书签
2. **内容提取**：使用 Jina Reader API (`https://r.jina.ai/{url}`) 获取 Markdown 格式的全文内容
3. **AI 摘要生成**：
   - 调用 OpenAI API 生成详细的列表式摘要
   - 生成一句话 TL;DR 总结
4. **文件组织**：
   - 按月份存储文件（`data/YYYYMM/` 目录）
   - 保存原始内容（`*_raw.md`）和摘要文件
   - 更新索引文件 `data/data.json`
5. **标签处理**：自动识别并归档带标签的书签

### 标签系统（process_tag_bookmark.py）

- 从书签 URL 行提取标签（格式：`#tag`）
- 按标签组织内容到 `data/tags/*.tag` 文件
- 生成标签摘要文件 `tag_summary.md`
- 特殊标签 `weekly` 用于标记需要进行周报分析的文章

### 关键词分析系统（keyword_analyzer.py）

**核心功能：** 自动识别书签中的高频关键词，生成深度分析报告和对比分析

**工作流程：**
1. **关键词提取**：使用 LLM 从书签标题和标签中提取 3-5 个核心关键词
2. **倒排索引构建**：构建关键词到文章的映射关系，保存到 `data/keyword_index.json`
3. **高频关键词筛选**：过滤频次 ≥ 3 的关键词（可配置）
4. **深度分析**：对每个高频关键词进行主题演变、核心观点、技术要点分析
5. **对比分析**：分析同一关键词下不同文章的共同点、差异和互补性
6. **报告生成**：生成独立的 Markdown 分析报告

**数据结构：**
- **关键词索引**: `data/keyword_index.json`
  ```json
  {
    "分布式系统": [
      {"url": "...", "title": "...", "timestamp": 123, "month": "202410", "summary_path": "..."},
      ...
    ]
  }
  ```
- **分析报告**: `data/keyword_analysis/{keyword-slug}.md`
  - 元数据（分析时间、文章数、时间跨度）
  - 文章列表（带链接）
  - 深度分析（主题演变、核心观点、技术要点）
  - 对比分析（共同观点、差异化视角、互补性、推荐阅读顺序）
- **分析索引**: `keyword_analysis_summary.md`

**增量更新机制：**
- 关键词索引支持增量构建（仅处理新书签）
- 每 10 个书签保存一次中间结果（防止中断丢失）
- 已处理的 URL 会被记录，避免重复提取

**容错策略：**
- 关键词提取失败时降级使用已有标签
- 摘要文件缺失时记录警告并跳过

## 环境配置

### 必需的环境变量

```bash
# OpenAI API 配置
OPENAI_API_KEY=sk-...           # OpenAI API 密钥
OPENAI_API_MODEL=gpt-4          # 可选，默认 gpt-4
OPENAI_API_ENDPOINT=https://... # 可选，自定义 API 端点
```

### Rye 包管理器使用

项目使用 [Rye](https://github.com/astral-sh/rye) 作为包管理器：

```bash
# 初始化环境
rye sync                    # 安装依赖，创建虚拟环境
rye add requests            # 添加新依赖
rye remove requests         # 移除依赖
rye run python script.py    # 在虚拟环境中运行命令

# 激活虚拟环境（手动操作时）
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

## 开发环境设置

```bash
# 使用 Rye（推荐方式）
rye sync                    # 安装依赖
rye run python -m bookmark_ai_summary.bookmark_process_changes  # 运行模块

# 或使用传统 pip 方式
pip install -r requirements.lock
python -m bookmark_ai_summary.bookmark_process_changes

# 环境变量配置
# 项目根目录已存在 .env 文件，直接编辑添加必要的环境变量：
# OPENAI_API_KEY=sk-...
# OPENAI_API_MODEL=gpt-4（可选）
```

## 常用命令

### 手动处理书签

```bash
# 处理新书签并生成摘要
python -m bookmark_ai_summary.bookmark_process_changes
# 或使用 rye
rye run python -m bookmark_ai_summary.bookmark_process_changes

# 仅更新标签摘要
python -m bookmark_ai_summary.process_tag_bookmark

# 生成周报（需要 weekly 标签的文章）
python -m bookmark_ai_summary.build_weekly_release

# 关键词分析（增量更新）
python -m bookmark_ai_summary.run_keyword_analysis

# 关键词分析（强制重建索引）
python -m bookmark_ai_summary.run_keyword_analysis --force-rebuild

# 关键词分析（自定义最小频次）
python -m bookmark_ai_summary.run_keyword_analysis --min-frequency 5
```

### 项目维护脚本

```bash
# 关键词分析健康检查
./scripts/keyword-analysis-health.sh

# 清理关键词分析数据
./scripts/keyword-analysis-cleanup.sh

# 查看项目统计信息
./scripts/keyword-analysis-health.sh --stats
```

### GitHub Actions 自动化

- **每周日 20:00 (北京时间)**：自动生成周报 Release
- **每周日 00:00 (UTC)**：处理 weekly 标签的文章

可通过仓库的 Actions 页面手动触发工作流。

## 关键数据结构

### SummarizedBookmark

```python
@dataclass
class SummarizedBookmark:
    month: str       # 格式：YYYYMM
    title: str       # 书签标题
    url: str         # 原始 URL
    timestamp: int   # Unix 时间戳
    tags: List[str]  # 标签列表
```

### 文件路径模式

- 摘要文件：`data/YYYYMM/YYYY-MM-DD-{slugified-title}.md`
- 原始内容：`data/YYYYMM/YYYY-MM-DD-{slugified-title}_raw.md`
- 标签文件：`data/tags/{tag-name}.tag`
- 索引文件：`data/data.json`
- 关键词索引：`data/keyword_index.json`
- 关键词分析报告：`data/keyword_analysis/{keyword-slug}.md`
- 关键词分析索引：`keyword_analysis_summary.md`

## LLM Prompt 策略

### 详细摘要 Prompt

系统使用结构化的 Prompt 生成多层次的列表式摘要：
- 强调使用 Markdown 列表格式
- 支持多层缩进和子列表
- 每项开头包含简短描述词
- 统一使用中文输出
- 参考示例：Trello 产品分析文章

### 一句话总结 Prompt

限制在 100 字以内，基于详细摘要生成精炼版本。

### 关键词提取 Prompt

从书签标题和标签中提取 3-5 个核心关键词（技术术语或主题词），优先技术术语，避免泛化词汇，中文输出。

### 关键词深度分析 Prompt

分析关键词主题的演变趋势、核心观点和技术要点，基于多篇文章摘要，使用 Markdown 列表格式。

### 关键词对比分析 Prompt

对比同一关键词下不同文章的共同观点、差异化视角、互补性，并建议阅读顺序。

## 架构设计要点

### 容错机制

- **Wayback Machine 存档**：失败时记录警告但不中断流程
- **API 调用**：使用 `@log_execution_time` 装饰器记录执行时间
- **文件操作**：自动创建必要的目录结构

### 文件命名规则

- 使用 `slugify()` 函数清理文件名中的特殊字符
- 移除文件系统非法字符：`/\:*?"<>|`
- URL 编码用于 README.md 中的链接路径

### 数据同步

1. 读取 `bookmark-collection/README.md` 获取新书签
2. 对比 `data/data.json` 中已处理的 URL
3. 处理未摘要的书签
4. 更新 `bookmark-ai-summary/README.md` 和 `data.json`

## 与外部系统集成

### bookmark-collection 仓库

- 源仓库：存储原始书签列表
- 格式：Markdown 列表 `- [Title](URL) #tag1 #tag2`
- 本项目作为消费者，定期拉取最新内容

### Jina Reader API

- 端点：`https://r.jina.ai/{url}`
- 功能：将网页转换为 Markdown 格式
- 无需认证，直接 GET 请求

## 关键词分析系统配置

### 配置常量（keyword_analyzer.py）

```python
# 关键词索引文件路径
KEYWORD_INDEX_PATH = "bookmark-ai-summary/data/keyword_index.json"

# 关键词分析报告目录
KEYWORD_ANALYSIS_DIR = "bookmark-ai-summary/data/keyword_analysis"

# 分析索引文件路径
KEYWORD_ANALYSIS_SUMMARY = "bookmark-ai-summary/keyword_analysis_summary.md"

# 最小关键词频次阈值（低于此值不生成分析报告）
MIN_KEYWORD_FREQUENCY = 3
```

### 可调参数

**1. 最小关键词频次（min_frequency）**
- **默认值**: 3
- **作用**: 只为出现频次 ≥ N 的关键词生成分析报告
- **调整方式**:
  ```bash
  # 命令行方式
  python -m bookmark_ai_summary.run_keyword_analysis --min-frequency 5

  # 代码方式（修改 MIN_KEYWORD_FREQUENCY 常量）
  ```
- **建议**:
  - 书签数量 < 50: 使用 `min_frequency=2`
  - 书签数量 50-200: 使用 `min_frequency=3`（默认）
  - 书签数量 > 200: 使用 `min_frequency=5`

**2. 关键词提取数量**
- **默认值**: 3-5 个
- **位置**: `extract_keywords_from_bookmark()` 函数的 Prompt
- **调整方式**: 修改 Prompt 中的 "3-5个" 为其他数值
- **建议**: 不建议超过 7 个，会导致关键词过于分散

**3. 索引保存频率**
- **默认值**: 每 10 个书签保存一次
- **位置**: `build_keyword_index()` 函数 `if new_count % 10 == 0`
- **调整方式**: 修改数值 10 为其他值
- **建议**:
  - 网络稳定: 可调整为 20-50
  - 网络不稳定: 保持 10 或降低到 5

**4. 关键词清洗规则**
- **位置**: `clean_keywords()` 函数
- **当前规则**:
  - 移除字符: `*#`"'数字.-`
  - 分隔符: `,，;；\n`
  - 长度限制: 2-20 字符
- **调整方式**: 修改正则表达式和过滤条件

### 性能优化配置

**1. API 调用优化**
- **批量提取**: 每次处理多个书签后统一保存索引
- **失败降级**: 关键词提取失败时使用已有标签
- **增量更新**: 仅处理新增书签，避免重复调用 API

**2. 内存优化**
- **文件读取**: 使用流式读取，避免一次性加载所有摘要
- **索引结构**: 使用倒排索引，O(1) 复杂度查询

**3. 执行模式**
```bash
# 增量模式（推荐日常使用）
python -m bookmark_ai_summary.run_keyword_analysis

# 强制重建模式（仅在索引损坏或需要全量更新时使用）
python -m bookmark_ai_summary.run_keyword_analysis --force-rebuild
```

### LLM Prompt 调优

**1. 关键词提取 Prompt 优化**
- **位置**: `extract_keywords_from_bookmark()`
- **可调整项**:
  - 关键词数量范围
  - 过滤规则（技术术语 vs 通用词汇）
  - 输出格式要求
  - 语言偏好（中文/英文）

**示例自定义 Prompt**:
```python
prompt = f"""从以下书签提取关键词：

要求：
1. 提取 5-7 个关键词（增加数量）
2. 包含英文缩写（如 AI、LLM、API）
3. 输出格式：中文,English

标题：{bookmark.title}
标签：{tags_str}
"""
```

**2. 深度分析 Prompt 优化**
- **位置**: `analyze_keyword_theme()`
- **可调整项**:
  - 分析维度（主题演变、技术要点、应用案例等）
  - 输出结构（列表 vs 段落）
  - 分析深度（简要 vs 详细）

**3. 对比分析 Prompt 优化**
- **位置**: `compare_articles()`
- **可调整项**:
  - 对比维度（理论 vs 实践、入门 vs 进阶等）
  - 推荐阅读顺序策略

### 数据管理

**1. 索引文件维护**
```bash
# 查看索引统计
cat data/keyword_index.json | jq 'to_entries | length'  # 关键词总数
cat data/keyword_index.json | jq '.[] | length' | awk '{sum+=$1} END {print sum}'  # 文章总数

# 备份索引
cp data/keyword_index.json data/keyword_index.json.backup

# 清空索引（重新构建）
rm data/keyword_index.json
python -m bookmark_ai_summary.run_keyword_analysis --force-rebuild
```

**2. 报告清理**
```bash
# 删除所有分析报告（保留索引）
rm -rf data/keyword_analysis/*.md

# 删除低频关键词报告（手动）
# 需根据 keyword_analysis_summary.md 中的频次手动删除
```

### 故障排查

**问题 1: 关键词提取失败**
- **现象**: 日志显示 "提取关键词失败"
- **原因**: OpenAI API 调用失败或返回格式错误
- **解决**:
  1. 检查 `OPENAI_API_KEY` 环境变量
  2. 查看日志中的详细错误信息
  3. 系统会自动降级使用已有标签

**问题 2: 索引文件损坏**
- **现象**: JSON 解析错误
- **解决**:
  ```bash
  # 恢复备份
  cp data/keyword_index.json.backup data/keyword_index.json

  # 或强制重建
  rm data/keyword_index.json
  python -m bookmark_ai_summary.run_keyword_analysis --force-rebuild
  ```

**问题 3: 内存占用过高**
- **原因**: 一次性加载大量文章摘要
- **解决**: 降低 `min_frequency` 参数，减少单个关键词的文章数量

**问题 4: 生成报告为空**
- **原因**: 没有满足 `min_frequency` 条件的关键词
- **解决**: 降低 `--min-frequency` 参数或增加书签数量

### 集成到自动化流程

**方式 1: 集成到主流程（不推荐）**
```python
# 在 bookmark_process_changes.py 的 main() 中
def main():
    process_bookmark_file()
    process_tag_summary()

    # 取消注释以启用
    from keyword_analyzer import process_keyword_analysis
    process_keyword_analysis(force_rebuild=False, min_frequency=3)
```

**方式 2: 定时任务（推荐）**
```bash
# crontab 示例（每周日凌晨 2 点执行）
0 2 * * 0 cd /path/to/bookmark-ai-summary && python -m bookmark_ai_summary.run_keyword_analysis

# GitHub Actions 示例
# .github/workflows/keyword_analysis.yml
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
      - name: Run Keyword Analysis
        run: python -m bookmark_ai_summary.run_keyword_analysis --min-frequency 3
```

### 成本估算

**OpenAI API 调用成本**（基于 GPT-4）:

- **关键词提取**: 约 200 tokens/书签
  - 100 个书签 ≈ 20,000 tokens ≈ $0.6
- **深度分析**: 约 3,000 tokens/关键词
  - 10 个关键词 ≈ 30,000 tokens ≈ $0.9
- **对比分析**: 约 3,000 tokens/关键词
  - 10 个关键词 ≈ 30,000 tokens ≈ $0.9

**总成本估算**: 100 个书签 → 10 个关键词 ≈ **$2.4**

**降低成本策略**:
1. 使用 `gpt-3.5-turbo` 替代 `gpt-4`（成本降低 90%）
2. 增加 `min_frequency` 减少分析的关键词数量
3. 使用增量更新模式，避免重复提取

## 项目结构说明

```
bookmark-ai-summary/
├── src/bookmark_ai_summary/          # 主要源码目录
│   ├── bookmark_process_changes.py   # 主流程：书签处理和摘要生成
│   ├── process_tag_bookmark.py       # 标签系统：按标签组织内容
│   ├── keyword_analyzer.py           # 关键词分析：深度分析和报告
│   ├── run_keyword_analysis.py       # 关键词分析入口脚本
│   └── build_weekly_release.py       # 周报生成：GitHub Release
├── data/                             # 数据存储目录
│   ├── YYYYMM/                       # 按月份组织的摘要文件
│   ├── tags/                         # 标签文件存储
│   ├── data.json                     # 主索引文件
│   └── keyword_analysis/             # 关键词分析报告
├── scripts/                          # 维护脚本
│   ├── keyword-analysis-health.sh    # 健康检查脚本
│   └── keyword-analysis-cleanup.sh   # 数据清理脚本
├── docs/                             # 文档目录
│   ├── keyword-analysis-quickstart.md # 关键词分析快速入门
│   └── keyword-analysis-config.md     # 关键词分析配置说明
└── .github/workflows/                # GitHub Actions 工作流
    ├── build_weekly_release.yml      # 周报自动生成
    └── process_weekly_articles.yml   # 周刊文章处理
```

## 核心模块依赖关系

```
bookmark_process_changes.py (主入口)
    ├── Jina Reader API (网页内容提取)
    ├── OpenAI API (AI 摘要生成)
    ├── process_tag_bookmark.py (标签处理)
    └── data/JSON 管理 (索引维护)

keyword_analyzer.py (独立模块)
    ├── OpenAI API (关键词提取、分析)
    ├── data/data.json (数据源)
    └── data/keyword_index.json (倒排索引)

build_weekly_release.py (自动化)
    ├── GitHub API (Release 创建)
    └── process_tag_bookmark.py (weekly 标签处理)
```

## 调试和故障排查

### 常见问题诊断

```bash
# 检查环境变量
echo $OPENAI_API_KEY

# 验证 OpenAI API 连接
curl -X POST "https://api.openai.com/v1/chat/completions" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "test"}]}'

# 测试 Jina Reader API
curl "https://r.jina.ai/https://example.com"

# 检查数据文件完整性
python -c "import json; print(json.load(open('data/data.json'))['bookmarks'][:5])"

# 关键词分析状态检查
./scripts/keyword-analysis-health.sh --verbose
```

### 日志和监控

系统使用 Python 标准 logging 模块，支持：
- 执行时间装饰器：`@log_execution_time`
- API 调用日志记录
- 错误和警告信息输出

## 注意事项

- 文件路径硬编码使用项目名称（`bookmark-ai-summary`、`bookmark-collection`）
- 当前月份和日期使用运行时动态生成（`CURRENT_MONTH`、`CURRENT_DATE`）
- 标签处理链通过 `deal_tags_chain()` 集中管理，新增特定标签需要修改此函数
- 周报分析功能（`process_weekly_articles`）当前为占位实现，LLM 分析逻辑待完善
- 关键词分析系统默认不集成到主流程，建议通过定时任务或手动执行
- 首次运行关键词分析需要处理所有历史书签，耗时较长且 API 成本较高
- 项目没有传统的单元测试，主要通过实际运行和脚本验证功能
