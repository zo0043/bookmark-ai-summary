import os
from typing import List
from pathlib import Path

BOOKMARK_SUMMARY_REPO_TAG_DIR: str = (
    "bookmark-ai-summary/data/tags"
)
BOOKMARK_SUMMARY_REPO_NAME: str = "bookmark-ai-summary"

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
