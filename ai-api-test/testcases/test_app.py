"""
应用模块接口自动化测试
覆盖：创建应用、查询详情、更新、列表、删除
"""
import pytest
import random


class TestAppCRUD:
    """应用 CRUD 测试"""

    created_app_ids = []

    @staticmethod
    def _make_app_data(suffix):
        return {
            "appName": f"测试应用_{suffix}",
            "appDesc": f"自动化测试创建_{suffix}",
            "initPrompt": f"请生成一个{suffix}相关的网页应用",
        }

    def test_create_app_success(self, ctx, logged_in):
        """正向：创建应用"""
        suffix = random.randint(10000, 99999)
        data = self._make_app_data(suffix)
        resp = ctx.session.post(f"{ctx.base_url}/app/add", json=data)
        body = resp.json()

        # 验证创建成功
        assert body.get("code") == 0 or body.get("data") is not None, f"创建应用失败: {body}"
        app_id = body.get("data")
        assert app_id is not None and int(app_id) > 0
        self.created_app_ids.append(app_id)
        print(f">>> 创建应用成功, ID: {app_id}")

    def test_create_app_empty_name(self, ctx, logged_in):
        """异常：应用名称为空"""
        data = {"appName": "", "appDesc": "名称为空的应用"}
        resp = ctx.session.post(f"{ctx.base_url}/app/add", json=data)
        body = resp.json()
        assert body.get("code") != 0 or resp.status_code == 400

    def test_get_app_detail(self, ctx, logged_in):
        """正向：获取应用详情"""
        # 先创建一个应用
        suffix = random.randint(10000, 99999)
        create_data = self._make_app_data(suffix)
        resp = ctx.session.post(f"{ctx.base_url}/app/add", json=create_data)
        app_id = resp.json().get("data")
        assert app_id is not None

        # 查询详情
        resp = ctx.session.get(f"{ctx.base_url}/app/get/vo", params={"id": app_id})
        body = resp.json()
        assert body.get("code") == 0 or body.get("data") is not None
        app_vo = body.get("data", {})
        # 验证返回字段
        assert "appName" in str(app_vo) or app_vo.get("appName") is not None

    def test_get_app_not_exist(self, ctx, logged_in):
        """异常：查询不存在的应用"""
        resp = ctx.session.get(f"{ctx.base_url}/app/get/vo", params={"id": 99999999})
        body = resp.json()
        assert body.get("code") != 0, "查询不存在的应用应返回错误"

    def test_update_app_name(self, ctx, logged_in):
        """正向：更新应用名称"""
        # 先创建
        suffix = random.randint(10000, 99999)
        create_data = self._make_app_data(suffix)
        resp = ctx.session.post(f"{ctx.base_url}/app/add", json=create_data)
        app_id = resp.json().get("data")
        assert app_id is not None

        # 更新名称
        update_data = {"id": app_id, "appName": f"更新后_{suffix}"}
        resp = ctx.session.post(f"{ctx.base_url}/app/update", json=update_data)
        body = resp.json()
        assert body.get("code") == 0 or body.get("data") is True, f"更新失败: {body}"

    def test_update_app_not_owner(self, ctx, logged_in):
        """异常：更新不属于自己的应用"""
        update_data = {"id": 1, "appName": "尝试修改他人应用"}
        resp = ctx.session.post(f"{ctx.base_url}/app/update", json=update_data)
        body = resp.json()
        # 应无权限
        assert body.get("code") != 0 or body.get("data") is False

    def test_my_app_list(self, ctx, logged_in):
        """正向：获取我的应用列表"""
        data = {"pageNum": 1, "pageSize": 10}
        resp = ctx.session.post(f"{ctx.base_url}/app/my/list/page/vo", json=data)
        body = resp.json()
        assert body.get("code") == 0 or body.get("data") is not None
        page_data = body.get("data", {})
        print(f">>> 我的应用列表: {page_data.get('totalRow', 'unknown')} 条记录")

    def test_good_app_list(self, ctx):
        """正向：获取精选应用列表（无需登录）"""
        data = {"pageNum": 1, "pageSize": 10}
        resp = ctx.session.post(f"{ctx.base_url}/app/good/list/page/vo", json=data)
        body = resp.json()
        assert body.get("code") == 0 or body.get("data") is not None

    def test_delete_own_app(self, ctx, logged_in):
        """正向：删除自己创建的应用"""
        # 先创建
        suffix = random.randint(10000, 99999)
        create_data = self._make_app_data(suffix)
        resp = ctx.session.post(f"{ctx.base_url}/app/add", json=create_data)
        app_id = resp.json().get("data")
        assert app_id is not None

        # 删除
        delete_data = {"id": app_id}
        resp = ctx.session.post(f"{ctx.base_url}/app/delete", json=delete_data)
        body = resp.json()
        assert body.get("code") == 0 or body.get("data") is True, f"删除失败: {body}"

    def test_delete_not_exist(self, ctx, logged_in):
        """异常：删除不存在的应用"""
        delete_data = {"id": 99999999}
        resp = ctx.session.post(f"{ctx.base_url}/app/delete", json=delete_data)
        body = resp.json()
        assert body.get("code") != 0, "删除不存在的应用应返回错误"
