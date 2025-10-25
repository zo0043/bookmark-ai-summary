#!/usr/bin/env python3
"""
CAPTCHA绕过系统测试和演示脚本

此脚本全面测试无头浏览器在各种CAPTCHA场景下的表现，
包括成功和失败场景的模拟。
"""

import asyncio
import json
import os
import time
from pathlib import Path
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from bookmark_ai_summary.headless_content_extractor import (
    HeadlessContentExtractor,
    create_stealth_config,
    ExtractionResult,
    StealthConfig,
    DetectionLevel
    HeadlessContentExtractorSync
    ExtractionResult
)

logger = logging.getLogger(__name__)

class CaptchaTestSuite:
    """CAPTCHA测试套件"""

    def __init__(self, config_path: str = "config/captcha_test_config.json"):
        """初始化测试套件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
                logger.info(f"已加载CAPTCHA测试配置: {config_path}")
        except Exception as e:
                logger.error(f"加载配置失败: {str(e)}")
                self.config = self._get_default_config()

    def _get_default_config(self) -> dict:
        """获取默认测试配置"""
        return {
            "detection_level": "medium",
            "use_headless": True,
            "use_proxy": True,
            "timeout": 30000,
            "max_retries": 3,
            "retry_delay": [2, 8],
            "test_urls": [
                "https://www.google.com/recaptcha/api/demo",  # Google reCAPTCHA Demo
                "https://www.baidu.com",
                "https://www.tencent.com",
                "https://captcha.aaen",
                "https://www.hcaptcha.com",
                "https://2captcha.com",
                "https://www.anti-captcha.com",
                "https://turnstile.com/turnstile/",
                "https://www.funcaptcha.com/",
                "https://arkoselabsaptcha.com/",
            ]
            ]
        }

    async def run_tests(self):
        """运行完整的CAPTCHA测试套件"""
        logger.info("开始CAPTCHA绕过测试...")

        total_tests = 0
        successful_tests = 0

        test_results = []
        error_results = []

        for i, test_case in enumerate(self.config['test_urls'], 1):
            logger.info(f"测试用例 {i}: {test_case}")

            result = await self._test_single_scenario(test_case)
            total_tests += 1

            if result.success:
                successful_tests += 1
            else:
                error_results.append({
                    'url': test_case['url'],
                    'test_type': test_case['test_type'],
                    'error': result.error_message
                })

            # 根据不同的测试类型使用不同的配置
            elif test_case['test_type'] == 'no_headless_browser':
                result = await self._test_no_headless_success(test_case)
            elif test_case['test_type'] == 'with_headless_failure':
                result = await self._test_with_headless_failure(test_case)
            elif test_case['test_url'] == 'jina_reader_success':
                result = await self._test_jina_reader_after_headless(test_case)
            elif test_case['test_url'] == 'enterprise_api_success':
                result = await self._test_enterprise_api(test_case)

            logger.info(f"测试用例 {i} 完成: {'成功' if result.success else '失败'}")

            # 记录结果
            test_results.append(result)

        # 输出测试总结
        await self._generate_test_report(test_results)

        return test_results

    async def _test_no_headless_success(self, test_case: dict) -> ExtractionResult:
        """测试无头浏览器在成功获取内容的情况"""
        logger.info(f"测试无头浏览器成功: {test_case['url']}")

        # 这里应该成功获取内容，验证无头浏览器功能
        # 但为了测试，我们故意模拟一些异常情况
        try:
            # 模拟JavaScript错误
            await page.evaluate("throw new Error('test error');")
            await asyncio.sleep(1)
            logger.warning("模拟JavaScript错误执行失败")
        except Exception as e:
            logger.error(f"JavaScript执行失败: {str(e)}")

        # 获取实际内容
        content = await self._extract_page_content(test_case['url'])

        if not content or len(content) < 50:
            return ExtractionResult(
                url=test_case['url'],
                content="",
                method_used="headless_browser",
                success=False,
                error_message="内容为空或过短"
            )

        return ExtractionResult(
            url=test_case['url'],
                content=content,
                method_used="headless_browser",
                success=True,
                execution_time=0.0
            )

    async def _test_with_headless_failure(self, test_case: dict) -> ExtractionResult:
        """测试无头浏览器在失败时的处理逻辑"""
        logger.info(f"测试无头浏览器失败: {test_case['url']}")

        try:
            # 这里应该失败，因为我们故意使用了无头浏览器模式
            # 验证错误处理机制
            try:
                await page.goto("about:blank")
                await page.wait_for_timeout(10000)
            except Exception as e:
                pass

            # 验证是否正确地跳转到错误页面
            current_url = page.url
            if current_url and "about:blank" in current_url:
                logger.warning("页面导航到了错误页面，可能被拦截")
                return ExtractionResult(
                    url=test_case['url'],
                    content="",
                    method_used="headless_browser",
                    success=False,
                    error_message="页面被重定向到错误页面"
                )

            # 模拟内存不足错误
            try:
                await page.set_content("".join([""] * 100000))  # 分配内存不足错误
                logger.error("页面内存不足")
            except Exception as e:
                pass

            # 模拟网络超时
            try:
                await page.set_navigation_timeout(100)
                logger.error("网络超时")
            except Exception as e:
                pass

            # 模拟连接关闭
            try:
                await page.close()
                logger.warning("连接被意外关闭")
            except Exception as e:
                pass

            # 验证代理使用情况
            proxy_used = getattr(page.context, 'proxy_used', None)
            if proxy_used:
                logger.info(f"代理配置: {proxy_used}")

            return ExtractionResult(
                url=test_case['url'],
                content="",
                method_used="headless_browser",
                success=False,
                error_message="页面关闭失败"
            )

    async def _test_jina_reader_after_headless(self, test_case: dict) -> ExtractionResult:
        """测试Jina Reader在无头浏览器模式失败后的情况"""
        logger.info(f"测试Jina Reader在无头浏览器失败后: {test_case['url']}")

        # 回退到Jina Reader
        content = await self._extract_content_with_headless_fallback(test_case['url'], use_headless=False)

        return ExtractionResult(
            url=test_case['url'],
            content=content,
            method_used="jina_reader",
            success=False,
            error_message="Jina Reader失败"
        )

    async def _test_enterprise_api(self, test_case: dict) -> ExtractionResult:
        """测试企业级API的成功情况"""
        logger.info(f"测试企业级API: {test_case['url']}")

        try:
            # 这里应该总是成功的
            # 使用企业级API绕过
            from bookmark_ai_summary.headless_content_extractor import (
                create_stealth_config
                ExtractionResult,
                EnterpriseAPIConfig
                )

            config = create_stealth_config("enterprise", headless=True)

            # 模拟企业级访问
            try:
                logger.info("尝试企业级API...")
                # 这里可以返回成功，或者需要特定的API key
                pass

            # 页面测试逻辑...
        except Exception as e:
                logger.error(f"企业级API测试失败: {str(e)}")

            return ExtractionResult(
                url=test_case['url'],
                content="",
                method_used="enterprise_api",
                success=False,
                error_message="企业级API测试失败"
            )

    async def _generate_test_report(self, test_results: List[dict]) -> None:
        """生成测试报告"""
        if not test_results:
            logger.warning("没有测试结果需要生成报告")
            return None

        # 统计结果
        success_count = sum(1 for result in test_results if result['success'])
        success_rate = (success_count / total_tests) * 100

        # 创建报告
        report_lines = [
            f"## CAPTCHA绕过测试报告",
            f"测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"总测试数: {total_tests}",
            f"成功测试数: {success_count}",
            f"成功率: {success_rate:.2f}",
            f"失败测试数: {total_tests - success_count}",
        ]

        # 按方法成功率统计
        method_success_counts = {
            'jina_reader': 0,
            'headless_browser': 0,
            'enterprise_api': 0,
            'with_headless_browser': 0
        }

        for result in test_results:
            if result['success']:
                method_success_counts[result['method_used']] += 1

        # 失败类型统计
        error_types = {}
        for result in test_results:
            if not result['success']:
                error_type = result.get('error_type', 'unknown')
                error_types[error_type] = error_types.get(result['error_type'], 0) + 1

        # 添加详细的方法成功率信息
        method_success_rates = {}
        for method, count in method_success_counts.items():
            if count > 0:
                method_success_rates[method] = count / method_success_counts[method] * 100

        # 显示测试结果
        report_lines.extend([
            f"### 📊 总体情况",
            f"- **总测试数**: {total_tests}",
            f"- **成功测试数**: {success_count}",
            f"- **总体成功率**: {success_rate:.2f}%",
            "",
        ])

        # 添加按方法分类的结果
        report_lines.extend([
            f"\n#### Jina Reader (0/0% 成功率)",
            f"- 无头浏览器 (0/0% 成功率)",
            f"- 企业级API (0/0% 成功率)",
            f"- 无头浏览器 (0/0% 成功率)",
        ])

        # 失败类型统计
        for error_type, count in error_types.items():
            report_lines.extend([
                f"\n- {error_type}: {count} 个"
            ])

        # 按加案例详情
        for result in test_results:
            report_lines.extend([
                f"\n\n### 测试 {i+1}: {test_case['test_type']}",
                f"  - URL: {result.url}",
                f"  - 方法: {result.method_used}",
                f"  - 成功: {'是' if result['success'] else '否'}",
                f"  - 耗误: {result.get('error_message', '无' if result.error_message else '无'}",
                f"  - 耗时: {result.execution_time:.2f}秒"
            ])
        ])

        # 保存报告
        report_file = f"logs/captcha_test_report_{datetime.now().strftime('%Y%m%d_%H:%M:%S')}.md"

        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.writelines(report_lines)
                logger.info(f"测试报告已保存到: {report_file}")
        except Exception as e:
                logger.error(f"保存测试报告失败: {str(e)}")

        logger.info(f"测试报告已生成")

    def _test_config_compatibility(self):
        """测试配置兼容性"""
        current_config = self.config

        # 检查环境变量
        use_headless_env = os.environ.get('USE_HEADLESS_BROWSER', 'false').lower() == 'true'
        headless_available = HEADLESS_AVAILABLE

        if use_headless_env and not headless_available:
            logger.error("配置错误：无头浏览器模块但 USE_HEADLESS_BROWSER=true")
            return False

        # 验证文件存在
        config_file = self.config.security_config_path
        if not os.path.exists(config_file):
            logger.warning(f"安全配置文件不存在: {config_file}")
            return False

        return True

    async def _run_single_test_with_config(self, config: dict) -> ExtractionResult:
        """使用指定配置运行单个测试"""
        # 临时替换配置
        original_config = self.config
        self.config = config

        try:
            # 应用新配置
            logger.info(f"使用配置: {config.get('detection_level')}")

            # 运行测试
            result = await self._extract_content_with_config(test_case['url'])

            # 恢复原始配置
            self.config = original_config

            logger.info(f"测试完成，使用配置: {config.get('detection_level')}")

            return result

    def run(self):
        """运行完整的CAPTCHA测试套件"""
        logger.info("开始CAPTCHA绕过测试套件...")

        try:
            # 检查配置
            if not self._test_config_compatibility():
                logger.error("配置不兼容，退出测试")
                return None

            test_results = []

            # 运行每个测试用例
            for test_case in self.config['test_urls']:
                logger.info(f"开始测试: {test_case.get('test_type')}")

            result = await self._run_single_test_with_config(test_case)
                test_results.append(result)

            # 生成报告
            await self._generate_test_report(test_results)

            return test_results

    async def run_with_retry_on_failure(self, test_case: dict) -> ExtractionResult:
        """测试失败重试机制"""
        logger.info(f"测试失败重试: {test_case.get('test_type')}")

        for attempt in range(test_case.get('max_retries')):
            logger.info(f"重试第 {attempt + 1}/{test_case.get('max_retries')}")

            # 增加重试延迟
            delay = random.uniform(*self.config.retry_delay)
            logger.info(f"等待 {delay:.1f} 秒")
            await asyncio.sleep(delay)

            result = await self._run_single_test_with_config(test_case)

            if result.success:
                return result

        # 如果所有重试都失败
            logger.error(f"所有重试都失败了: {test_case.get('url')}")
            return ExtractionResult(
                url=test_case['url'],
                content="",
                method_used="headless_browser",
                success=False,
                error_message="所有重试都失败",
                execution_time=0.0
            )

        except Exception as e:
            logger.error(f"重试过程异常: {str(e)}")
            return ExtractionResult(
                url=test_case['url'],
                content="",
                method_used="headless_browser",
                success=False,
                error_message=f"重试异常: {str(e)}",
                execution_time=0.0
            )

    async def run_with_retry_on_failure(self, test_case: dict) -> ExtractionResult:
        """测试失败重试机制，保留历史结果"""
        logger.info(f"测试失败重试: {test_case.get('url')}")

        # 重试一定次数
        max_retries = test_case.get('max_retries')
        last_result = None

        for attempt in range(max_retries):
            delay = random.uniform(*self.config.retry_delay)
            logger.info(f"重试第 {attempt + 1}/{max_retries} 次，等待 {delay:.1f} 秒")

            try:
                result = await self._run_single_test_with_config(test_case)
                if result.success:
                    return result
                logger.info(f"重试成功！")
                    break
                else:
                    logger.warning(f"重试第 {attempt + 1}/{max_retries} 次述: 失败")

            await asyncio.sleep(delay)

        return last_result or ExtractionResult(
            url=test_case['url'],
            content="",
            method_used="headless_browser",
            success=last_result.success if last_result else False,
            error_message=f"所有重试都失败",
            execution_time=last_result.execution_time if last_result else 0.0
            )

    async def generate_test_report(self, test_results: List[dict]) -> str:
        """生成详细的测试报告"""
        total_tests = len(test_results)
        success_count = sum(1 for r in test_results if r['success'])
        success_rate = (success_count / total_tests) * 100

        # 创建报告
        report_lines = [
            f"# CAPTCHA绕过测试报告",
            f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"总测试数: {total_tests}",
            f"成功测试数: {success_count}",
            f"总体成功率: {success_rate:.2f}%",
            f"失败测试数: {total_tests - success_count}",
            f"",
            f"## 📊 按策略评估",
            f"### 成功率统计:"
        ]

        # 按各方法成功率：
        method_success_rates = {}
        for r in test_results:
            if r['success']:
                method_success_rates[r['method_used']] = method_success_rates.get(r['method_used'], 0) + 1

        return report_lines

        report_file = f"logs/captcha_test_report_{datetime.now().strftime('%Y%m%d_%H:%M:%S')}.md"

        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.writelines(report_lines)
                logger.info(f"测试报告已保存到: {report_file}")
        except Exception as e:
                logger.error(f"保存测试报告失败: {str(e)}")

        logger.info(f"CAPTCHA绕过测试完成，成功率: {success_rate:.2f}%")

        return report_file

# 使用示例
if __name__ == "__main__":
    # 创建测试配置
    config_file = "config/captcha_test_config.json"

    # 创建测试配置
    test_config = {
        "detection_level": "medium",
        "use_headless": True,
        "use_proxy": True,
        "timeout": 30000,
        "max_retries": 3,
        "retry_delay": [2, 8],
        "test_urls": [
            "https://www.google.com/recaptcha/api/demo",
            "https://www.baidu.com",
            "https://example-captcha.com",
            "https://example-captcha.com"
        ]
    }

    # 创建实例并运行测试
    tester = CaptchaTestSuite()
    asyncio.run(tester.run_tests())