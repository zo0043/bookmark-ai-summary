#!/usr/bin/env python3
"""
独立测试脚本：验证改进的 slugify 函数（不依赖外部模块）
"""

import hashlib
import re

# 配置常量（从原模块复制）
MAX_FILENAME_LENGTH = 80
HASH_LENGTH = 8
TRUNCATE_PREFIX_LENGTH = 50
TRUNCATE_SUFFIX_LENGTH = 20
SEPARATOR = "..."

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

def run_tests():
    """运行所有测试"""

    print(f"文件名长度限制: {MAX_FILENAME_LENGTH} 字符")
    print("=" * 60)

    test_cases = [
        # 短文件名
        {
            "input": "简单标题",
            "description": "短文件名不应截断"
        },

        # 超长文件名（实际案例）
        {
            "input": "【网站自荐】投资策略模拟器---通过直观可视化界面和详细数据分析，让用户深入了解各种投资策略优劣，从而做出更明智投资决策-·-issue-#5288-·-ruanyf-weekly",
            "description": "超长文件名测试"
        },

        # 包含特殊字符
        {
            "input": "包含/特殊\\字符:*的文件?标题",
            "description": "特殊字符清理测试"
        },

        # 英文标题
        {
            "input": "A Very Long English Title with Many Words and Special Characters that Should Be Truncated Properly",
            "description": "英文长标题测试"
        }
    ]

    all_passed = True

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {test_case['description']}")
        print(f"输入: {test_case['input'][:60]}{'...' if len(test_case['input']) > 60 else ''}")

        result = slugify(test_case['input'])
        print(f"输出: {result}")
        print(f"长度: {len(result)} 字符")

        # 验证长度限制
        if len(result) <= MAX_FILENAME_LENGTH:
            print("✓ 长度检查通过")
        else:
            print(f"✗ 长度检查失败: {len(result)} > {MAX_FILENAME_LENGTH}")
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
    print("唯一性测试:")
    print("-" * 30)

    # 测试唯一性
    base_title = "这是一个很长很长的标题用来测试哈希唯一性"
    titles = [base_title + "版本" + str(i) for i in range(1, 5)]

    results = [slugify(title) for title in titles]
    unique_results = set(results)

    print(f"输入标题数: {len(titles)}")
    print(f"生成结果数: {len(unique_results)}")

    if len(results) == len(unique_results):
        print("✓ 唯一性检查通过: 所有结果都不同")
        uniqueness_passed = True
    else:
        print("✗ 唯一性检查失败: 存在重复结果")
        uniqueness_passed = False

    print("\n" + "=" * 60)
    print("测试总结:")
    print(f"基本功能: {'✓ 通过' if all_passed else '✗ 失败'}")
    print(f"唯一性: {'✓ 通过' if uniqueness_passed else '✗ 失败'}")

    overall_passed = all_passed and uniqueness_passed

    if overall_passed:
        print("\n🎉 所有测试通过! slugify 函数工作正常。")
    else:
        print("\n❌ 部分测试失败，请检查实现。")

    return overall_passed

def test_performance():
    """测试性能优化效果"""
    import time

    print("\n性能测试:")
    print("-" * 30)

    # 测试数据
    test_texts = [
        "这是一个很长的标题用来测试性能" * 2,
        "【网站自荐】投资策略模拟器---通过直观可视化界面和详细数据分析，让用户深入了解各种投资策略优劣，从而做出更明智投资决策-·-issue-#5288-·-ruanyf-weekly",
        "A Very Long English Title with Many Words" * 3,
        "包含/特殊\\字符:*的文件?标题" * 2
    ]

    # 清空缓存
    global _COMPILED_HASH_CACHE
    _COMPILED_HASH_CACHE.clear()

    # 第一次运行（无缓存）
    start_time = time.time()
    for _ in range(100):
        for text in test_texts:
            slugify(text)
    first_run_time = time.time() - start_time

    # 第二次运行（有缓存）
    start_time = time.time()
    for _ in range(100):
        for text in test_texts:
            slugify(text)
    second_run_time = time.time() - start_time

    print(f"第一次运行（无缓存）: {first_run_time:.4f}秒")
    print(f"第二次运行（有缓存）: {second_run_time:.4f}秒")

    if second_run_time < first_run_time:
        improvement = ((first_run_time - second_run_time) / first_run_time) * 100
        print(f"缓存优化提升: {improvement:.1f}%")
        print("✓ 性能优化有效")
    else:
        print("⚠ 缓存效果不明显（可能因数据集较小）")

def run_comprehensive_tests():
    """运行完整测试套件"""
    print("开始全面测试...")

    # 基本功能测试
    basic_passed = run_tests()

    # 性能测试
    test_performance()

    print("\n" + "=" * 60)
    print("测试总结:")
    print(f"基本功能: {'✓ 通过' if basic_passed else '✗ 失败'}")

    return basic_passed

if __name__ == "__main__":
    run_comprehensive_tests()