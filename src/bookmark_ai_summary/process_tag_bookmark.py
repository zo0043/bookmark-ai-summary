import os
from typing import List, Dict
from pathlib import Path
import json

BOOKMARK_SUMMARY_REPO_TAG_DIR: str = (
    "bookmark-ai-summary/data/tags"
)
BOOKMARK_SUMMARY_REPO_NAME: str = "bookmark-ai-summary"
BOOKMARK_SUMMARY_REPO_DATA_DIR: str = "bookmark-ai-summary/data"

def load_tags_data(target_tag):
    tag_path: Path = Path(f"{BOOKMARK_SUMMARY_REPO_TAG_DIR}/{target_tag}.tag")
    if not tag_path.exists():
        return []
    with open(tag_path, "r", encoding="utf-8") as f:
        target_tag_lines = f.readlines()
        return target_tag_lines

def save_tags_data(target_tag, target_tag_lines, title_url):
    tag_path: Path = Path(f"{BOOKMARK_SUMMARY_REPO_TAG_DIR}/{target_tag}.tag")
    target_tag_lines.insert(0, title_url)
    target_tag_lines = list(set(target_tag_lines))
    target_tag_lines = sorted(target_tag_lines)
    with open(tag_path, "w", encoding="utf-8") as f:
        f.writelines(target_tag_lines)
    pass

def _deal_tags(tags: List[str], title_url: str, target_tag: str = "tool"):
    if target_tag in tags:
        print(f"found title_url: {title_url}, tags: {tags}")
        target_tag_lines = load_tags_data(target_tag)
        save_tags_data(target_tag, target_tag_lines, title_url)
    
    if target_tag == "*":
        for ct in tags:
            print(f"deal tag title_url: {title_url}, tags: {ct}")
            target_tag_lines = load_tags_data(ct)
            save_tags_data(ct, target_tag_lines, title_url)

def deal_tags_chain(tags: List[str], title_url: str):
    _deal_tags(tags, title_url, "tool")
    _deal_tags(tags, title_url, "系统设计")
    _deal_tags(tags, title_url, "*")

def process_tag_summary():
    tag_summary_path = Path(f"{BOOKMARK_SUMMARY_REPO_NAME}/tag_summary.md")
    
    # 获取所有 .tag 文件并排序
    tag_files = sorted([f for f in os.listdir(BOOKMARK_SUMMARY_REPO_TAG_DIR) if f.endswith('.tag')])
    
    with open(tag_summary_path, "w", encoding="utf-8") as summary_file:
        summary_file.write("# 标签摘要\n\n")
        
        for tag_file in tag_files:
            tag_name = tag_file[:-4]  # 移除 .tag 扩展名
            summary_file.write(f"## {tag_name}\n\n")
            
            tag_file_path = Path(BOOKMARK_SUMMARY_REPO_TAG_DIR) / tag_file
            with open(tag_file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                summary_file.write(content + "\n\n")

def load_data_json() -> Dict:
    """加载data.json文件"""
    data_file = Path(f"{BOOKMARK_SUMMARY_REPO_DATA_DIR}/data.json")
    if data_file.exists():
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def get_weekly_articles() -> List[Dict]:
    """获取标记为weekly的文章"""
    data = load_data_json()
    weekly_articles = []
    
    # 遍历所有文章
    for article in data.get('articles', []):
        if 'tags' in article and 'weekly' in article['tags']:
            # 读取文章内容
            content_file = Path(f"{BOOKMARK_SUMMARY_REPO_DATA_DIR}/{article['file_path']}")
            if content_file.exists():
                with open(content_file, 'r', encoding='utf-8') as f:
                    article['content'] = f.read()
                weekly_articles.append(article)
    
    return weekly_articles

def analyze_with_llm(article: Dict) -> Dict:
    """使用LLM分析文章内容"""
    # TODO: 实现LLM分析逻辑
    # 1. 提取文章主题
    # 2. 识别关键观点
    # 3. 提取数据支撑
    # 4. 生成结构化摘要
    return {
        'title': article.get('title', ''),
        'url': article.get('url', ''),
        'analysis': {
            'theme': '',  # 主题
            'key_points': [],  # 关键观点
            'data_support': [],  # 数据支撑
            'summary': ''  # 结构化摘要
        }
    }

def generate_weekly_report(articles: List[Dict]) -> str:
    """生成周报分析报告"""
    report = []
    report.append('# Weekly Articles Analysis Report\n')
    
    for article in articles:
        analysis = analyze_with_llm(article)
        report.append(f'## {analysis["title"]}\n')
        report.append(f'- URL: {analysis["url"]}\n')
        report.append('### Analysis\n')
        report.append(f'- Theme: {analysis["analysis"]["theme"]}\n')
        report.append('- Key Points:\n')
        for point in analysis['analysis']['key_points']:
            report.append(f'  * {point}\n')
        report.append('- Data Support:\n')
        for data in analysis['analysis']['data_support']:
            report.append(f'  * {data}\n')
        report.append(f'### Summary\n{analysis["analysis"]["summary"]}\n\n')
    
    return ''.join(report)

def process_weekly_articles():
    """处理weekly标签文章并生成分析报告"""
    weekly_articles = get_weekly_articles()
    if not weekly_articles:
        print("No weekly articles found.")
        return
    
    report = generate_weekly_report(weekly_articles)
    
    # 保存报告
    report_dir = Path(f"{BOOKMARK_SUMMARY_REPO_DATA_DIR}/weekly_reports")
    report_dir.mkdir(exist_ok=True)
    report_file = report_dir / 'weekly_analysis.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Weekly analysis report generated at {report_file}")
