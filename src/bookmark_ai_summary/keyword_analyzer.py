# 使用方法:
# 1. 独立运行关键词分析:
#    python -m bookmark_ai_summary.run_keyword_analysis
# 2. 在主流程中自动执行:
#    python -m bookmark_ai_summary.bookmark_process_changes
# 3. 强制重建索引:
#    python -m bookmark_ai_summary.run_keyword_analysis --force-rebuild

import json
import logging
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from collections import defaultdict

from bookmark_process_changes import (
    call_openai_api,
    log_execution_time,
    SummarizedBookmark,
    BOOKMARK_SUMMARY_REPO_DATA_DIR,
)

# -- 常量配置 --
KEYWORD_INDEX_PATH = Path(f"{BOOKMARK_SUMMARY_REPO_DATA_DIR}/keyword_index.json")
KEYWORD_ANALYSIS_DIR = Path(f"{BOOKMARK_SUMMARY_REPO_DATA_DIR}/keyword_analysis")
KEYWORD_ANALYSIS_SUMMARY = Path("bookmark-ai-summary/keyword_analysis_summary.md")
MIN_KEYWORD_FREQUENCY = 3  # 最小关键词频次（低于此值不生成分析报告）
KEYWORD_MIN_LENGTH = 2  # 关键词最小长度
KEYWORD_MAX_LENGTH = 20  # 关键词最大长度
INDEX_SAVE_INTERVAL = 10  # 索引保存间隔（每N个书签保存一次）

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@dataclass
class KeywordArticle:
    """关键词关联的文章元数据"""
    url: str
    title: str
    timestamp: int
    month: str
    summary_path: str


def clean_keywords(raw_keywords: str) -> List[str]:
    """清洗LLM返回的关键词字符串"""
    # 移除可能的markdown格式、编号、引号等
    cleaned = re.sub(r'[*#`"\'\d\.\-]', '', raw_keywords)
    # 按逗号、分号、换行符分割
    keywords = re.split(r'[,，;；\n]+', cleaned)
    # 去除空白、去重
    keywords = [kw.strip() for kw in keywords if kw.strip()]
    # 过滤过短或过长的关键词
    keywords = [kw for kw in keywords if KEYWORD_MIN_LENGTH <= len(kw) <= KEYWORD_MAX_LENGTH]
    return list(set(keywords))


@log_execution_time
def extract_keywords_from_bookmark(bookmark: SummarizedBookmark) -> List[str]:
    """从单个书签中提取关键词"""
    tags_str = ", ".join(bookmark.tags) if bookmark.tags else "无"

    prompt = f"""请从以下书签信息中提取3-5个最核心的关键词（技术术语或主题词）。

要求：
1. 优先提取技术术语、框架名称、概念名词
2. 避免泛化词汇（如"技术"、"方法"、"介绍"）
3. 使用中文输出
4. 仅输出关键词，用逗号分隔，不要解释

书签标题：{bookmark.title}
已有标签：{tags_str}

输出格式示例：分布式系统,一致性算法,Raft,共识协议
"""

    try:
        raw_keywords = call_openai_api(prompt, "")
        keywords = clean_keywords(raw_keywords)
        logging.info(f"提取关键词成功: {bookmark.title} -> {keywords}")
        return keywords
    except Exception as e:
        logging.error(f"提取关键词失败: {bookmark.title}, 错误: {e}")
        # 降级策略：使用已有标签
        return bookmark.tags[:3] if bookmark.tags else []


@log_execution_time
def build_keyword_index(force_rebuild: bool = False) -> Dict[str, List[Dict]]:
    """构建或更新关键词倒排索引"""
    # 读取现有索引
    existing_index = {}
    processed_urls = set()

    if KEYWORD_INDEX_PATH.exists() and not force_rebuild:
        with open(KEYWORD_INDEX_PATH, 'r', encoding='utf-8') as f:
            existing_index = json.load(f)
            # 提取已处理的URL
            for articles in existing_index.values():
                processed_urls.update([art['url'] for art in articles])
        logging.info(f"加载现有索引，已处理 {len(processed_urls)} 个URL")

    # 读取所有书签
    data_file = Path(f"{BOOKMARK_SUMMARY_REPO_DATA_DIR}/data.json")
    with open(data_file, 'r', encoding='utf-8') as f:
        bookmark_dicts = json.load(f)
        all_bookmarks = [SummarizedBookmark(**bm) for bm in bookmark_dicts]

    # 构建新索引
    keyword_index = defaultdict(list)

    # 恢复现有索引数据
    for keyword, articles in existing_index.items():
        keyword_index[keyword] = articles

    # 处理新书签
    new_count = 0
    for bookmark in all_bookmarks:
        if bookmark.url in processed_urls:
            continue

        keywords = extract_keywords_from_bookmark(bookmark)

        # 构建文章元数据
        from bookmark_process_changes import get_summary_file_path
        summary_path = str(get_summary_file_path(
            bookmark.title,
            bookmark.timestamp,
            bookmark.month,
            in_readme_md=True
        ))

        article_meta = {
            'url': bookmark.url,
            'title': bookmark.title,
            'timestamp': bookmark.timestamp,
            'month': bookmark.month,
            'summary_path': summary_path
        }

        # 添加到倒排索引
        for keyword in keywords:
            keyword_index[keyword].append(article_meta)

        new_count += 1

        # 定期保存索引（防止中断丢失）
        if new_count % INDEX_SAVE_INTERVAL == 0:
            _save_keyword_index(dict(keyword_index))
            logging.info(f"已处理 {new_count} 个新书签，保存中间结果")

    # 最终保存
    final_index = dict(keyword_index)
    _save_keyword_index(final_index)
    logging.info(f"索引构建完成，共处理 {new_count} 个新书签，总关键词数: {len(final_index)}")

    return final_index


def _save_keyword_index(index: Dict[str, List[Dict]]) -> None:
    """保存关键词索引到文件"""
    KEYWORD_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(KEYWORD_INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def load_keyword_index() -> Dict[str, List[Dict]]:
    """加载关键词索引"""
    if not KEYWORD_INDEX_PATH.exists():
        logging.warning("关键词索引不存在，请先运行 build_keyword_index()")
        return {}

    with open(KEYWORD_INDEX_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


@log_execution_time
def get_high_frequency_keywords(min_count: int = MIN_KEYWORD_FREQUENCY) -> List[Tuple[str, int]]:
    """获取高频关键词列表"""
    index = load_keyword_index()

    # 统计频次并过滤
    keyword_counts = [(kw, len(articles)) for kw, articles in index.items() if len(articles) >= min_count]

    # 按频次降序排序
    keyword_counts.sort(key=lambda x: x[1], reverse=True)

    logging.info(f"找到 {len(keyword_counts)} 个高频关键词（≥{min_count}篇）")
    return keyword_counts


def get_articles_by_keyword(keyword: str) -> List[KeywordArticle]:
    """获取指定关键词的所有文章"""
    index = load_keyword_index()
    articles = index.get(keyword, [])
    return [KeywordArticle(**art) for art in articles]


@log_execution_time
def load_article_summary(article: KeywordArticle) -> str:
    """加载文章的详细摘要内容"""
    from urllib.parse import unquote
    summary_path = Path(unquote(article.summary_path))

    if not summary_path.exists():
        logging.warning(f"摘要文件不存在: {summary_path}")
        return f"[文章: {article.title}] - 摘要文件缺失"

    with open(summary_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return content


def load_all_summaries(articles: List[KeywordArticle]) -> str:
    """加载所有文章摘要并格式化为统一字符串"""
    summaries = []
    for idx, article in enumerate(articles, 1):
        summary = load_article_summary(article)
        date_str = datetime.fromtimestamp(article.timestamp).strftime('%Y-%m-%d')
        summaries.append(f"### 文章{idx}: {article.title} ({date_str})\n{summary}\n")
    return "\n---\n".join(summaries)


@log_execution_time
def analyze_keyword_theme(keyword: str, articles: List[KeywordArticle]) -> str:
    """深度分析关键词主题"""
    combined_summaries = load_all_summaries(articles)

    prompt = f"""请对以下 {len(articles)} 篇关于「{keyword}」的文章进行深度主题分析。

要求：
1. 分析主题的演变趋势（如果有时间跨度）
2. 提炼核心观点和技术要点
3. 总结关键数据和案例支撑
4. 使用markdown列表格式，结构清晰

文章摘要合集：
{combined_summaries}

输出结构：
## 主题演变
...

## 核心观点汇总
...

## 技术要点
...
"""

    analysis = call_openai_api(prompt, "")
    return analysis


@log_execution_time
def compare_articles(keyword: str, articles: List[KeywordArticle]) -> str:
    """对比分析多篇文章"""
    combined_summaries = load_all_summaries(articles)

    prompt = f"""请对以下 {len(articles)} 篇关于「{keyword}」的文章进行对比分析。

要求：
1. 识别文章之间的共同观点
2. 对比不同文章的差异化视角
3. 分析文章的互补性（如理论vs实践、入门vs进阶）
4. 建议阅读顺序
5. 使用markdown列表格式

文章摘要合集：
{combined_summaries}

输出结构：
## 共同观点
...

## 差异化视角
...

## 互补性总结
...

## 推荐阅读顺序
...
"""

    comparison = call_openai_api(prompt, "")
    return comparison


@log_execution_time
def generate_keyword_report(keyword: str, articles: List[KeywordArticle]) -> None:
    """生成关键词的独立分析报告"""
    logging.info(f"开始生成关键词分析报告: {keyword} ({len(articles)}篇文章)")

    # 确保目录存在
    KEYWORD_ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)

    # 元数据
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamps = [art.timestamp for art in articles]
    date_range = f"{datetime.fromtimestamp(min(timestamps)).strftime('%Y-%m-%d')} ~ {datetime.fromtimestamp(max(timestamps)).strftime('%Y-%m-%d')}"

    # 文章列表
    article_list = []
    for idx, article in enumerate(articles, 1):
        date_str = datetime.fromtimestamp(article.timestamp).strftime('%Y-%m-%d')
        article_list.append(f"{idx}. [{article.title}]({article.summary_path}) - {date_str}")
    article_list_str = "\n".join(article_list)

    # 深度分析
    theme_analysis = analyze_keyword_theme(keyword, articles)

    # 对比分析
    comparison_analysis = compare_articles(keyword, articles)

    # 拼接完整报告
    report = f"""# {keyword} - 主题分析报告

## 元数据
- **分析时间**: {current_time}
- **相关文章数**: {len(articles)}篇
- **时间跨度**: {date_range}

## 文章列表
{article_list_str}

## 深度分析
{theme_analysis}

## 对比分析
{comparison_analysis}
"""

    # 保存报告
    from bookmark_process_changes import slugify
    report_path = KEYWORD_ANALYSIS_DIR / f"{slugify(keyword)}.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    logging.info(f"报告生成完成: {report_path}")


@log_execution_time
def build_analysis_summary() -> None:
    """生成关键词分析索引文件"""
    if not KEYWORD_ANALYSIS_DIR.exists():
        logging.warning("分析报告目录不存在")
        return

    # 扫描所有报告文件
    report_files = list(KEYWORD_ANALYSIS_DIR.glob("*.md"))

    if not report_files:
        logging.warning("未找到任何分析报告")
        return

    # 读取索引统计信息
    index = load_keyword_index()
    report_entries = []

    for report_file in sorted(report_files):
        # 从文件名反推关键词（需要处理slugify后的名称）
        keyword_slug = report_file.stem

        # 匹配原始关键词
        matched_keyword = None
        max_count = 0
        for kw, articles in index.items():
            from bookmark_process_changes import slugify
            if slugify(kw) == keyword_slug and len(articles) > max_count:
                matched_keyword = kw
                max_count = len(articles)

        if matched_keyword:
            report_entries.append((matched_keyword, max_count, report_file.name))

    # 按文章数量排序
    report_entries.sort(key=lambda x: x[1], reverse=True)

    # 生成索引内容
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    summary_lines = [
        "# 关键词分析报告索引\n",
        f"> 最后更新：{current_time}\n",
        f"> 共分析 {len(report_entries)} 个关键词\n\n",
        "## 高频关键词（按文章数量排序）\n\n"
    ]

    for keyword, count, filename in report_entries:
        summary_lines.append(f"- [{keyword}](data/keyword_analysis/{filename}) - {count}篇文章\n")

    # 保存索引文件
    with open(KEYWORD_ANALYSIS_SUMMARY, 'w', encoding='utf-8') as f:
        f.writelines(summary_lines)

    logging.info(f"索引文件已生成: {KEYWORD_ANALYSIS_SUMMARY}")


@log_execution_time
def process_keyword_analysis(force_rebuild: bool = False, min_frequency: int = MIN_KEYWORD_FREQUENCY) -> None:
    """主流程：执行完整的关键词分析"""
    logging.info("=" * 50)
    logging.info("开始关键词分析流程")
    logging.info("=" * 50)

    # 步骤1：构建/更新关键词索引
    logging.info("[1/4] 构建关键词索引...")
    build_keyword_index(force_rebuild=force_rebuild)

    # 步骤2：获取高频关键词
    logging.info("[2/4] 获取高频关键词...")
    high_freq_keywords = get_high_frequency_keywords(min_count=min_frequency)

    if not high_freq_keywords:
        logging.warning(f"未找到频次≥{min_frequency}的关键词，流程结束")
        return

    logging.info(f"找到 {len(high_freq_keywords)} 个高频关键词")

    # 步骤3：生成分析报告
    logging.info("[3/4] 生成关键词分析报告...")
    for idx, (keyword, count) in enumerate(high_freq_keywords, 1):
        logging.info(f"处理关键词 [{idx}/{len(high_freq_keywords)}]: {keyword} ({count}篇)")
        articles = get_articles_by_keyword(keyword)
        generate_keyword_report(keyword, articles)

    # 步骤4：生成索引文件
    logging.info("[4/4] 生成分析索引...")
    build_analysis_summary()

    logging.info("=" * 50)
    logging.info("关键词分析流程完成！")
    logging.info("=" * 50)


if __name__ == "__main__":
    # 测试运行
    process_keyword_analysis(force_rebuild=False, min_frequency=3)
