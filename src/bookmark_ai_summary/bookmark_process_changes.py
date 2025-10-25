import asyncio
import hashlib
import json
import logging
import os
import re
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import List, Optional, Union
from urllib.parse import quote

import requests
from waybackpy import WaybackMachineSaveAPI
# 尝试导入标签处理模块
try:
    from .process_tag_bookmark import deal_tags_chain,process_tag_summary,process_weekly_articles
except ImportError:
    try:
        from process_tag_bookmark import deal_tags_chain,process_tag_summary,process_weekly_articles
    except ImportError:
        logging.warning("标签处理模块不可用")
        deal_tags_chain = None
        process_tag_summary = None
        process_weekly_articles = None

# 尝试导入无头浏览器模块（可选依赖）
try:
    from .headless_content_extractor import (
        HeadlessContentExtractor,
        ExtractionResult,
        StealthConfig,
        create_stealth_config
    )
    HEADLESS_AVAILABLE = True
except ImportError:
    try:
        from headless_content_extractor import (
            HeadlessContentExtractor,
            ExtractionResult,
            StealthConfig,
            create_stealth_config
        )
        HEADLESS_AVAILABLE = True
    except ImportError:
        HEADLESS_AVAILABLE = False
        logging.warning("无头浏览器模块不可用，将仅使用Jina Reader")

# -- 配置 --
BOOKMARK_COLLECTION_REPO_NAME: str = (
    "bookmark-collection"
)
BOOKMARK_SUMMARY_REPO_NAME: str = "bookmark-ai-summary"
BOOKMARK_SUMMARY_REPO_DATA_DIR: str = (
    "bookmark-ai-summary/data"
)

# -- 文件名长度配置 --
MAX_FILENAME_LENGTH = 80          # 最大文件名长度
HASH_LENGTH = 8                  # 哈希后缀长度
TRUNCATE_PREFIX_LENGTH = 50      # 保留前缀长度
TRUNCATE_SUFFIX_LENGTH = 20      # 保留后缀长度
SEPARATOR = "..."                # 截断分隔符

# 配置验证
if not (20 <= MAX_FILENAME_LENGTH <= 255):
    raise ValueError(f"MAX_FILENAME_LENGTH ({MAX_FILENAME_LENGTH}) 必须在 20-255 之间")
if not (4 <= HASH_LENGTH <= 32):
    raise ValueError(f"HASH_LENGTH ({HASH_LENGTH}) 必须在 4-32 之间")
if TRUNCATE_PREFIX_LENGTH + TRUNCATE_SUFFIX_LENGTH >= MAX_FILENAME_LENGTH - len(SEPARATOR) - HASH_LENGTH:
    import warnings
    warnings.warn("截断长度配置较大，建议调整以确保足够的文件名空间", UserWarning)

# 性能优化：预编译正则表达式
_INVALID_FS_CHARS_PATTERN = re.compile(r"[/" + re.escape('/\\:*?"<>|') + r"\s]+")
_COMPILED_HASH_CACHE = {}  # 简单的LRU缓存

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# 配置无头浏览器环境变量
USE_HEADLESS_BROWSER = os.environ.get('USE_HEADLESS_BROWSER', 'false').lower() == 'true'


def log_execution_time(func):
    """记录函数执行时间的装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"进入函数 {func.__name__}")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"离开函数 {func.__name__} - 耗时: {elapsed_time:.4f} 秒")
        return result

    return wrapper


@dataclass
class SummarizedBookmark:
    """已摘要的书签数据类"""

    month: str  # yyyyMM
    title: str
    url: str
    timestamp: int  # unix timestamp
    tags: List[str]


CURRENT_MONTH: str = datetime.now().strftime("%Y%m")
CURRENT_DATE: str = datetime.now().strftime("%Y-%m-%d")
CURRENT_DATE_AND_TIME: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@log_execution_time
def submit_to_wayback_machine(url: str):
    """提交URL到Wayback Machine存档"""
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    try:
        save_api = WaybackMachineSaveAPI(url, user_agent, 2)
        wayback_url = save_api.save()
        logging.info(f"Wayback已保存: {wayback_url}")
    except Exception as e:
        # 非关键路径，容忍失败
        logging.warning(f"提交到Wayback Machine失败，跳过，url={url}")
        logging.exception(e)


@log_execution_time
def get_text_content(url: str) -> str:
    logging.info(f"get_text_content: {url}")
    """获取URL的文本内容"""

    # 使用新的内容获取方法
    try:
        # 在同步环境中，需要运行事件循环
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果已经在事件循环中，直接使用
                return loop.run_until_complete(
                    get_text_content_with_headless_fallback(url, use_headless=USE_HEADLESS_BROWSER)
                )
            else:
                # 创建新的事件循环
                return asyncio.run(get_text_content_with_headless_fallback(url, use_headless=USE_HEADLESS_BROWSER))
        except Exception as e:
            logging.error(f"异步内容获取失败: {str(e)}，使用同步Jina Reader")
            # 回退到原始Jina Reader
            return _fallback_to_jina_reader(url)
    except Exception as fallback_e:
        logging.error(f"所有方法都失败: {str(fallback_e)}")
        return ""


@log_execution_time
def call_openai_api(prompt: str, content: str) -> str:
    """调用OpenAI API生成摘要"""
    model: str = os.environ.get("OPENAI_API_MODEL", "gpt-4")
    headers: dict = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "Content-Type": "application/json",
    }
    data: dict = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": content},
        ],
    }
    api_endpoint: str = os.environ.get(
        "OPENAI_API_ENDPOINT", "https://api.openai.com/v1/chat/completions"
    )
    # logging.info(f"调用OpenAI API，数据: {data}")
    logging.info(f"调用OpenAI API，请求头: {headers}")
    logging.info(f"调用OpenAI API，端点: {api_endpoint}")
    response: requests.Response = requests.post(
        api_endpoint, headers=headers, data=json.dumps(data)
    )
    logging.info(f"OpenAI API响应: {response.json()}")
    return response.json()["choices"][0]["message"]["content"]


@log_execution_time
def summarize_text(text: str) -> str:
    """生成文本的详细摘要"""
    prompt: str = """
请用markdown列表格式**详细**总结我发送给你的文本。充分合理使用缩进和子列表，如果有需要可以使用多层子列表，或是在子列表中包含多个条目（3个或以上）。在每个总结项开头，用简短的词语描述该项。忽略和文章主体无关的内容（如广告）。无论原文语言为何，总是使用中文进行总结。

示例如下：

1. **Trello简介**：Trello是Fog Creek Software推出的100%基于云端的团队协作工具，自发布以来获得了积极的反馈和强劲的用户增长。

2. **开发模式转变**：Trello的开发标志着Fog Creek转向完全的云服务，不再提供安装版软件，开发过程中未使用Visual Basic，体现了开发流程的现代化。

3. **产品定位**：Trello是一款横跨多行业的产品，与之前主要针对软件开发者的垂直产品不同，它适用于各行各业的用户。

4. **横纵对比**：
   - **横向产品**：适用于广泛用户群体，如Word处理器和Web浏览器，难以定价过高，风险与回报并存。
   - **垂直产品**：针对特定行业，如牙医软件，用户定位明确，利润空间大，适合初创企业。

5. **Excel故事**：通过Excel的使用案例说明，大多数用户使用Excel实际上是作为列表工具，而非复杂的计算，引出"杀手级应用实际上是高级数据结构"的观点。

6. **Trello的核心**：Trello是一个高度灵活的数据结构应用，不仅限于敏捷开发的Kanban板，适用于规划婚礼、管理招聘流程等多种场景。

7. **产品特性**：
   - **持续交付**：新功能不断推出，无重大或次要版本的区别。
   - **快速迭代与修复**：测试不求面面俱到，但快速响应修复。
   - **公共透明**：开发过程公开，用户可参与反馈和投票。
   - **快速扩张策略**：目标是大规模用户增长，初期免费，优先消除采用障碍。
   - **API优先**：鼓励通过API和插件扩展功能，用户和第三方参与建设。

8. **技术选择**：采用前沿技术如MongoDB、WebSockets、CoffeeScript和Node.js，虽然有挑战，但有利于吸引顶尖程序员并为长期发展做准备。

9. **总结**：Trello及其开发策略体现了现代互联网产品的开发趋势，注重用户基础的快速扩展，技术的前沿性，以及通过社区参与和反馈来不断优化产品。
"""
    return call_openai_api(prompt, text)


@log_execution_time
def one_sentence_summary(text: str) -> str:
    """生成文本的一句话总结"""
    prompt: str = f"以下是对一篇长文的列表形式总结。请基于此输出对该文章的简短总结，长度不超过100个字。总是使用简体中文输出。"
    return call_openai_api(prompt, text)


def slugify(text: str) -> str:
    """将文本转换为适用于文件名或URL的"slug"格式，支持长度限制和智能截断"""
    if not text:
        return ""

    # 基础清理：使用预编译的正则表达式提高性能
    cleaned = _INVALID_FS_CHARS_PATTERN.sub("-", text.lower()).strip("-")

    # 如果长度在限制内，直接返回
    if len(cleaned) <= MAX_FILENAME_LENGTH:
        return cleaned

    # 使用缓存提高性能（适用于重复的输入）
    cache_key = (text, MAX_FILENAME_LENGTH, HASH_LENGTH, TRUNCATE_PREFIX_LENGTH, TRUNCATE_SUFFIX_LENGTH)
    if cache_key in _COMPILED_HASH_CACHE:
        return _COMPILED_HASH_CACHE[cache_key]

    # 生成原文本的哈希值确保唯一性
    hash_suffix = hashlib.md5(text.encode('utf-8')).hexdigest()[:HASH_LENGTH]

    # 计算可用长度（减去分隔符和哈希）
    available_length = MAX_FILENAME_LENGTH - len(SEPARATOR) - HASH_LENGTH

    # 智能截断：保留前缀和后缀
    prefix_length = min(TRUNCATE_PREFIX_LENGTH, available_length // 2)
    suffix_length = min(TRUNCATE_SUFFIX_LENGTH, available_length - prefix_length)

    # 构建截断后的文件名
    prefix = cleaned[:prefix_length]
    suffix = cleaned[-suffix_length:] if suffix_length > 0 else ""

    truncated_name = f"{prefix}{SEPARATOR}{suffix}_{hash_suffix}"

    # 确保最终长度不超过限制
    if len(truncated_name) > MAX_FILENAME_LENGTH:
        # 如果仍然过长，进一步缩短前缀
        excess = len(truncated_name) - MAX_FILENAME_LENGTH
        prefix = prefix[:-excess]
        truncated_name = f"{prefix}{SEPARATOR}{suffix}_{hash_suffix}"

    # 缓存结果（简单的FIFO缓存，限制大小）
    if len(_COMPILED_HASH_CACHE) < 1000:
        _COMPILED_HASH_CACHE[cache_key] = truncated_name

    return truncated_name


def get_summary_file_path(
    title: str, timestamp: int, month: Optional[str] = None, in_readme_md: bool = False
) -> Path:
    """根据给定的标题、时间戳和月份生成书签摘要文件的路径"""
    date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")

    # 使用改进的 slugify 函数，已包含长度限制
    slugified_title = slugify(title)
    summary_filename: str = f"{date_str}-{slugified_title}.md"

    if in_readme_md:
        if month is None:
            raise ValueError("在README.md中生成摘要时必须提供月份")
        root: Path = Path("data/", month)
        # 对于 README.md 中的链接，仍需要 URL 编码，但使用更短的编码
        summary_filename = f"{date_str}-{quote(slugified_title, safe='-_.~')}.md"
    else:
        if month is None:
            month = CURRENT_MONTH
        root: Path = Path(BOOKMARK_SUMMARY_REPO_DATA_DIR, month)

    summary_path: Path = Path(root, summary_filename)
    return summary_path


def get_text_content_path(title: str, in_summary_md: bool = False) -> Path:
    """构建并返回文本内容文件的路径"""
    text_content_filename: str = f"{CURRENT_DATE}-{slugify(title)}_raw.md"
    root: Path = Path(BOOKMARK_SUMMARY_REPO_DATA_DIR, CURRENT_MONTH)

    if in_summary_md:
        root = Path(".")

    text_content_path: Path = Path(root, text_content_filename)
    return text_content_path


def build_summary_file(title: str, url: str, summary: str, one_sentence: str) -> str:
    """构建一个摘要文件，包含文章的标题、链接、完整摘要及一句话总结"""
    return f"""# {title}
- URL: {url}
- Added At: {CURRENT_DATE_AND_TIME}
- [Link To Text]({get_text_content_path(title, in_summary_md=True)})

## TL;DR
{one_sentence}

## Summary
{summary}
"""


def build_summary_readme_md(summarized_bookmarks: List[SummarizedBookmark]) -> str:
    """生成一个摘要书签的README文件"""
    initial_prefix: str = """# Bookmark Summary 
读取 [bookmark-collection](https://github.com/zo0043/bookmark-collection) 中的书签，使用 jina reader 获取文本内容，然后使用 LLM 总结文本。详细实现请参见 bookmark_process_changes.py。需要和 bookmark-collection 中的 Github Action 一起使用。

- [tag list](tag_summary.md)

## Summarized Bookmarks
"""
    summary_list: str = ""
    sorted_summarized_bookmarks = sorted(
        summarized_bookmarks, key=lambda bookmark: bookmark.timestamp, reverse=True
    )

    for bookmark in sorted_summarized_bookmarks:
        summary_file_path = get_summary_file_path(
            title=bookmark.title,
            timestamp=bookmark.timestamp,
            month=bookmark.month,
            in_readme_md=True,
        )
        date_str = datetime.fromtimestamp(bookmark.timestamp).strftime("%Y-%m-%d")
        current_line = f"- ({date_str}) [{bookmark.title}]({summary_file_path})\n"
        summary_list += current_line
        if deal_tags_chain:
            deal_tags_chain(bookmark.tags, current_line)

    return initial_prefix + summary_list


@log_execution_time
def process_bookmark_file():
    """处理书签文件的主函数"""
    with open(f"{BOOKMARK_COLLECTION_REPO_NAME}/README.md", "r", encoding="utf-8") as f:
        bookmark_lines: List[str] = f.readlines()

    with open(
        f"{BOOKMARK_SUMMARY_REPO_DATA_DIR}/data.json", "r", encoding="utf-8"
    ) as f:
        summarized_bookmark_dicts = json.load(f)
        summarized_bookmarks = [
            SummarizedBookmark(**bookmark) for bookmark in summarized_bookmark_dicts
        ]

    summarized_urls = set([bookmark.url for bookmark in summarized_bookmarks])

    title: Optional[str] = None
    url: Optional[str] = None
    url_tags: List[str] = []
    for line in bookmark_lines:
        logging.info(f"processing line: {line}")
        pattern = r"- \[(.*?)\]\((.*?)\)(?: (#\w+))*"
        match: re.Match = re.search(pattern, line)
        if match and match.group(2) not in summarized_urls:
            title = match.group(1)
            url = match.group(2)
            url_tags = re.findall(r"#(\w+)", line)
            logging.info(f"found title: {title}, url: {url}, tags: {url_tags}")
            break

    if title and url:
        Path(f"{BOOKMARK_SUMMARY_REPO_DATA_DIR}/{CURRENT_MONTH}").mkdir(
            parents=True, exist_ok=True
        )

        # submit_to_wayback_machine(url)  # 提交书签到Wayback Machine存档
        text_content: str = get_text_content(url)
        summary: str = summarize_text(text_content)
        one_sentence: str = one_sentence_summary(summary)
        summary_file_content: str = build_summary_file(
            title, url, summary, one_sentence
        )
        timestamp = int(datetime.now().timestamp())

        with open(get_text_content_path(title), "w", encoding="utf-8") as f:
            f.write(text_content)

        with open(
            get_summary_file_path(title, timestamp=timestamp), "w", encoding="utf-8"
        ) as f:
            f.write(summary_file_content)

        summarized_bookmarks.append(
            SummarizedBookmark(
                month=CURRENT_MONTH,
                title=title,
                url=url,
                timestamp=timestamp,
                tags=url_tags,
            )
        )

        with open(
            f"{BOOKMARK_SUMMARY_REPO_NAME}/README.md", "w", encoding="utf-8"
        ) as f:
            f.write(build_summary_readme_md(summarized_bookmarks))

        with open(
            f"{BOOKMARK_SUMMARY_REPO_DATA_DIR}/data.json", "w", encoding="utf-8"
        ) as f:
            json.dump(
                [asdict(bookmark) for bookmark in summarized_bookmarks],
                f,
                indent=2,
                ensure_ascii=False,
            )


def main():
    process_bookmark_file()
    if process_tag_summary:
        process_tag_summary()
    # if process_weekly_articles:
    #     process_weekly_articles()

    # 关键词分析（可选，注释掉避免每次都执行）
    # from keyword_analyzer import process_keyword_analysis
    # process_keyword_analysis(force_rebuild=False, min_frequency=3)

async def get_text_content_with_headless_fallback(url: str, use_headless: bool = False) -> str:
    """
    带有无头浏览器备用方案的内容获取函数

    Args:
        url: 目标URL
        use_headless: 是否使用无头浏览器作为备用方案

    Returns:
        str: 提取的文本内容
    """
    if not use_headless or not HEADLESS_AVAILABLE:
        # 直接使用Jina Reader
        return _fallback_to_jina_reader(url)

    # 尝试Jina Reader，失败时使用无头浏览器
    try:
        logging.info(f"尝试使用Jina Reader: {url}")
        jina_content = _fallback_to_jina_reader(url)
        if jina_content and len(jina_content) > 100:
            logging.info(f"Jina Reader成功，内容长度: {len(jina_content)}")
            return jina_content
        else:
            logging.warning("Jina Reader内容过短，尝试无头浏览器")
    except Exception as e:
        logging.error(f"Jina Reader失败: {str(e)}")

    # 使用无头浏览器作为备用方案
    try:
        logging.info(f"使用无头浏览器: {url}")
        config = create_stealth_config("medium", headless=True)
        extractor = HeadlessContentExtractor(config)
        result = await extractor.extract_content(url)

        if result.success and result.content:
            logging.info(f"无头浏览器成功，内容长度: {len(result.content)}")
            return result.content
        else:
            logging.error(f"无头浏览器失败: {result.error_message or '未知错误'}")
            return ""
    except Exception as e:
        logging.error(f"无头浏览器异常: {str(e)}")
        return ""

def _fallback_to_jina_reader(url: str) -> str:
    """
    使用Jina Reader获取网页内容的回退方案

    Args:
        url: 目标URL

    Returns:
        str: 提取的文本内容
    """
    try:
        jina_url = f"https://r.jina.ai/{url}"
        logging.info(f"使用Jina Reader: {jina_url}")

        response = requests.get(jina_url, timeout=30)
        response.raise_for_status()

        content = response.text
        logging.info(f"Jina Reader成功，内容长度: {len(content)}")
        return content

    except requests.exceptions.RequestException as e:
        logging.error(f"Jina Reader请求失败: {str(e)}")
        return ""
    except Exception as e:
        logging.error(f"Jina Reader未知错误: {str(e)}")
        return ""

if __name__ == "__main__":
    main()
