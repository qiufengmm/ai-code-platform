"""
pytest 全局配置
自动管理测试会话：登录 → 测试 → 清理
"""
import pytest
import requests

BASE_URL = "http://localhost:8123/api"

class TestContext:
    """测试上下文 - 存储全局状态"""
    def __init__(self):
        self.session = requests.Session()
        self.base_url = BASE_URL
        self.current_user = None

@pytest.fixture(scope="session")
def ctx():
    """全局测试上下文"""
    return TestContext()

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture
def logged_in(ctx):
    """
    登录 fixture - 每个测试类自动获取登录状态
    测试账号：test_user / 12345678
    """
    # 1. 注册测试账号（如果已存在会失败，不影响）
    register_data = {
        "userAccount": "test_auto",
        "userPassword": "12345678",
        "checkPassword": "12345678"
    }
    ctx.session.post(f"{BASE_URL}/user/register", json=register_data)

    # 2. 登录
    login_data = {
        "userAccount": "test_auto",
        "userPassword": "12345678"
    }
    resp = ctx.session.post(f"{BASE_URL}/user/login", json=login_data)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("code") == 0 or data.get("data") is not None

    # 3. 保存用户信息
    ctx.current_user = data.get("data")
    print(f"\n>>> 登录成功: test_auto")
    return ctx
