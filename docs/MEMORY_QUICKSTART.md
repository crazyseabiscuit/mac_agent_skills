# 长期和短期记忆快速启动指南

## 🎯 新增功能概览

已成功为你的项目添加了完整的长期和短期记忆系统，支持：

✅ **长期记忆** - 跨会话持久化存储  
✅ **短期记忆** - 当前会话内快速访问  
✅ **自动注入** - 记忆信息自动添加到系统提示  
✅ **导入导出** - 备份和恢复记忆数据  

---

## 📦 新增文件

| 文件 | 说明 |
|------|------|
| `memory_manager.py` | 记忆管理核心模块 |
| `MEMORY_USAGE.md` | 详细使用文档 |
| `test_memory.py` | 功能演示脚本 |

## ⚡ 已修改的文件

- `glm_langchain_client.py` - 集成记忆管理
- `glm_terminal.py` - 添加记忆命令

---

## 🚀 快速开始

### 1. 在代码中使用

```python
from glm_langchain_client import GLMClient

# 自动启用记忆
client = GLMClient(api_key="your-key")

# 保存用户偏好
client.memory.save_preference("language", "Chinese")

# 保存上下文
client.memory.save_context("user_name", "Alice")

# 使用 invoke() 时，记忆会自动注入系统提示
response = client.invoke(messages)
```

### 2. 在终端中使用

```bash
python glm_terminal.py

# 终端命令：
> save-pref language Chinese
> save-pref timezone Asia/Shanghai
> show-memory          # 查看所有记忆
> clear               # 清除当前会话
```

### 3. 运行演示

```bash
python test_memory.py
```

---

## 📂 记忆文件结构

```
.memories/
├── preferences.json    # 用户偏好 {language: "Chinese", ...}
├── context.json       # 上下文信息 {user_name: "Alice", ...}
└── history.json       # 对话历史 [{role, content, timestamp}, ...]
```

---

## 🔑 核心 API

### 保存和读取

```python
# 偏好
client.memory.save_preference("key", "value")
value = client.memory.get_preference("key")

# 上下文
client.memory.save_context("key", "value")
value = client.memory.get_context("key")
all_context = client.memory.get_all_context()

# 历史
client.memory.add_to_history("user", "message content")
history = client.memory.get_history(limit=100)
```

### 导入导出

```python
# 导出
client.memory.export_long_term_memory("backup.json")

# 导入
client.memory.import_long_term_memory("backup.json")
```

### 获取记忆摘要

```python
# 获取格式化的记忆摘要（用于系统提示）
summary = client.memory.get_memory_summary()
print(summary)
```

---

## 💾 禁用记忆（可选）

如果需要禁用长期记忆：

```python
client = GLMClient(
    api_key="your-key",
    enable_memory=False
)
```

---

## 🛠️ 高级用法

### 自定义记忆目录

```python
client = GLMClient(
    api_key="your-key",
    memory_dir="/custom/path"
)
```

### 多用户环境

```python
from pathlib import Path

# 每个用户独立记忆
memory_dir = Path(".memories") / user_id
client = GLMClient(api_key="your-key", memory_dir=str(memory_dir))
```

### 定期备份

```python
from datetime import datetime

backup_file = f"backup_{datetime.now().strftime('%Y%m%d')}.json"
client.memory.export_long_term_memory(backup_file)
```

---

## 📖 详细文档

查看 `MEMORY_USAGE.md` 获取：
- 完整的 API 参考
- 数据结构说明
- 最佳实践指南
- 故障排除

---

## 🧪 验证安装

```bash
# 运行测试脚本
python test_memory.py

# 预期输出：Demo Complete! ✓
```

---

## 📝 工作原理

```
User Input
   ↓
📖 加载长期记忆 (.memories/)
   ↓
🎯 生成记忆摘要
   ↓
💬 注入系统提示
   ↓
🤖 发送给 GLM 模型
   ↓
💾 保存响应到历史记录
   ↓
✨ 返回回复
```

---

## 🎓 使用场景

### 用户偏好记忆
```python
client.memory.save_preference("response_style", "concise")
# 后续所有回复都会参考此偏好
```

### 项目上下文
```python
client.memory.save_context("project_status", "In Development")
client.memory.save_context("team_size", "5 people")
# AI 会理解项目背景，提供更贴切的帮助
```

### 长期学习
```
会话 1: 用户讲解了项目架构
      → 保存到历史记忆

会话 2: 用户问"上次说的架构怎样？"
      → AI 从历史中读取并回答
```

---

## ⚠️ 注意事项

1. **隐私**: 不要保存敏感个人信息到记忆中
2. **大小**: 定期清理旧历史以管理存储空间
3. **权限**: 确保 `.memories/` 目录有正确的访问权限
4. **备份**: 重要数据定期备份

---

## 🆘 常见问题

**Q: 如何清除所有记忆？**  
A: `rm -rf .memories/`

**Q: 能否为不同用户设置不同记忆？**  
A: 是的，创建不同的 `memory_dir` 即可

**Q: 记忆会影响性能吗？**  
A: 最小化影响，只在需要时加载和序列化

**Q: 能否加密记忆数据？**  
A: 当前不支持，但可自行扩展 `memory_manager.py`

---

## 🔗 相关文件

- `memory_manager.py` - 核心实现
- `glm_langchain_client.py` - GLM 集成
- `glm_terminal.py` - 终端交互
- `MEMORY_USAGE.md` - 完整文档
- `test_memory.py` - 功能演示

---

**开始使用吧！** 🎉
