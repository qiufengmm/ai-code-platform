"""
AI Code Platform - 接口自动化测试
"""
import pytest


class TestHealth:
    """健康检查"""

    def test_api_health(self, ctx):
        """检查系统是否正常运行"""
        # 访问用户接口验证系统可用
        resp = ctx.session.get(f"{ctx.base_url}/user/get/login")
        # 未登录返回 401 或错误码，但接口本身可用
        assert resp.status_code in (200, 401, 302), f"系统不可用: {resp.status_code}"
