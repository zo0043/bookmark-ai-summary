import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import unquote

import requests

from bookmark_process_changes import get_summary_file_path

# 常量定义
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
GITHUB_REF_NAME = os.getenv("GITHUB_REF_NAME", "main")
API_URL = "https://api.github.com"
BOOKMARK_SUMMARY_REPO_NAME = "."  # 当前目录


def extract_tldr(summary_file: Path) -> str:
    """
    从摘要文件中提取 TL;DR 部分。
    """
    if not summary_file.exists():
        raise FileNotFoundError(f"摘要文件未找到: {summary_file}")
    with summary_file.open("r", encoding="utf-8") as f:
        content = f.read()
    # 使用正则表达式提取 ## TL;DR 部分
    match = re.search(r"##\s+TL;DR\s+(.*?)\n##\s+", content, re.DOTALL)
    if not match:
        # 尝试匹配文件末尾
        match = re.search(r"##\s+TL;DR\s+(.*)", content, re.DOTALL)
        if not match:
            raise ValueError(f"在 {summary_file} 中未找到 TL;DR 部分")
    tldr = match.group(1).strip()
    # 将多余的空白字符替换为单个空格
    tldr = re.sub(r"\s+", " ", tldr)
    return tldr


def get_last_week_date_range():
    """
    获取上周的开始和结束日期范围。
    """
    today = datetime.utcnow().date()
    last_monday = today - timedelta(days=today.weekday() + 7)
    last_sunday = last_monday + timedelta(days=6)
    start_datetime = datetime.combine(last_monday, datetime.min.time())
    end_datetime = datetime.combine(last_sunday, datetime.max.time())
    return start_datetime, end_datetime


def get_release_entries(data, start_datetime, end_datetime):
    """
    从数据中获取符合条件的发布条目。
    """
    release_entries = []
    for entry in data:
        timestamp = entry.get("timestamp")
        if timestamp is None:
            continue
        entry_datetime = datetime.fromtimestamp(timestamp)
        if start_datetime <= entry_datetime <= end_datetime:
            month = entry.get("month")
            title = entry.get("title")
            url = entry.get("url")
            if not all([month, title, url]):
                continue
            summary_file = Path(
                unquote(
                    str(
                        get_summary_file_path(
                            title, timestamp, month=month, in_readme_md=True
                        )
                    )
                )
            )
            try:
                tldr = extract_tldr(summary_file)
            except (FileNotFoundError, ValueError) as e:
                print(f"处理 '{title}' 时出错: {e}")
                tldr = "没有可用的 TL;DR。"
            date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
            owner, repo = GITHUB_REPOSITORY.split("/")
            summary_path_str = str(summary_file).replace("\\", "/")
            raw_url = f"https://github.com/{owner}/{repo}/blob/{GITHUB_REF_NAME}/{summary_path_str}"
            release_entries.append(
                {"date": date_str, "title": title, "link": raw_url, "tldr": tldr}
            )
    return release_entries


def create_github_release(tag_name, release_name, release_body):
    """
    在 GitHub 上创建新的发布。
    """
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    # 检查标签是否已存在
    tags_url = f"{API_URL}/repos/{GITHUB_REPOSITORY}/git/refs/tags/{tag_name}"
    response = requests.get(tags_url, headers=headers)
    if response.status_code == 200:
        print(f"标签 '{tag_name}' 已存在,跳过发布。")
        return
    elif response.status_code != 404:
        raise ValueError(f"检查标签时出错: {response.status_code} {response.text}")

    # 获取默认分支的最新提交 SHA
    repo_url = f"{API_URL}/repos/{GITHUB_REPOSITORY}"
    repo_resp = requests.get(repo_url, headers=headers)
    repo_resp.raise_for_status()
    repo_info = repo_resp.json()
    default_branch = repo_info.get("default_branch", "main")
    branch_url = f"{API_URL}/repos/{GITHUB_REPOSITORY}/git/ref/heads/{default_branch}"
    branch_resp = requests.get(branch_url, headers=headers)
    branch_resp.raise_for_status()
    branch_info = branch_resp.json()
    commit_sha = branch_info["object"]["sha"]

    # 创建新的标签对象
    tag_object = {
        "tag": tag_name,
        "message": release_name,
        "object": commit_sha,
        "type": "commit",
        "tagger": {
            "name": "GitHub Actions",
            "email": "actions@github.com",
            "date": datetime.utcnow().isoformat() + "Z",
        },
    }
    tag_resp = requests.post(
        f"{API_URL}/repos/{GITHUB_REPOSITORY}/git/tags",
        headers=headers,
        json=tag_object,
    )
    tag_resp.raise_for_status()
    tag_info = tag_resp.json()
    tag_sha = tag_info["sha"]

    # 创建标签引用
    ref_object = {"ref": f"refs/tags/{tag_name}", "sha": tag_sha}
    ref_resp = requests.post(
        f"{API_URL}/repos/{GITHUB_REPOSITORY}/git/refs",
        headers=headers,
        json=ref_object,
    )
    ref_resp.raise_for_status()

    # 创建发布
    release_payload = {
        "tag_name": tag_name,
        "name": release_name,
        "body": release_body,
        "draft": False,
        "prerelease": False,
    }
    release_url = f"{API_URL}/repos/{GITHUB_REPOSITORY}/releases"
    release_resp = requests.post(release_url, headers=headers, json=release_payload)
    release_resp.raise_for_status()

    print(f"发布 '{release_name}' 创建成功。")


def main():
    if not GITHUB_TOKEN:
        raise EnvironmentError("环境变量 GITHUB_TOKEN 未设置")
    if not GITHUB_REPOSITORY:
        raise EnvironmentError("环境变量 GITHUB_REPOSITORY 未设置")

    # 获取上周的日期范围
    start_datetime, end_datetime = get_last_week_date_range()

    # 读取 data.json
    data_file = Path("data/data.json")
    if not data_file.exists():
        raise FileNotFoundError("未找到 data.json 文件")
    with data_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # 获取符合条件的发布条目
    release_entries = get_release_entries(data, start_datetime, end_datetime)

    if not release_entries:
        print("上周没有符合条件的条目,跳过发布。")
        return

    # 构建发布内容
    start_date_str = start_datetime.strftime("%Y-%m-%d")
    end_date_str = end_datetime.strftime("%Y-%m-%d")
    total = len(release_entries)
    release_body = (
        f"本周（{start_date_str} - {end_date_str}）共收藏了 {total} 篇文章。\n"
    )
    for idx, entry in enumerate(release_entries, start=1):
        release_body += f"{idx}. （{entry['date']}） [{entry['title']}]({entry['link']}) - {entry['tldr']}\n"

    print(release_body)

    # 创建 GitHub Release
    tag_name = f"weekly-{start_date_str}"
    release_name = f"Weekly Read Articles ({start_date_str} - {end_date_str})"
    create_github_release(tag_name, release_name, release_body)


if __name__ == "__main__":
    main()