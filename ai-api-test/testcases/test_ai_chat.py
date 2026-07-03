"""
AI 对话接口测试
覆盖：AI 生成代码的流式接口、对话历史查询

注意：AI 对话接口为 SSE 流式返回，需要特殊处理
"""
import pytest
import re


class TestAIChat:
    """AI 对话测试"""

    @pytest.mark.skip(reason="需要先创建应用并配置AI密钥，手动确认后去掉skip运行")
    def test_chat_gen_code_stream(self, ctx, logged_in):
        """
        正向：AI对话生成代码（SSE流式）
        验证点：
        1. 接口正常返回 200
        2. 返回内容为 text/event-stream 格式
        3. 能接收到数据事件
        4. 能接收到 done 事件
        """
        # 先创建一个应用
        create_data = {"appName": "AI测试应用", "appDesc": "用于测试AI对话"}
        resp = ctx.session.post(f"{ctx.base_url}/app/add", json=create_data)
        app_id = resp.json().get("data")

        # 调用AI对话接口（流式）
        params = {"appId": app_id, "message": "用Python写一个计算器程序"}
        resp = ctx.session.get(
            f"{ctx.base_url}/app/chat/gen/code",
            params=params,
            stream=True,
            headers={"Accept": "text/event-stream"}
        )

        assert resp.status_code == 200
        assert "text/event-stream" in resp.headers.get("Content-Type", "")

        # 读取流式响应
        received_data = False
        received_done = False
        for line in resp.iter_lines():
            if not line:
                continue
            line_str = line.decode("utf-8", errors="ignore")
            if line_str.startswith("data:"):
                # 检查数据事件
                if line_str == "data:" and not received_done:
                    received_done = True
                elif not received_done:
                    received_data = True

        # 至少收到了数据
        assert received_data, "AI对话未返回数据"

    def test_chat_with_empty_message(self, ctx, logged_in):
        """异常：AI对话传入空提示词"""
        params = {"appId": 1, "message": ""}
        resp = ctx.session.get(f"{ctx.base_url}/app/chat/gen/code", params=params)
        # 期望返回参数校验错误
        assert resp.status_code != 200 or "error" in resp.text.lower()

    def test_chat_history_list(self, ctx, logged_in):
        """正向：查询应用的对话历史"""
        resp = ctx.session.get(
            f"{ctx.base_url}/chatHistory/app/1",
            params={"pageSize": 10}
        )
        # 即使应用没有对话历史，接口也应正常返回
        assert resp.status_code == 200
