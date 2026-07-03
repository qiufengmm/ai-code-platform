"""
用户模块接口自动化测试
覆盖：注册、登录、获取当前用户、注销
"""
import pytest


class TestUserRegister:
    """用户注册测试"""

    BASE = "/user/register"

    def test_register_success(self, ctx):
        """正向：注册新用户"""
        import random
        suffix = random.randint(10000, 99999)
        data = {
            "userAccount": f"test_{suffix}",
            "userPassword": "12345678",
            "checkPassword": "12345678"
        }
        resp = ctx.session.post(f"{ctx.base_url}{self.BASE}", json=data)
        body = resp.json()
        assert body.get("code") == 0 or body.get("data") is not None, f"注册失败: {body}"

    def test_register_duplicate_account(self, ctx):
        """异常：重复注册相同账号"""
        data = {
            "userAccount": "test_dup",
            "userPassword": "12345678",
            "checkPassword": "12345678"
        }
        # 第一次注册
        ctx.session.post(f"{ctx.base_url}{self.BASE}", json=data)
        # 第二次注册（应失败）
        resp = ctx.session.post(f"{ctx.base_url}{self.BASE}", json=data)
        body = resp.json()
        # 期望返回错误码
        assert body.get("code") != 0, "重复注册应失败"

    def test_register_password_mismatch(self, ctx):
        """异常：两次密码不一致"""
        import random
        suffix = random.randint(10000, 99999)
        data = {
            "userAccount": f"test_mismatch_{suffix}",
            "userPassword": "12345678",
            "checkPassword": "87654321"
        }
        resp = ctx.session.post(f"{ctx.base_url}{self.BASE}", json=data)
        body = resp.json()
        assert body.get("code") != 0, "密码不一致应注册失败"

    def test_register_empty_account(self, ctx):
        """异常：用户名为空"""
        data = {
            "userAccount": "",
            "userPassword": "12345678",
            "checkPassword": "12345678"
        }
        resp = ctx.session.post(f"{ctx.base_url}{self.BASE}", json=data)
        assert resp.status_code in (400, 200)
        body = resp.json()
        assert body.get("code") != 0, "空用户名应注册失败"

    def test_register_short_password(self, ctx):
        """异常：密码太短"""
        import random
        suffix = random.randint(10000, 99999)
        data = {
            "userAccount": f"test_short_{suffix}",
            "userPassword": "123",
            "checkPassword": "123"
        }
        resp = ctx.session.post(f"{ctx.base_url}{self.BASE}", json=data)
        body = resp.json()
        assert body.get("code") != 0, "密码过短应注册失败"


class TestUserLogin:
    """用户登录测试"""

    BASE = "/user/login"

    def test_login_success(self, ctx):
        """正向：正确账号密码登录"""
        data = {"userAccount": "test_auto", "userPassword": "12345678"}
        resp = ctx.session.post(f"{ctx.base_url}{self.BASE}", json=data)
        body = resp.json()
        assert body.get("code") == 0 or body.get("data") is not None
        # 验证返回字段
        user_info = body.get("data", {})
        assert "id" in str(user_info) or user_info.get("id") is not None

    def test_login_wrong_password(self, ctx):
        """异常：错误密码"""
        data = {"userAccount": "test_auto", "userPassword": "wrong_password"}
        resp = ctx.session.post(f"{ctx.base_url}{self.BASE}", json=data)
        body = resp.json()
        assert body.get("code") != 0, "错误密码应登录失败"

    def test_login_nonexist_user(self, ctx):
        """异常：不存在的用户"""
        data = {"userAccount": "nonexist_user_99999", "userPassword": "12345678"}
        resp = ctx.session.post(f"{ctx.base_url}{self.BASE}", json=data)
        body = resp.json()
        assert body.get("code") != 0, "不存在的用户应登录失败"
