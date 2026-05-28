# AI 零代码应用生成平台

基于 **Spring Boot 3 + LangChain4j + LangGraph4j + Vue 3** 的企业级 AI 代码生成平台，支持通过自然语言描述自动生成完整的前端应用。

## 项目介绍

本平台以 **AI 开发实战 + 后端架构设计** 为核心，集成 AI 智能体（Agent）与 AI 工作流（Workflow）技术，实现了从需求描述到可运行应用的完整链路。

### 4 大核心能力

1. **智能代码生成**：用户输入需求描述，AI 自动分析并选择合适的生成策略，通过工具调用生成代码文件，采用流式输出让用户实时看到 AI 的执行过程。

2. **可视化编辑**：生成的应用实时展示，支持编辑模式，可自由选择网页元素并通过 AI 对话快速修改页面。

3. **一键部署分享**：生成的应用可一键部署到云端并自动截取封面图，获得可访问的地址进行分享，同时支持完整项目源码下载。

4. **企业级管理**：提供用户管理、应用管理、系统监控、业务指标监控等后台功能，管理员可设置精选应用、监控 AI 调用情况和系统性能。

## 技术栈

### 后端
- **基础框架**: Spring Boot 3.5.4, Java 21
- **AI 框架**: LangChain4j 1.1.0, LangGraph4j 1.6.0
- **数据库**: MySQL, MyBatis-Flex
- **缓存**: Redis + Caffeine 多级缓存
- **流式处理**: Project Reactor (Flux), SSE
- **监控**: Prometheus + Grafana + Actuator
- **对象存储**: 腾讯云 COS

### 前端
- Vue 3 (Composition API)
- Vite
- Vue Router 4

## 项目架构

### AI Agent 架构（LangChain4j）

```
用户输入 → AI 路由服务 → 选择生成类型 (HTML / MultiFile / Vue)
                       → AI 代码生成器 (Tool Calling)
                         → FileWriteTool / FileReadTool / FileModifyTool / FileDeleteTool
                       → 代码解析器 → 代码保存器 → 项目构建
```

### AI 工作流（LangGraph4j）

```
Start → 图片收集 → Prompt增强 → 智能路由 → 代码生成 → 质量检查
                                                         ↓
                                             通过 → 项目构建 → End
                                             不通过 → 重新生成 (循环)
```

## 功能模块

| 模块 | 说明 |
|------|------|
| AI 代码生成 | 支持 HTML / 多文件 / Vue 项目三种生成模式 |
| 对话记忆 | Redis 持久化 + Caffeine 本地缓存，多租户隔离 |
| 安全防护 | Prompt 注入检测、敏感词过滤、API 限流 |
| 用户系统 | 注册登录、权限管理、AOP 拦截 |
| 应用管理 | 创建、编辑、删除、精选应用 |
| 系统监控 | Prometheus 指标、Grafana 仪表盘 |
| 一键部署 | 自动构建并部署到云端，支持代码下载 |

## 核心依赖

- [LangChain4j](https://github.com/langchain4j/langchain4j) - Java 版 LangChain，AI 智能体框架
- [LangGraph4j](https://github.com/bsorrentino/langgraph4j) - Java 版 LangGraph，AI 工作流框架
- [MyBatis-Flex](https://github.com/mybatis-flex/mybatis-flex) - 灵活的 MyBatis 增强框架
- [Knife4j](https://github.com/xiaoymin/knife4j) - Swagger 文档增强

## 项目结构

```
├── src/main/java/com/aicode/platform/
│   ├── ai/              # AI 核心服务
│   │   ├── guardrail/   # Prompt 安全护轨
│   │   ├── model/       # AI 消息模型
│   │   └── tools/       # AI 工具（文件读写等）
│   ├── config/          # 配置（AI 模型、缓存等）
│   ├── controller/      # REST API 控制器
│   ├── core/            # 代码生成核心门面
│   │   ├── builder/     # Vue 项目构建器
│   │   ├── handler/     # 流式处理器
│   │   ├── parser/      # 代码解析器
│   │   └── saver/       # 代码保存器
│   ├── langgraph4j/     # AI 工作流实现
│   └── service/         # 业务服务层
```

## 代码生成类型

| 类型 | 适用场景 | 技术栈 |
|------|----------|--------|
| HTML | 简单静态页面 | 单 HTML 文件（内联 CSS/JS） |
| MULTI_FILE | 多文件静态页面 | 分离 HTML、CSS、JS |
| VUE_PROJECT | 复杂前端项目 | Vue 3 + Vite + Vue Router |

## 快速开始

### 前置要求

- JDK 21+
- Maven 3.8+
- MySQL 8.0+
- Redis 7.0+
- AI API Key（兼容 OpenAI 协议的模型）

### 配置

1. 复制 `application-prod-sample.yml` 为 `application-prod.yml`
2. 配置数据库连接、Redis 连接、AI API Key
3. 执行 `sql/create_table.sql` 初始化数据库

### 启动

```bash
mvn spring-boot:run -Dspring.profiles.active=prod
```

---

> 本项目为个人学习项目，基于开源技术栈构建。
