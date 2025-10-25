#!/usr/bin/env python3
"""
安全管理器：提供URL安全检查、内容清理和审计功能
"""

import json
import logging
import re
from typing import List, Optional, Set
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class SecurityManager:
    """安全管理器，提供URL安全检查、内容清理和审计功能"""

    # 恶意URL模式检测
    MALICIOUS_PATTERNS = [
        r'javascript:',
        r'data:text/html',
        r'<script',
        r'onerror=',
        r'vbscript:',
        r'file://',
        r'ftp://',
        r'sql:',
        r'union\s+select',
        r'drop\s+table',
        r'exec\s*\(',
        r'eval\s*\(',
        r'system\s*\(',
        r'shell_exec\s*\(',
        r'base64_decode',
        r'\bhref\s*=',
    ]

    # 敏感信息关键词
    SENSITIVE_KEYWORDS = [
        'password', 'token', 'secret', 'key', 'credential', 'auth',
        'session', 'cookie', 'csrf', 'captcha', 'login', 'admin',
        'private_key', 'api_key', 'access_token', 'bearer', 'authorization',
        'credit_card', 'ssn', 'social_security', 'personal_data',
    ]

    def __init__(self, config_file: Optional[str] = None):
        self.blocked_domains: Set[str] = set()
        self.audit_log: List[dict] = []

        # 加载安全配置
        if config_file:
            self._load_security_config(config_file)

    def _load_security_config(self, config_file: str):
        """加载安全配置"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.blocked_domains = set(config.get('blocked_domains', []))
                self.sensitive_filters = config.get('sensitive_filters', {})
                logger.info(f"已加载安全配置: {config_file}")
        except Exception as e:
            logger.error(f"加载安全配置失败: {str(e)}")

    def validate_url(self, url: str) -> tuple[bool, Optional[str]]:
        """
        验证URL的安全性

        Returns:
            (is_safe, error_message)
        """
        try:
            # 基本URL格式检查
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False, "无效的URL格式"

            # 恶意模式检测
            for pattern in self.MALICIOUS_PATTERNS:
                if re.search(pattern, url, re.IGNORECASE):
                    return False, f"检测到潜在恶意内容: {pattern}"

            # 检查是否在黑名单中
            if parsed.netloc.lower() in self.blocked_domains:
                return False, f"域名已被阻止: {parsed.netloc}"

            # 检查敏感信息关键词
            url_lower = url.lower()
            for keyword in self.SENSITIVE_KEYWORDS:
                if keyword in url_lower:
                    return False, f"URL包含敏感信息: {keyword}"

            return True, None

        except Exception as e:
            logger.error(f"URL验证失败: {str(e)}")
            return False, str(e)

    def sanitize_content(self, content: str) -> tuple[str, List[str]]:
        """
        清理和验证内容

        Returns:
            (sanitized_content, detected_issues)
        """
        issues = []
        sanitized = content

        try:
            # 移除脚本标签
            sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)

            # 移除潜在的恶意事件处理器
            sanitized = re.sub(r'on\w+load\s*=', '', sanitized, flags=re.IGNORECASE)

            # 检测敏感信息
            content_lower = sanitized.lower()
            for keyword in self.SENSITIVE_KEYWORDS:
                if keyword in content_lower:
                    issues.append(f"检测到敏感关键词: {keyword}")
                    # 简单地移除或替换
                    sanitized = sanitized.replace(keyword, '[已过滤]')

            # 检查JavaScript代码
            if 'javascript:' in content_lower and '<' in sanitized:
                issues.append("检测到潜在JavaScript代码")
                sanitized = re.sub(r'<script[^>]*>[^<]*?</script>', '', sanitized)

            # 移除HTML注释（可能包含敏感信息）
            sanitized = re.sub(r'<!--.*?-->', '', sanitized)

            return sanitized, issues

        except Exception as e:
            logger.error(f"内容清理失败: {str(e)}")
            return content, [f"清理失败: {str(e)}"]

    def log_request(self, url: str, method: str = "GET", status_code: int = 200,
                   error_message: Optional[str] = None, config: Optional[dict] = None):
        """
        记录请求审计日志

        Args:
            url: 请求的URL
            method: HTTP方法
            status_code: 响应状态码
            error_message: 错误信息
            config: 使用的配置
        """
        if not self._should_log_request(url, status_code):
            return

        # 检查内容是否包含敏感信息
        is_safe, security_error = self.validate_url(url)
        if not is_safe:
            error_message = security_error or "URL未通过安全检查"

        audit_entry = {
            'timestamp': self._get_timestamp(),
            'url': url,
            'method': method,
            'status_code': status_code,
            'error_message': error_message,
            'config': config or {},
            'security_level': self._get_security_level(status_code),
            'blocked': not is_safe
        }

        self.audit_log.append(audit_entry)
        self._write_audit_log()

    def _should_log_request(self, url: str, status_code: int) -> bool:
        """判断是否应该记录此请求"""
        # 只记录失败请求或特定状态码
        return (status_code != 200 or
                status_code in [403, 429, 500] or
                self._is_problematic_url(url))

    def _get_security_level(self, status_code: int) -> str:
        """根据状态码确定安全级别"""
        if status_code in [403, 401, 403]:
            return 'HIGH'
        elif status_code in [429, 503]:
            return 'MEDIUM'
        elif status_code >= 500:
            return 'LOW'
        else:
            return 'INFO'

    def _is_problematic_url(self, url: str) -> bool:
        """检查是否为有问题的URL"""
        return any(problematic in url.lower() for problematic in ['admin', 'login', 'api', 'internal'])

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        import datetime
        return datetime.now().isoformat()

    def _write_audit_log(self):
        """写入审计日志"""
        try:
            log_file = f"logs/security_audit_{datetime.now().strftime('%Y%m%d')}.json"

            # 保持日志文件大小
            if len(self.audit_log) > 10000:
                self.audit_log = self.audit_log[-5000:]

            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(self.audit_log, f, indent=2, ensure_ascii=False)

            logger.info(f"审计日志已写入: {len(self.audit_log)} 条记录")

        except Exception as e:
            logger.error(f"写入审计日志失败: {str(e)}")

    def get_security_summary(self) -> dict:
        """获取安全统计摘要"""
        if not self.audit_log:
            return {'total_requests': 0, 'blocked_requests': 0}

        total_requests = len(self.audit_log)
        blocked_requests = sum(1 for entry in self.audit_log if entry.get('blocked', False))

        return {
            'total_requests': total_requests,
            'blocked_requests': blocked_requests,
            'blocking_rate': (blocked_requests / total_requests * 100) if total_requests > 0 else 0,
            'last_24h_blocked': sum(1 for entry in self.audit_log[-100:] if entry.get('blocked', False)),
        }

    def clear_audit_log(self):
        """清空审计日志"""
        self.audit_log.clear()
        logger.info("审计日志已清空")

# 使用示例
if __name__ == "__main__":
    # 创建安全管理器
    security_manager = SecurityManager("config/security_config.json")

    # 测试URL安全检查
    test_urls = [
        "https://example.com/normal",
        "https://example.com/javascript:alert('xss')",
        "https://malicious-site.com/admin",
        "https://example.com/api?key=secret123",
    ]

    print("URL安全检查测试:")
    for url in test_urls:
        is_safe, error = security_manager.validate_url(url)
        status = "安全" if is_safe else "不安全"
        print(f"  {url}: {status}")
        if error:
            print(f"    错误: {error}")

    print("\n内容清理测试:")
    test_content = "这是一个正常的内容，包含password=secret和token=abc123"
    sanitized, issues = security_manager.sanitize_content(test_content)
    print(f"  原内容长度: {len(test_content)}")
    print(f"  清理后长度: {len(sanitized)}")
    print(f"  检测到的问题: {issues}")

    print(f"\n安全统计: {security_manager.get_security_summary()}")