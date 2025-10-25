#!/usr/bin/env python3
"""
无头浏览器内容提取器：使用Playwright进行CAPTCHA绕过和内容提取

该模块提供智能的反检测浏览器功能，作为Jina Reader失败时的备用方案，
特别针对基于JavaScript和浏览器指纹的CAPTCHA检测。
"""

import asyncio
import json
import logging
import random
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional, Tuple

# 导入SecurityManager
try:
    from .security_manager import SecurityManager
except ImportError:
    # 如果无法导入，创建一个简单的占位符
    class SecurityManager:
        def __init__(self, config_path=None):
            pass

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

class DetectionLevel(Enum):
    """检测级别枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    STEALTH = "stealth"

@dataclass
class StealthConfig:
    """隐形浏览器配置"""
    detection_level: DetectionLevel = DetectionLevel.MEDIUM
    use_proxy: bool = True
    use_headless: bool = False
    random_user_data: bool = True
    timeout: int = 30000
    max_retries: int = 3
    retry_delay: Tuple[int, int] = (2, 8)  # (min, max) seconds

@dataclass
class ExtractionResult:
    """内容提取结果"""
    url: str
    content: str
    method_used: str
    success: bool
    error_message: Optional[str] = None
    execution_time: float = 0.0
    proxy_used: Optional[Dict] = None

class HeadlessContentExtractor:
    """无头浏览器内容提取器"""

    def __init__(self, config: Optional[StealthConfig] = None):
        """初始化提取器"""
        self.config = config or StealthConfig()
        self.browser = None
        self.context = None
        self.security_manager = SecurityManager(
            config_file=getattr(config, 'security_config_path', None) if config else "config/security_config.json"
        )

        # 预定义的User-Agent
        self.user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        ]

    async def extract_content(self, url: str) -> ExtractionResult:
        """
        使用无头浏览器提取网页内容

        Args:
            url: 目标URL

        Returns:
            ExtractionResult: 提取结果
        """
        start_time = asyncio.get_event_loop().time()

        try:
            logger.info(f"开始无头浏览器内容提取: {url}")

            # 创建浏览器实例
            await self._initialize_browser()

            # 执行内容提取
            content = await self._perform_extraction_with_retry(url)

            execution_time = asyncio.get_event_loop().time() - start_time

            result = ExtractionResult(
                url=url,
                content=content,
                method_used="headless_browser",
                success=bool(content and len(content) > 100),
                execution_time=execution_time
            )

            logger.info(f"提取完成: 成功={result.success}, 耗时={execution_time:.2f}秒")

            return result

        except Exception as e:
            execution_time = asyncio.get_event_loop().time() - start_time
            error_msg = str(e)

            result = ExtractionResult(
                url=url,
                content="",
                method_used="headless_browser",
                success=False,
                error_message=error_msg,
                execution_time=execution_time
            )

            logger.error(f"无头浏览器提取失败: {error_msg}")
            return result

        finally:
            await self._cleanup()

    async def _initialize_browser(self):
        """初始化浏览器和上下文"""
        from playwright.async_api import async_playwright

        playwright = await async_playwright().start()

        # 启动参数
        launch_args = [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-infobars',
            '--window-position=0,0',
            '--ignore-certificate-errors',
            '--ignore-ssl-errors',
            '--ignore-certificate-errors-spki-list',
            '--disable-background-networking',
            '--disable-default-apps',
            '--disable-extensions',
            '--disable-sync',
            '--disable-translate',
            '--hide-scrollbars',
            '--metrics-recording-only',
            '--mute-audio',
            '--no-first-run',
        ]

        # 根据检测级别添加参数
        if self.config.detection_level in [DetectionLevel.HIGH, DetectionLevel.STEALTH]:
            launch_args.extend([
                '--disable-blink-features=AutomationControlled',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-features=CrossSiteDocumentBlockingIfIsolating',
                '--disable-features=CrossSiteDocumentBlockingAlways',
                '--disable-features=CrossSiteDocumentBlocking',
                '--disable-features=VizDisplayCompositor',
                '--disable-web-security',
                '--disable-gpu',
                '--disable-dev-shm-usage',
            ])

            # 添加随机User-Agent
            random_user_agent = random.choice(self.user_agents)
            launch_args.append(f'--user-agent={random_user_agent}')

            logger.info(f"使用检测级别: {self.config.detection_level.value}")
            logger.info(f"使用User-Agent: {random_user_agent}")

        self.browser = await playwright.chromium.launch(
            headless=self.config.use_headless,
            args=launch_args,
            timeout=self.config.timeout
        )

        self.context = await self._create_stealth_context()

    async def _create_stealth_context(self):
        """创建隐形上下文"""
        # 隐形上下文配置
        context_options = {
            'java_script_enabled': True,
            'ignore_https_errors': True,
            'extra_http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Upgrade-Insecure-Requests': '1',
            }
        }

        # 用户数据目录设置暂时注释掉，因为API可能不兼容
        # if self.config.random_user_data:
        #     context_options['user_data_dir'] = '/tmp/playwright_user_data'

        context = await self.browser.new_context(**context_options)

        # 注入反检测脚本
        await self._inject_bypass_scripts(context)

        return context

    async def _inject_bypass_scripts(self, context):
        """注入绕过检测的JavaScript脚本"""

        # 基础反检测脚本
        base_scripts = [
            # 移除webdriver痕迹
            """
            () => {
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                    configurable: true
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [],
                    configurable: true
                });
                window.chrome = window.chrome || {};
                window.chrome.runtime = window.chrome.runtime || {};
            }
            """,

            # 伪造设备信息
            """
            () => {
                Object.defineProperty(navigator, 'hardwareConcurrency', {
                    get: () => navigator.hardwareConcurrency || 4
                });
                Object.defineProperty(navigator, 'deviceMemory', {
                    get: () => navigator.deviceMemory || 8
                });
                screen.orientation = screen.orientation || { angle: 0, type: 'landscape-primary' };
            }
            """,

            # 防止检测自动化工具
            """
            () => {
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) =>
                    Promise.resolve({ status: 'granted' });

                const originalQueryLocal = window.navigator.permissions.queryLocalDescriptors;
                window.navigator.permissions.queryLocalDescriptors = () => Promise.resolve([]);

                // 移除可能的自动化标识
                delete window.cdc_adoQcache;
                delete window.cdc_iadoVcache;
                delete window._phantom;
                delete window.__nightmare;
                delete window.phantom;
            }
            """
        ]

        if self.config.detection_level == DetectionLevel.STEALTH:
            # 高级隐形脚本
            base_scripts.extend([
                # Canvas指纹伪造
                """
                () => {
                    const toBlob = HTMLCanvasElement.prototype.toBlob;
                    HTMLCanvasElement.prototype.toBlob = function(...args) {
                        const result = toBlob.apply(this, args);
                        result.toString = () => 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABGCAQAAAC1HAwCAAAAC0lEQVR42mNkY9E';
                        return result;
                    };
                }
                """,

                # WebGL指纹随机化
                """
                () => {
                    const getParameter = WebGLRenderingContext.prototype.getParameter;
                    WebGLRenderingContext.prototype.getParameter = function(parameter) {
                        if (parameter === 37445) { // UNMASKED_VENDOR_WEBGL
                            return random.choice(['Intel Inc.', 'NVIDIA Corporation', 'AMD']);
                        }
                        if (parameter === 37446) { // UNMASKED_RENDERER_WEBGL
                            return random.choice(['Intel(R) HD Graphics', 'NVIDIA GeForce GTX', 'AMD Radeon']);
                        }
                        return getParameter.call(this, parameter);
                    };
                }
                """,
            ])

        # 将脚本添加到上下文
        for script in base_scripts:
            await context.add_init_script(script)

    async def _perform_extraction_with_retry(self, url: str) -> str:
        """带重试的内容提取"""
        for attempt in range(self.config.max_retries):
            if attempt > 0:
                delay = random.uniform(*self.config.retry_delay)
                logger.info(f"重试第 {attempt + 1} 次，等待 {delay:.1f} 秒")
                await asyncio.sleep(delay)

            try:
                page = await self.context.new_page()

                # 设置视口和用户代理
                await page.set_viewport_size({"width": 1920, "height": 1080})
                await page.set_extra_http_headers({
                    "Referer": f"https://www.google.com/",
                })

                # 模拟人类行为
                await self._simulate_human_behavior(page)

                # 导航到目标页面
                response = await page.goto(url, wait_until='domcontentloaded', timeout=self.config.timeout)

                if response and response.status == 200:
                    logger.info(f"页面加载成功，尝试提取内容")

                    # 等待动态内容加载
                    await asyncio.sleep(random.uniform(3, 8))

                    # 提取内容
                    content = await self._extract_page_content(page)

                    if content and len(content) > 100:
                        logger.info(f"成功提取到内容，长度: {len(content)} 字符")
                        return content
                    else:
                        logger.warning("提取到的内容过短或为空")
                        return ""

                elif response and response.status == 403:
                    logger.warning("访问被拒绝 (403)，可能触发CAPTCHA检测")
                    if attempt < self.config.max_retries - 1:
                        continue

                else:
                    logger.error(f"页面访问失败，状态码: {response.status if response else 'None'}")
                    if attempt < self.config.max_retries - 1:
                        continue

            except Exception as e:
                logger.error(f"提取尝试 {attempt + 1} 失败: {str(e)}")
                if attempt < self.config.max_retries - 1:
                    continue

            logger.error(f"所有重试都失败了")
            return ""

    async def _extract_page_content(self, page) -> str:
        """从页面提取主要内容"""
        try:
            # 多种内容提取策略
            extraction_strategies = [
                # 策略1：查找主要内容区域
                """
                () => {
                    const mainSelectors = [
                        'main', 'article', '[role="main"]',
                        '.content', '.post-content', '.article-content',
                        '#content', '#main-content'
                    ];

                    for (const selector of mainSelectors) {
                        const element = document.querySelector(selector);
                        if (element && element.textContent && element.textContent.length > 200) {
                            return element.textContent;
                        }
                    }
                    return '';
                }
                """,

                # 策略2：查找标题下的内容
                """
                () => {
                    const title = document.querySelector('h1, h2, [role="heading"]');
                    if (title) {
                        const nextElement = title.nextElementSibling;
                        while (nextElement) {
                            if (nextElement.tagName.toLowerCase() === 'div' ||
                                nextElement.tagName.toLowerCase() === 'section' ||
                                nextElement.tagName.toLowerCase() === 'article') {
                                return nextElement.textContent;
                            }
                            nextElement = nextElement.nextElementSibling;
                        }
                    }
                    return '';
                }
                """,

                # 策略3：提取正文内容
                """
                () => {
                    // 移除脚本和样式标签
                    const scripts = document.querySelectorAll('script');
                    scripts.forEach(script => script.remove());

                    const styles = document.querySelectorAll('style');
                    styles.forEach(style => style.remove());

                    // 获取body内容
                    return document.body ? document.body.textContent : '';
                }
                """
            ]

            # 尝试每种策略
            for i, strategy in enumerate(extraction_strategies):
                try:
                    content = await page.evaluate(strategy)
                    logger.info(f"尝试提取策略 {i + 1}: {'成功' if content and len(content) > 100 else '失败'}")

                    if content and len(content) > 100:
                        return content

                except Exception as e:
                    logger.warning(f"提取策略 {i + 1} 失败: {str(e)}")

            # 最后尝试：简单的body内容
            try:
                content = await page.evaluate("() => document.body ? document.body.textContent : ''")
                return content if content else ""

            except Exception as e:
                logger.error(f"简单内容提取也失败: {str(e)}")
                return ""

        except Exception as e:
            logger.error(f"内容提取过程发生错误: {str(e)}")
            return ""

    async def _simulate_human_behavior(self, page):
        """模拟人类浏览行为"""
        try:
            # 随机滚动
            await asyncio.sleep(random.uniform(1, 3))

            # 模拟鼠标移动
            viewport = page.viewport_size
            for _ in range(random.randint(2, 5)):
                x = random.randint(100, viewport['width'] - 100)
                y = random.randint(100, viewport['height'] - 100)
                await page.mouse.move(x, y)
                await asyncio.sleep(random.uniform(0.1, 0.5))

            # 模拟键盘操作
            if random.random() < 0.3:
                await page.keyboard.press('Tab')
                await asyncio.sleep(random.uniform(0.2, 0.8))

            # 模拟滚动
            scroll_count = random.randint(3, 8)
            for _ in range(scroll_count):
                await page.evaluate("window.scrollBy(0, Math.random() * 200)")
                await asyncio.sleep(random.uniform(0.5, 2.0))

        except Exception as e:
            logger.warning(f"模拟人类行为失败: {str(e)}")

    async def _cleanup(self):
        """清理浏览器资源"""
        try:
            if self.context:
                await self.context.close()
                self.context = None

            if self.browser:
                await self.browser.close()
                self.browser = None

        except Exception as e:
            logger.error(f"清理浏览器资源失败: {str(e)}")

# 简化的同步接口
class HeadlessExtractorSync:
    """同步版本的无头浏览器提取器"""

    def __init__(self, config: Optional[StealthConfig] = None):
        self.extractor = HeadlessContentExtractor(config)

    def extract_content_sync(self, url: str) -> ExtractionResult:
        """同步接口提取内容"""
        return asyncio.run(self.extractor.extract_content(url))

def create_stealth_config(level: str = "medium", headless: bool = True) -> StealthConfig:
    """创建隐形配置"""
    try:
        detection_level = DetectionLevel(level.lower())
        return StealthConfig(
            detection_level=detection_level,
            use_headless=headless,
            use_proxy=True,
            timeout=30000
        )
    except ValueError:
        # 默认使用中等级别
        return StealthConfig()

# 使用示例
if __name__ == "__main__":
    async def demo():
        """演示用法"""
        # 创建配置
        config = create_stealth_config("high", headless=True)

        # 创建提取器
        extractor = HeadlessContentExtractor(config)

        # 测试URL
        test_url = "https://example.com"

        # 提取内容
        result = await extractor.extract_content(test_url)

        # 输出结果
        print(f"URL: {result.url}")
        print(f"成功: {result.success}")
        print(f"方法: {result.method_used}")
        print(f"内容长度: {len(result.content)}")
        print(f"耗时: {result.execution_time:.2f}秒")

        if result.error_message:
            print(f"错误: {result.error_message}")

    # 运行演示
    asyncio.run(demo())