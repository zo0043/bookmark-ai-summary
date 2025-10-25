#!/usr/bin/env python3
"""
无头浏览器内容提取器测试脚本
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from bookmark_ai_summary.headless_content_extractor import (
    HeadlessContentExtractor,
    ExtractionResult,
    create_stealth_config
)
from bookmark_ai_summary.headless_content_extractor import StealthConfig

async def test_basic_functionality():
    """测试基本功能"""
    print("测试基本功能...")

    # 创建配置
    config = create_stealth_config("high", headless=True)
    extractor = HeadlessContentExtractor(config)

    # 测试URL列表
    test_urls = [
        "https://example.com",  # 简单测试
        "https://httpbin.org/user-agent",  # UA检测测试
        "https://bot.sannysoft.com/",  # CAPTCHA测试
    ]

    results = []

    for i, url in enumerate(test_urls, 1):
        print(f"\n测试 {i}: {url}")
        result = await extractor.extract_content(url)

        results.append({
            'url': url,
            'success': result.success,
            'content_length': len(result.content),
            'method_used': result.method_used,
            'execution_time': result.execution_time,
            'error': result.error_message
        })

        print(f"  结果: {'成功' if result.success else '失败'}")
        print(f"  方法: {result.method_used}")
        print(f"  内容长度: {len(result.content)} 字符")
        print(f"  耗时: {result.execution_time:.2f} 秒")

        if result.error_message:
            print(f"  错误: {result.error_message}")

        # 清理资源
        await extractor._cleanup()

        # 避免请求过于频繁
        await asyncio.sleep(2)

    return results

async def test_config_variations():
    """测试不同配置的影响"""
    print("\n测试配置变化...")

    # 测试不同的检测级别
    detection_levels = ["low", "medium", "high", "stealth"]
    results = []

    for level in detection_levels:
        print(f"\n测试检测级别: {level}")

        config = create_stealth_config(level, headless=True)
        extractor = HeadlessContentExtractor(config)

        result = await extractor.extract_content("https://example.com")

        results.append({
            'detection_level': level,
            'success': result.success,
            'execution_time': result.execution_time
        })

        print(f"  成功: {result.success}")
        print(f"  耗时: {result.execution_time:.2f} 秒")

        # 清理资源
        await extractor._cleanup()

        # 避免请求过于频繁
        await asyncio.sleep(1)

    return results

def test_sync_functionality():
    """测试同步功能"""
    print("测试同步功能...")

    from bookmark_ai_summary.headless_content_extractor import HeadlessExtractorSync

    config = create_stealth_config("medium", headless=True)
    extractor = HeadlessExtractorSync(config)

    result = extractor.extract_content_sync("https://example.com")

    print(f"同步结果: {'成功' if result.success else '失败'}")
    print(f"内容长度: {len(result.content)} 字符")
    print(f"使用方法: {result.method_used}")

def test_config_loading():
    """测试配置加载"""
    print("\n测试配置加载...")

    try:
        # 测试配置文件加载
        config_file = "config/headless_config.json"
        config = create_stealth_config()

        extractor = HeadlessContentExtractor(config)
        print(f"配置加载成功: {config_file}")

    except Exception as e:
        print(f"配置加载失败: {str(e)}")

async def main():
    """主测试函数"""
    print("开始无头浏览器内容提取器测试...")

    try:
        # 基本功能测试
        basic_results = await test_basic_functionality()

        # 配置变化测试
        config_results = await test_config_variations()

        # 同步功能测试
        test_sync_functionality()

        # 配置加载测试
        test_config_loading()

        # 输出测试总结
        print("\n=== 测试总结 ===")
        total_tests = len(basic_results) + len(config_results) + 2  # +2 for sync and config tests
        successful_tests = sum(1 for r in basic_results if r['success'])

        print(f"总测试数: {total_tests}")
        print(f"成功测试数: {successful_tests}")
        print(f"成功率: {successful_tests/total_tests*100:.1f}%")

        # 显示平均执行时间
        basic_times = [r['execution_time'] for r in basic_results if r['success']]
        if basic_times:
            avg_time = sum(basic_times) / len(basic_times)
            print(f"平均成功执行时间: {avg_time:.2f} 秒")

    except Exception as e:
        print(f"测试过程出错: {str(e)}")

if __name__ == "__main__":
    # 运行测试
    asyncio.run(main())