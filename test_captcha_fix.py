#!/usr/bin/env python3
"""
测试CAPTCHA跳过功能的脚本
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from bookmark_ai_summary.headless_content_extractor import (
    HeadlessContentExtractor,
    ExtractionResult,
    create_stealth_config
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

async def test_captcha_bypass():
    """测试CAPTCHA跳过功能"""

    # 测试URL - 选择一些可能有验证问题的网站
    test_urls = [
        "https://httpbin.org/user-agent",  # 简单测试
        "https://bot.sannysoft.com/",      # 检测自动化工具
        "https://example.com",             # 基础网站
    ]

    # 创建配置
    config = create_stealth_config("medium", headless=True)

    # 创建提取器
    extractor = HeadlessContentExtractor(config)

    results = []

    for i, url in enumerate(test_urls, 1):
        logger.info(f"\n{'='*50}")
        logger.info(f"测试 {i}/{len(test_urls)}: {url}")
        logger.info(f"{'='*50}")

        try:
            result = await extractor.extract_content(url)
            results.append(result)

            # 输出结果
            print(f"URL: {result.url}")
            print(f"成功: {result.success}")
            print(f"方法: {result.method_used}")
            print(f"内容长度: {len(result.content)} 字符")
            print(f"耗时: {result.execution_time:.2f}秒")

            if result.error_message:
                print(f"错误: {result.error_message}")

            if result.success and len(result.content) > 50:
                print(f"内容预览: {result.content[:200]}...")

        except Exception as e:
            logger.error(f"测试 {url} 时发生异常: {str(e)}")
            results.append(ExtractionResult(
                url=url,
                content="",
                method_used="headless_browser",
                success=False,
                error_message=str(e)
            ))

    # 生成报告
    print(f"\n{'='*50}")
    print("测试报告")
    print(f"{'='*50}")

    success_count = sum(1 for r in results if r.success)
    total_count = len(results)

    print(f"总测试数: {total_count}")
    print(f"成功数: {success_count}")
    print(f"成功率: {success_count/total_count*100:.1f}%")

    print("\n详细结果:")
    for i, result in enumerate(results, 1):
        status = "✓" if result.success else "✗"
        print(f"{i}. {status} {result.url} - {len(result.content)} 字符")
        if result.error_message:
            print(f"   错误: {result.error_message}")

    return results

async def test_jina_vs_headless():
    """比较Jina Reader和无头浏览器的效果"""

    test_url = "https://httpbin.org/json"

    logger.info(f"测试URL: {test_url}")

    # 测试Jina Reader
    try:
        import requests
        jina_url = f"https://r.jina.ai/{test_url}"
        response = requests.get(jina_url, timeout=10)

        if response.status_code == 200:
            jina_content = response.text
            print(f"✓ Jina Reader 成功: {len(jina_content)} 字符")
        else:
            print(f"✗ Jina Reader 失败: HTTP {response.status_code}")
            jina_content = ""
    except Exception as e:
        print(f"✗ Jina Reader 异常: {str(e)}")
        jina_content = ""

    # 测试无头浏览器
    try:
        config = create_stealth_config("low", headless=True)  # 使用低级别以便快速测试
        extractor = HeadlessContentExtractor(config)
        result = await extractor.extract_content(test_url)

        if result.success:
            print(f"✓ 无头浏览器成功: {len(result.content)} 字符")
        else:
            print(f"✗ 无头浏览器失败: {result.error_message}")
    except Exception as e:
        print(f"✗ 无头浏览器异常: {str(e)}")

    return jina_content, result if 'result' in locals() else None

if __name__ == "__main__":
    print("CAPTCHA跳过功能测试")
    print("=" * 50)

    # 检查环境
    print(f"USE_HEADLESS_BROWSER: {os.environ.get('USE_HEADLESS_BROWSER', 'Not set')}")
    print(f"OPENAI_API_KEY configured: {'Yes' if os.environ.get('OPENAI_API_KEY') else 'No'}")

    # 运行测试
    try:
        print("\n1. 基础CAPTCHA跳过测试")
        asyncio.run(test_captcha_bypass())

        print("\n2. Jina Reader vs 无头浏览器对比测试")
        asyncio.run(test_jina_vs_headless())

    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        logger.error(f"测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()