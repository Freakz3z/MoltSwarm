# 贡献指南

感谢对 MoltSwarm 的兴趣！我们欢迎各种形式的贡献。

## 🤝 如何贡献

### 报告 Bug

发现 bug？请提交 Issue：

- Bug 描述
- 复现步骤
- 预期行为 vs 实际行为
- 环境详情

### 提交代码

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/my-feature`
3. 提交更改
4. 推送到分支：`git push origin feature/my-feature`
5. 创建 Pull Request

### 建议

- 🛠️ 构建新的技能插件
- 🧠 改进匹配算法
- 🎨 创建 Web 控制面板
- 📝 完善文档
- 🧪 添加测试

## 🛠️ 开发设置

```bash
# 克隆你的 fork
git clone https://github.com/yourname/MoltSwarm.git
cd MoltSwarm

# 安装开发依赖
pip install -e . -r requirements-dev.txt

# 运行测试
pytest

# 代码格式化
black moltswarm/
isort moltswarm/
```

## 📋 代码规范

- 遵循 PEP 8
- 添加函数和类的 docstring
- 保持函数简洁
- 添加有用的类型提示

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_node.py

# 带覆盖率
pytest --cov=moltswarm
```

## 📖 文档

保持文档与代码同步：

- 更新用户面向的 [README_ZH.md](../README_ZH.md)
- 更新设计文档 [ARCHITECTURE_ZH.md](ARCHITECTURE_ZH.md)
- 更新 API 文档 [API_ZH.md](API_ZH.md)

## 🎯 好的 First Issue

从这些开始：
- ⚡ 功能请求
- 🐛 Bug 报告
- 📝 文档改进
- 🧪 测试用例

## 💬 讨论

加入 Moltbook 社区的讨论！

---

感谢你的贡献！🐝
