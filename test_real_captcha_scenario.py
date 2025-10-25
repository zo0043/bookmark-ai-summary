#!/usr/bin/env python3
"""
模拟真实场景测试：测试一些可能被验证卡住的文章
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

async def test_problematic_articles():
    """测试一些可能被验证卡住的真实文章URL"""

    # 从现有书签中选择一些可能有问题的URL
    # 这些网站通常有更严格的反爬虫措施
    problematic_urls = [
        # 一些技术网站，可能有防护
        "https://www.juejin.cn/post/7424904499666501632",
        "https://mp.weixin.qq.com/s/StZeb__lyrZl_as_sQ8l6A",
        "https://xueqiu.com/8233733182/310036973",

        # 一些可能有Cloudflare保护的网站
        "https://github.com/ruanyf/weekly/issues/5288",
        "https://www.cnblogs.com/trunks2008/p/16706962.html",

        # 一些可能有验证的论坛/社区
        "https://linux.do/t/topic/408100",
        "https://www.zhihu.com/question/47220912",
    ]

    # 创建配置（使用高级别的隐形模式）
    config = create_stealth_config("high", headless=True)

    # 创建提取器
    extractor = HeadlessContentExtractor(config)

    results = []
    total_tests = len(problematic_urls)

    print(f"开始测试 {total_tests} 个可能有验证问题的URL...")
    print("=" * 80)

    for i, url in enumerate(problematic_urls, 1):
        print(f"\n[{i}/{total_tests}] 测试: {url}")
        print("-" * 60)

        try:
            result = await extractor.extract_content(url)
            results.append((url, result))

            # 输出结果
            status = "✓ 成功" if result.success else "✗ 失败"
            print(f"状态: {status}")
            print(f"内容长度: {len(result.content)} 字符")
            print(f"耗时: {result.execution_time:.2f}秒")

            if result.error_message:
                print(f"错误信息: {result.error_message}")

            if result.success and len(result.content) > 50:
                # 显示内容预览
                preview = result.content[:200].replace('\n', ' ').strip()
                print(f"内容预览: {preview}...")

                # 检查是否包含CAPTCHA相关的关键词
                content_lower = result.content.lower()
                captcha_indicators = ['captcha', '验证码', 'robot', 'cloudflare', 'ddos', 'protection']
                found_indicators = [word for word in captcha_indicators if word in content_lower]

                if found_indicators:
                    print(f"⚠️  检测到验证相关关键词: {found_indicators}")

        except Exception as e:
            logger.error(f"测试 {url} 时发生异常: {str(e)}")
            error_result = ExtractionResult(
                url=url,
                content="",
                method_used="headless_browser",
                success=False,
                error_message=str(e)
            )
            results.append((url, error_result))
            print(f"✗ 异常: {str(e)}")

        # 测试间隔，避免过于频繁的请求
        if i < total_tests:
            await asyncio.sleep(2)

    # 生成详细报告
    print(f"\n{'='*80}")
    print("详细测试报告")
    print(f"{'='*80}")

    success_count = sum(1 for _, r in results if r.success)
    total_count = len(results)

    print(f"总测试数: {total_count}")
    print(f"成功数: {success_count}")
    print(f"成功率: {success_count/total_count*100:.1f}%")

    print(f"\n详细结果:")
    for i, (url, result) in enumerate(results, 1):
        status = "✓" if result.success else "✗"
        content_len = len(result.content)
        time_taken = result.execution_time

        print(f"{i:2d}. {status} {content_len:5d}字符 {time_taken:6.2f}s {url}")

        if result.error_message:
            print(f"     错误: {result.error_message}")

    # 分析成功的模式
    successful_results = [(url, r) for url, r in results if r.success]
    if successful_results:
        print(f"\n✓ 成功案例 ({len(successful_results)} 个):")
        for url, result in successful_results:
            print(f"   - {url}")
            print(f"     内容长度: {len(result.content)} 字符")

    # 分析失败的模式
    failed_results = [(url, r) for url, r in results if not r.success]
    if failed_results:
        print(f"\n✗ 失败案例 ({len(failed_results)} 个):")
        for url, result in failed_results:
            print(f"   - {url}")
            print(f"     错误: {result.error_message}")

    return results

async def compare_with_jina_reader():
    """对比Jina Reader和无头浏览器的效果"""

    test_url = "https://www.juejin.cn/post/7424904499666501632"

    print(f"\n{'='*80}")
    print(f"对比测试: {test_url}")
    print(f"{'='*80}")

    # 测试Jina Reader
    print("\n1. 测试Jina Reader:")
    try:
        import requests
        jina_url = f"https://r.jina.ai/{test_url}"
        response = requests.get(jina_url, timeout=30)

        if response.status_code == 200:
            jina_content = response.text
            print(f"✓ Jina Reader 成功: {len(jina_content)} 字符")

            # 检查是否包含验证相关内容
            content_lower = jina_content.lower()
            if any(word in content_lower for word in ['captcha', '验证码', 'robot', 'cloudflare']):
                print("⚠️  内容中可能包含验证相关页面")
            else:
                print("✓ 内容正常，无验证页面")

        else:
            print(f"✗ Jina Reader 失败: HTTP {response.status_code}")
            jina_content = ""

    except Exception as e:
        print(f"✗ Jina Reader 异常: {str(e)}")
        jina_content = ""

    # 测试无头浏览器
    print("\n2. 测试无头浏览器:")
    try:
        config = create_stealth_config("high", headless=True)
        extractor = HeadlessContentExtractor(config)
        result = await extractor.extract_content(test_url)

        if result.success:
            print(f"✓ 无头浏览器成功: {len(result.content)} 字符")
            print(f"   耗时: {result.execution_time:.2f}秒")

            # 检查内容质量
            if len(result.content) > 500:
                print("✓ 内容质量良好")
            elif len(result.content) > 100:
                print("⚠️  内容较短，可能不完整")
            else:
                print("✗ 内容过短，可能失败")

        else:
            print(f"✗ 无头浏览器失败: {result.error_message}")

    except Exception as e:
        print(f"✗ 无头浏览器异常: {str(e)}")

    # 对比结果
    print("\n3. 对比结果:")
    if jina_content and result.success:
        jina_len = len(jina_content)
        headless_len = len(result.content)

        print(f"   Jina Reader:    {jina_len:5d} 字符")
        print(f"   无头浏览器:    {headless_len:5d} 字符")

        if headless_len > jina_len:
            print("   → 无头浏览器获得更多内容")
        elif headless_len == jina_len:
            print("   → 两种方法获得相似内容")
        else:
            print("   → Jina Reader获得更多内容")

    elif jina_content and not result.success:
        print("   → Jina Reader 成功，无头浏览器失败")
    elif not jina_content and result.success:
        print("   → Jina Reader 失败，无头浏览器成功")
    else:
        print("   → 两种方法都失败")

if __name__ == "__main__":
    print("真实场景CAPTCHA跳过测试")
    print("=" * 80)

    # 检查环境
    print(f"USE_HEADLESS_BROWSER: {os.environ.get('USE_HEADLESS_BROWSER', 'Not set')}")
    print(f"PLAYWRIGHT_BROWSERS_PATH: {os.environ.get('PLAYWRIGHT_BROWSERS_PATH', 'Default')}")

    # 运行测试
    try:
        print("\n正在运行真实场景测试...")
        asyncio.run(test_problematic_articles())

        print("\n正在运行对比测试...")
        asyncio.run(compare_with_jina_reader())

    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        logger.error(f"测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()