# 关键词分析系统快速入门

## 安装和准备

### 1. 环境要求
```bash
# Python 版本
python >= 3.8

# 必需的环境变量
export OPENAI_API_KEY="sk-your-api-key-here"
export OPENAI_API_MODEL="gpt-4"  # 可选，默认 gpt-4
```

### 2. 安装依赖
```bash
# 使用 pip
pip install -r requirements.lock

# 或使用 Rye（推荐）
rye sync
```

## 快速开始

### 基础使用（推荐）

```bash
# 1. 增量分析新书签（日常使用）
python -m bookmark_ai_summary.run_keyword_analysis

# 2. 查看分析结果
cat keyword_analysis_summary.md
ls data/keyword_analysis/
```

### 高级配置

```bash
# 3. 强制重建所有索引（首次运行或修复时）
python -m bookmark_ai_summary.run_keyword_analysis --force-rebuild

# 4. 自定义频次阈值（仅分析高频关键词）
python -m bookmark_ai_summary.run_keyword_analysis --min-frequency 5

# 5. 查看帮助信息
python -m bookmark_ai_summary.run_keyword_analysis --help
```

## 输出文件说明

### 1. 关键词索引
```bash
# 查看关键词倒排索引
cat data/keyword_index.json | jq 'keys'  # 所有关键词
cat data/keyword_index.json | jq '.分布式系统 | length'  # 特定关键词的文章数
```

### 2. 分析报告
```bash
# 查看生成的分析报告
ls data/keyword_analysis/*.md

# 查看特定关键词分析
cat data/keyword_analysis/分布式系统.md
```

### 3. 分析索引
```bash
# 查看分析报告索引
cat keyword_analysis_summary.md
```

## 常用命令示例

### 场景 1: 日常维护
```bash
# 每天运行一次增量更新
python -m bookmark_ai_summary.run_keyword_analysis

# 查看本周新增的高频关键词
grep "篇" keyword_analysis_summary.md | head -10
```

### 场景 2: 质量优化
```bash
# 提高分析质量，仅分析出现5次以上的关键词
python -m bookmark_ai_summary.run_keyword_analysis --min-frequency 5

# 检查分析结果
ls -la data/keyword_analysis/ | wc -l  # 报告数量
```

### 场景 3: 故障恢复
```bash
# 索引损坏时重建
rm data/keyword_index.json
python -m bookmark_ai_summary.run_keyword_analysis --force-rebuild

# 验证重建结果
python -c "import json; print('Keywords:', len(json.load(open('data/keyword_index.json'))))"
```

### 场景 4: 数据分析
```bash
# 统计关键词分布
cat data/keyword_index.json | jq '.[] | length' | sort -n | tail -10

# 查找最受欢迎的主题
grep -E "^\- \[.*\].*篇" keyword_analysis_summary.md | head -20
```

## 自动化设置

### 定时任务
```bash
# 添加到 crontab
crontab -e

# 每周日凌晨2点自动分析
0 2 * * 0 cd /path/to/bookmark-ai-summary && python -m bookmark_ai_summary.run_keyword_analysis

# 每天凌晨1点高频更新
0 1 * * * cd /path/to/bookmark-ai-summary && python -m bookmark_ai_summary.run_keyword_analysis --min-frequency 2
```

### GitHub Actions
```yaml
# .github/workflows/keyword-analysis.yml
name: Weekly Keyword Analysis
on:
  schedule:
    - cron: '0 2 * * 0'  # 每周日 UTC 2:00
  workflow_dispatch:

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
      - name: Run analysis
        run: python -m bookmark_ai_summary.run_keyword_analysis --min-frequency 3
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      - name: Commit results
        run: |
          git add data/keyword_analysis/ keyword_analysis_summary.md data/keyword_index.json
          git commit -m "Auto update keyword analysis" || exit 0
          git push
```

## 故障排查快速指南

### 常见问题

1. **API 错误**
```bash
# 检查 API Key
echo $OPENAI_API_KEY

# 测试 API 连接
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
```

2. **索引文件问题**
```bash
# 检查索引文件
ls -lh data/keyword_index.json
python -c "import json; print(json.load(open('data/keyword_index.json'))['分布式系统'][:2])"

# 重建索引
python -m bookmark_ai_summary.run_keyword_analysis --force-rebuild
```

3. **权限问题**
```bash
# 确保目录可写
mkdir -p data/keyword_analysis
chmod 755 data/keyword_analysis
```

### 日志查看
```bash
# 运行时查看详细日志
python -m bookmark_ai_summary.run_keyword_analysis 2>&1 | tee keyword_analysis.log

# 过滤关键信息
grep "关键词分析完成" keyword_analysis.log
grep "找到.*高频关键词" keyword_analysis.log
```

## 性能调优

### 成本控制
```bash
# 使用 GPT-3.5 降低成本
export OPENAI_API_MODEL="gpt-3.5-turbo"

# 增加频次阈值减少分析量
python -m bookmark_ai_summary.run_keyword_analysis --min-frequency 10
```

### 速度优化
```bash
# 减少保存频率（网络稳定时）
# 修改 keyword_analyzer.py 中的 INDEX_SAVE_INTERVAL = 50

# 降低分析深度
# 修改 run_keyword_analysis.py 中的默认 --min-frequency = 5
```

## 进阶用法

### 自定义 Prompt
```python
# 编辑 keyword_analyzer.py 中的 extract_keywords_from_bookmark 函数
prompt = f"""请从以下书签信息中提取 5-7 个关键词：

要求：
1. 包含英文缩写
2. 重视技术术语
3. 输出格式：关键词1,关键词2,关键词3

标题：{bookmark.title}
标签：{tags_str}
"""
```

### 批量处理
```bash
# 处理特定范围的书签
# 修改 keyword_analyzer.py 中的过滤逻辑
for bookmark in all_bookmarks:
    if bookmark.timestamp > start_timestamp:
        # 只处理新书签
        keywords = extract_keywords_from_bookmark(bookmark)
```

### 数据导出
```bash
# 导出关键词统计
cat data/keyword_index.json | jq -r 'to_entries[] | "\(.key),\(.value | length)"' > keyword_stats.csv

# 导出文章关联
cat data/keyword_index.json | jq -r 'to_entries[] | .key as $k | .value[] | "\($k),\(.title),\(.url)"' > keyword_articles.csv
```

## 监控和维护

### 健康检查
```bash
#!/bin/bash
# health_check.sh

echo "=== 关键词分析系统健康检查 ==="

# 检查索引文件
if [ -f "data/keyword_index.json" ]; then
    echo "✅ 索引文件存在"
    python -c "import json; print(f'关键词数量: {len(json.load(open(\"data/keyword_index.json\")))}')"
else
    echo "❌ 索引文件不存在"
fi

# 检查分析报告
if [ -d "data/keyword_analysis" ]; then
    report_count=$(ls data/keyword_analysis/*.md 2>/dev/null | wc -l)
    echo "✅ 分析报告目录存在，包含 $report_count 个报告"
else
    echo "❌ 分析报告目录不存在"
fi

# 检查索引文件
if [ -f "keyword_analysis_summary.md" ]; then
    echo "✅ 分析索引文件存在"
else
    echo "❌ 分析索引文件不存在"
fi

echo "=== 检查完成 ==="
```

### 清理脚本
```bash
#!/bin/bash
# cleanup.sh

echo "=== 清理低质量报告 ==="

# 删除空报告
find data/keyword_analysis -name "*.md" -size 0 -delete

# 删除过旧的备份文件
find . -name "keyword_index.json.backup.*" -mtime +30 -delete

echo "=== 清理完成 ==="
```

## 下一步

1. **阅读完整配置文档**: [keyword-analysis-config.md](keyword-analysis-config.md)
2. **了解项目架构**: [../README.md](../README.md)
3. **查看主流程文档**: [../docs/bookmark-process-guide.md](bookmark-process-guide.md)
4. **参与贡献**: 请参考 [CONTRIBUTING.md](../CONTRIBUTING.md)

## 支持和反馈

如遇到问题或有改进建议，请：
1. 查看本文档的故障排查部分
2. 检查 [Issues](https://github.com/zo0043/bookmark-ai-summary/issues)
3. 提交新的 Issue 或 Pull Request