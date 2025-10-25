#!/usr/bin/env python3
"""
性能优化器：提供浏览器池管理、智能重试、性能监控等功能
"""

import asyncio
import json
import logging
import random
import time
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class BrowserInstance:
    """浏览器实例信息"""
    browser_id: str
    playwright_instance: object
    context: object
    page: object
    created_at: float
    last_used_at: float
    success_count: int = 0
    failure_count: int = 0
    total_requests: int = 0
    total_response_time: float = 0.0

class ProxyManager:
    """代理管理器"""

    def __init__(self):
        self.proxies: List[Dict] = []
        self.healthy_proxies: Set[str] = set()
        self.blocked_proxies: Set[str] = set()
        self.proxy_usage: Dict[str, int] = {}

    def add_proxy(self, proxy: Dict) -> bool:
        proxy_str = f"{proxy['server']}:{proxy.get('username', '')}:{proxy.get('password', '')}"
        if proxy_str not in self.proxy_usage:
            self.proxies.append(proxy)
            self.proxy_usage[proxy_str] = 0
            return True
        return False

    def get_random_proxy(self) -> Optional[Dict]:
        """获取随机健康代理"""
        healthy_proxies = [p for p in self.proxies if p['server'] in self.healthy_proxies]
        if not healthy_proxies:
            return None

        return random.choice(healthy_proxies)

    def mark_proxy_success(self, proxy_str: str):
        """标记代理成功"""
        self.proxy_usage[proxy_str] = self.proxy_usage.get(proxy_str, 0) + 1

    def mark_proxy_failure(self, proxy_str: str):
        """标记代理失败"""
        self.proxy_usage[proxy_str] = self.proxy_usage.get(proxy_str, 0) + 1

    def mark_proxy_healthy(self, proxy_str: str):
        """标记代理为健康"""
        self.healthy_proxies.add(proxy_str)

    def mark_proxy_blocked(self, proxy_str: str):
        """标记代理为被阻止"""
        if proxy_str in self.healthy_proxies:
            self.healthy_proxies.remove(proxy_str)
        self.blocked_proxies.add(proxy_str)

    def get_statistics(self) -> Dict:
        """获取代理统计信息"""
        return {
            'total_proxies': len(self.proxies),
            'healthy_proxies': len(self.healthy_proxies),
            'blocked_proxies': len(self.blocked_proxies),
            'usage_stats': dict(self.proxy_usage)
        }

class PerformanceOptimizer:
    """性能优化器"""

    def __init__(self):
        self.browser_pool: List[BrowserInstance] = []
        self.proxy_manager = ProxyManager()
        self.request_history: List[Dict] = []
        self.rate_limiter = RateLimiter(requests_per_minute=30)
        self.performance_stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'avg_response_time': 0.0,
            'total_response_time': 0.0
        }

    def calculate_optimal_delay(self, instance: BrowserInstance) -> float:
        """根据实例使用情况计算最优延迟"""
        success_rate = instance.success_count / max(instance.total_requests, 1)

        if success_rate < 0.7:
            return 5.0  # 成功率低，增加延迟
        elif success_rate < 0.9:
            return 2.0  # 成功率中等，适中延迟
        else:
            return 1.0  # 成功率高，低延迟

    def get_best_browser(self, url: str) -> Optional[BrowserInstance]:
        """获取最佳浏览器实例"""
        if not self.browser_pool:
            return None

        # 根据URL和实例状态选择最佳浏览器
        available_browsers = [b for b in self.browser_pool if not b.in_use]

        if not available_browsers:
            return None

        # 选择最近使用成功率高且响应快的实例
        best_browser = min(available_browsers, key=lambda b: (
            b.success_count / max(b.total_requests, 1) * 0.5 +  # 50%成功率权重
            1.0 / (b.total_response_time / max(b.total_requests, 1)) if b.total_requests > 0 else 10.0  # 响应时间权重
            - self.calculate_optimal_delay(b)  # 延迟惩罚
        ))

        return best_browser

    async def release_browser(self, instance: BrowserInstance):
        """释放浏览器实例"""
        if instance.page:
            await instance.page.close()
        if instance.context:
            await instance.context.close()

        instance.in_use = False
        instance.last_used_at = time.time()
        logger.info(f"释放浏览器实例: {instance.browser_id}")

    async def acquire_browser(self, url: str) -> Optional[BrowserInstance]:
        """获取或创建浏览器实例"""
        # 尝试从池中获取
        existing_browser = self.get_best_browser(url)
        if existing_browser:
            existing_browser.in_use = True
            existing_browser.last_used_at = time.time()
            logger.info(f"复用浏览器实例: {existing_browser.browser_id}")
            return existing_browser

        # 创建新实例（如果可用）
        if len(self.browser_pool) < 5:  # 限制最大并发数
            return None

        # 这里可以集成代理获取
        proxy = self.proxy_manager.get_random_proxy()

        try:
            # 模拟实例创建时间
            start_time = time.time()

            # 实际的浏览器创建逻辑应该在这里
            # 这里只是返回模拟的实例信息
            browser_id = f"browser_{len(self.browser_pool)}"

            instance = BrowserInstance(
                browser_id=browser_id,
                playwright_instance=None,  # 实际创建
                context=None,
                page=None,
                created_at=start_time,
                proxy_used=proxy
            )

            self.browser_pool.append(instance)
            logger.info(f"创建新的浏览器实例: {browser_id}")

            # 模拟初始化时间
            init_time = time.time() - start_time
            await asyncio.sleep(random.uniform(1, 3))  # 模拟初始化开销

            instance.created_at = time.time() - init_time

            return instance

        except Exception as e:
            logger.error(f"创建浏览器实例失败: {str(e)}")
            return None

    def update_statistics(self, result: 'success' or 'failure', response_time: float):
        """更新性能统计"""
        self.performance_stats['total_requests'] += 1

        if result == 'success':
            self.performance_stats['successful_requests'] += 1
        else:
            self.performance_stats['failed_requests'] += 1

        self.performance_stats['total_response_time'] += response_time

        # 更新平均响应时间
        if self.performance_stats['total_requests'] > 0:
            self.performance_stats['avg_response_time'] = (
                self.performance_stats['total_response_time'] / self.performance_stats['total_requests']
            )

    def get_performance_report(self) -> Dict:
        """获取性能报告"""
        if self.performance_stats['total_requests'] == 0:
            return {}

        success_rate = (self.performance_stats['successful_requests'] /
                       self.performance_stats['total_requests']) * 100

        return {
            'performance_stats': self.performance_stats,
            'browser_pool': {
                'total_instances': len(self.browser_pool),
                'in_use': sum(1 for b in self.browser_pool if b.in_use),
                'utilization_rate': len([b for b in self.browser_pool if b.total_requests > 10]) / max(len(self.browser_pool), 1) * 100
            },
            'proxy_stats': self.proxy_manager.get_statistics(),
            'success_rate': success_rate
        }

class RateLimiter:
    """请求频率限制器"""

    def __init__(self, requests_per_minute: int = 30):
        self.requests_per_minute = requests_per_minute
        self.request_times: List[float] = []
        self.max_requests_per_minute = requests_per_minute * 2  # 允许突发

    async def wait_if_needed(self):
        """如果需要，等待到下个时间窗口"""
        now = time.time()

        # 清理过期的请求时间
        self.request_times = [t for t in self.request_times if now - t > 60]

        if len(self.request_times) >= self.max_requests_per_minute:
            sleep_time = 60 - (now - self.request_times[-1])
            logger.info(f"达到频率限制，等待 {sleep_time:.1f} 秒")
            await asyncio.sleep(sleep_time)

    def can_make_request(self) -> bool:
        """检查是否可以发送请求"""
        now = time.time()
        recent_requests = [t for t in self.request_times if now - t < 60]
        return len(recent_requests) < self.requests_per_minute

    async def acquire(self):
        """获取请求许可"""
        while not self.can_make_request():
            await asyncio.sleep(0.1)  # 短暂等待
        self.request_times.append(time.time())

    async def release(self):
        """释放请求许可"""
        if self.request_times:
            self.request_times.pop()

# 使用示例
if __name__ == "__main__":
    optimizer = PerformanceOptimizer()

    # 添加一些测试代理
    test_proxies = [
        {'server': 'proxy1.example.com:8080', 'username': 'user1', 'password': 'pass1'},
        {'server': 'proxy2.example.com:8080', 'username': 'user2', 'password': 'pass2'},
    ]

    for proxy in test_proxies:
        optimizer.proxy_manager.add_proxy(proxy)

    print("性能优化器测试")
    print(f"代理池状态: {optimizer.proxy_manager.get_statistics()}")

    # 模拟性能统计
    for i in range(10):
        optimizer.update_statistics('success', random.uniform(0.5, 3.0))
        optimizer.update_statistics('failure', random.uniform(0.1, 1.0))
        optimizer.update_statistics('success', random.uniform(0.8, 4.0))

    print(f"性能报告: {optimizer.get_performance_report()}")