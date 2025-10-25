#!/usr/bin/env python3
"""
测试脚本：验证改进的 slugify 函数
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from bookmark_ai_summary.bookmark_process_changes import (
    MAX_FILENAME_LENGTH, slugify
)

def test_slugify_function():
    """测试 slugify 函数的各种情况"""

    test_cases = [
        # 短文件名（不应截断）
        {
            "input": "简单标题",
            "expected_max_length": 50,
            "description": "短文件名不应截断"
        },

        # 中等长度文件名
        {
            "input": "这是一个中等长度的文件标题，用来测试 slugify 函数的行为",
            "expected_max_length": MAX_FILENAME_LENGTH,
            "description": "中等长度文件名"
        },

        # 超长文件名（实际案例）
        {
            "input": "【网站自荐】投资策略模拟器---通过直观可视化界面和详细数据分析，让用户深入了解各种投资策略优劣，从而做出更明智投资决策-·-issue-#5288-·-ruanyf-weekly",
            "expected_max_length": MAX_FILENAME_LENGTH,
            "description": "超长文件名测试"
        },

        # 包含特殊字符
        {
            "input": "包含/特殊\\字符:*的文件?标题",
            "expected_max_length": MAX_FILENAME_LENGTH,
            "description": "特殊字符清理测试"
        },

        # 英文标题
        {
            "input": "A Very Long English Title with Many Words and Special Characters that Should Be Truncated Properly",
            "expected_max_length": MAX_FILENAME_LENGTH,
            "description": "英文长标题测试"
        },

        # 中英混合
        {
            "input": "中英文Mixed标题with多种Characters和Very Long内容that需要智能截断处理",
            "expected_max_length": MAX_FILENAME_LENGTH,
            "description": "中英混合标题测试"
        }
    ]

    print(f"文件名长度限制: {MAX_FILENAME_LENGTH} 字符")
    print("=" * 60)

    all_passed = True

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {test_case['description']}")
        print(f"输入: {test_case['input'][:50]}{'...' if len(test_case['input']) > 50 else ''}")

        result = slugify(test_case['input'])

        print(f"输出: {result}")
        print(f"长度: {len(result)} 字符")

        # 验证长度限制
        if len(result) <= test_case['expected_max_length']:
            print("✓ 长度检查通过")
        else:
            print(f"✗ 长度检查失败: {len(result)} > {test_case['expected_max_length']}")
            all_passed = False

        # 验证不包含非法字符
        illegal_chars = '/\\:*?"<>|'
        has_illegal = any(char in result for char in illegal_chars)
        if not has_illegal:
            print("✓ 非法字符检查通过")
        else:
            print(f"✗ 非法字符检查失败: 包含非法字符")
            all_passed = False

        # 验证唯一性哈希存在（对于被截断的文件）
        if len(test_case['input']) > MAX_FILENAME_LENGTH:
            if '_' in result and result.split('_')[-1].isalnum():
                print("✓ 哈希后缀检查通过")
            else:
                print("✗ 哈希后缀检查失败: 缺少哈希后缀")
                all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("✓ 所有测试通过!")
        return True
    else:
        print("✗ 部分测试失败")
        return False

def test_edge_cases():
    """测试边界情况"""

    print("\n边界情况测试:")
    print("-" * 30)

    edge_cases = [
        ("", "空字符串"),
        (" ", "空白字符"),
        ("---", "仅分隔符"),
        ("a" * 200, "超长单字符"),
        ("测试" * 50, "超长中文字符")
    ]

    for input_str, description in edge_cases:
        try:
            result = slugify(input_str)
            print(f"{description}: '{input_str[:20]}...' -> '{result}' (长度: {len(result)})")
        except Exception as e:
            print(f"{description}: 异常 - {e}")

def test_uniqueness():
    """测试唯一性保证"""

    print("\n唯一性测试:")
    print("-" * 30)

    # 生成多个相似的标题
    base_title = "这是一个很长很长的标题用来测试哈希唯一性"
    titles = [
        base_title + "版本一",
        base_title + "版本二",
        base_title + "版本三",
        base_title + "最终版本"
    ]

    results = [slugify(title) for title in titles]
    unique_results = set(results)

    print(f"输入标题数: {len(titles)}")
    print(f"生成结果数: {len(unique_results)}")

    if len(results) == len(unique_results):
        print("✓ 唯一性检查通过: 所有结果都不同")
        return True
    else:
        print("✗ 唯一性检查失败: 存在重复结果")

        # 显示重复项
        for i, result in enumerate(results):
            print(f"  {i+1}. {result}")
        return False

def main():
    """主测试函数"""

    print("开始测试改进的 slugify 函数...")

    # 基本功能测试
    basic_passed = test_slugify_function()

    # 边界情况测试
    test_edge_cases()

    # 唯一性测试
    uniqueness_passed = test_uniqueness()

    print("\n" + "=" * 60)
    print("测试总结:")
    print(f"基本功能: {'✓ 通过' if basic_passed else '✗ 失败'}")
    print(f"唯一性: {'✓ 通过' if uniqueness_passed else '✗ 失败'}")

    overall_passed = basic_passed and uniqueness_passed

    if overall_passed:
        print("\n🎉 所有测试通过! slugify 函数工作正常。")
        return True
    else:
        print("\n❌ 部分测试失败，请检查实现。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)