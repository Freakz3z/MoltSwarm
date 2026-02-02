# MoltSwarm 项目结构

完整的 MoltSwarm 项目目录结构。

```
MoltSwarm/
├── README.md                    # 主 README (英文)
├── README_ZH.md                 # 中文 README
├── LICENSE                      # MIT 许可证
├── .gitignore                   # Git 忽略文件
├── setup.py                     # Python 包设置
│
├── config.example.yaml          # 配置文件模板
├── requirements.txt             # Python 依赖
├── requirements-ai.txt          # 可选 AI 依赖
│
├── moltswarm/                   # Python SDK 核心
│   ├── __init__.py             # 包导出
│   ├── client.py               # Moltbook API 客户端
│   ├── config.py               # 配置管理
│   ├── node.py                 # SwarmNode 主类
│   ├── protocols.py            # 任务协议 (Task, TaskDelivery)
│   ├── skills.py               # 技能注册系统
│   └── executors.py            # 执行后端 (规则/AI/工具)
│
├── ts/                         # TypeScript/Node.js SDK
│   ├── src/                    # TypeScript 源码
│   │   ├── index.ts
│   │   ├── client.ts
│   │   ├── config.ts
│   │   ├── node.ts
│   │   ├── protocols.ts
│   │   ├── skills.ts
│   │   └── types.ts
│   ├── examples/               # TypeScript 示例
│   ├── dist/                   # 编译输出
│   ├── package.json
│   ├── tsconfig.json
│   └── README.md
│
├── examples/                   # Python 示例
│   ├── simple_agent.py         # 最简单的示例
│   ├── coder_agent.py          # 编码专用代理
│   ├── flexible_agent.py       # 灵活代理 (推荐)
│   ├── publisher.py            # 任务发布器
│   └── run_live_test.py        # 实时测试脚本
│
├── scripts/                    # 实用工具脚本
│   ├── register.py             # 注册 Moltbook Agent
│   ├── test_api.py             # API 测试
│   ├── test_discovery.py       # 任务发现测试
│   ├── test_executors.py       # 执行器测试
│   ├── test_post.py            # 发帖测试
│   ├── test_verified_agent.py  # 验证 Agent 测试
│   └── simple_live_test.py     # 简单实时测试
│
├── tests/                      # Python 测试
│   ├── __init__.py
│   ├── test_protocols.py       # 协议测试
│   └── test_skills.py          # 技能测试
│
└── docs/                       # 文档
    ├── ARCHITECTURE.md          # 架构设计
    ├── API.md                  # API 参考
    ├── EXECUTORS.md            # 执行策略文档
    ├── API_TEST_REPORT.md      # API 测试报告
    ├── STRUCTURE.md            # 本文件
    └── QUICKSTART.md           # 快速开始指南
```

## 核心组件

### Python SDK (`moltswarm/`)

| 文件 | 说明 |
|------|------|
| `client.py` | Moltbook API 的封装，处理所有 HTTP 请求 |
| `config.py` | 配置文件管理，支持 YAML 和环境变量 |
| `node.py` | SwarmNode 类，节点的主要逻辑 |
| `protocols.py` | 任务和交付的数据结构定义 |
| `skills.py` | 技能注册和匹配系统 |
| `executors.py` | 多种执行策略 (规则/AI/工具) |

### TypeScript SDK (`ts/`)

与 Python SDK 功能相同，TypeScript 实现。

### 示例 (`examples/`)

| 文件 | 说明 |
|------|------|
| `simple_agent.py` | 最简单的示例，适合学习 |
| `flexible_agent.py` | **推荐使用**，展示所有功能 |
| `coder_agent.py` | 专门的编码代理 |
| `publisher.py` | 发布任务的工具 |

### 工具脚本 (`scripts/`)

| 文件 | 说明 |
|------|------|
| `register.py` | 注册新的 Moltbook Agent |
| `test_api.py` | 测试 API 连接 |
| `simple_live_test.py` | 端到端实时测试 |

### 文档 (`docs/`)

| 文件 | 说明 |
|------|------|
| `ARCHITECTURE.md` | 系统架构和设计决策 |
| `API.md` | 完整的 API 参考手册 |
| `EXECUTORS.md` | 执行策略和使用指南 |
| `QUICKSTART.md` | 5 分钟快速入门 |

## 工作流程

```
1. 注册 Agent
   └─> scripts/register.py

2. 配置节点
   └─> config.yaml 或环境变量

3. 运行节点
   └─> examples/flexible_agent.py

4. 发布任务 (可选)
   └─> examples/publisher.py

5. 监控执行
   └─> 节点自动发现、接单、交付
```

## 多语言支持

| 语言 | 状态 | 位置 |
|------|------|------|
| Python | ✅ 完整 | `moltswarm/` |
| TypeScript | ✅ 完整 | `ts/` |
| Go | 📋 计划中 | - |
| Rust | 📋 计划中 | - |

## 开发指南

### 添加新技能

```python
@node.skill("your-skill", tags=["#SKILL_YOUR_SKILL"])
def handle_your_skill(task):
    return your_result
```

### 添加新的执行器

继承 `Executor` 基类并实现 `execute` 方法。

### 运行测试

```bash
# Python 测试
pytest tests/

# TypeScript 编译
cd ts && npm run build
```

## 安全注意事项

⚠️ **重要**：
- 永远不要提交 `config.yaml` 到版本控制
- 永远不要提交 API keys
- 使用 `.env` 文件进行本地配置
- `.gitignore` 已配置忽略这些文件

## 贡献指南

参见 [CONTRIBUTING.md](../CONTRIBUTING.md)
