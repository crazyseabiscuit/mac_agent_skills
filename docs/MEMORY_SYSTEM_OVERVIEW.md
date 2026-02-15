# Memory Manager System Overview

## 概述 (Overview)

项目的内存管理系统由三个核心部分组成，实现了智能对话代理的长期和短期记忆功能。

The project's memory manager system consists of three core components that provide persistent and session-based memory for the AI agent.

---

## 系统架构 (System Architecture)

```
┌─────────────────────────────────────────────────────────────┐
│                    GLMClient (Main)                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ✓ enable_memory=True (默认/default)                        │
│  ✓ Automatically initializes MemoryManager                   │
│  ✓ Auto-injects memory into system prompts                   │
│  ✓ Auto-saves conversation to long-term history             │
│                                                               │
└─────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│                   MemoryManager                              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📋 Short-Term Memory (Session)                              │
│     └─ messages[]  - Current session conversation history    │
│     └─ context{}   - Session-specific context data           │
│     └─ created_at  - Session start timestamp                 │
│                                                               │
│  💾 Long-Term Memory (Persistent Files)                      │
│     └─ preferences.json   - User preferences                 │
│     └─ context.json       - Persistent context               │
│     └─ history.json       - Complete conversation history    │
│                                                               │
│  🔄 Auto Injection                                           │
│     └─ get_memory_summary() - Formats memory for prompts     │
│                                                               │
└─────────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│              Storage: .memories/ Directory                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  .memories/                                                  │
│  ├─ preferences.json     (User preferences)                 │
│  ├─ context.json         (Persistent context)               │
│  └─ history.json         (Conversation history)             │
│                                                               │
│  [Auto-created on first use]                                │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 核心使用流程 (Core Usage Flow)

### 1️⃣ 初始化 (Initialization)

```python
# 方式 1: 默认启用内存 (Default - Memory Enabled)
client = GLMClient(
    api_key=os.getenv("ZHIPUAI_API_KEY"),
    enable_memory=True  # 默认值 (default)
)

# 方式 2: 禁用内存 (Disable Memory)
client = GLMClient(
    api_key=os.getenv("ZHIPUAI_API_KEY"),
    enable_memory=False
)

# 方式 3: 自定义内存存储位置 (Custom Memory Directory)
client = GLMClient(
    api_key=os.getenv("ZHIPUAI_API_KEY"),
    memory_dir="/custom/path/.memories"
)
```

### 2️⃣ 保存用户偏好 (Save Preferences)

```python
# 保存用户语言偏好
client.memory.save_preference("language", "Chinese")
client.memory.save_preference("style", "concise")
client.memory.save_preference("timezone", "Asia/Shanghai")

# 检索偏好
lang = client.memory.get_preference("language", "English")
# lang = "Chinese"
```

### 3️⃣ 保存上下文信息 (Save Context)

```python
# 保存项目相关上下文
client.memory.save_context("user_name", "Alice")
client.memory.save_context("project", "AI Assistant")
client.memory.save_context("team_size", 3)

# 检索上下文
name = client.memory.get_context("user_name")
# name = "Alice"
```

### 4️⃣ 对话时自动注入内存 (Auto-Injection During Conversation)

```python
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Who am I and what am I working on?")
]

# invoke() 自动：
# 1. 加载长期记忆内容
# 2. 生成内存摘要
# 3. 注入到系统提示词中
# 4. 发送消息给LLM
# 5. 保存用户/助手消息到历史记录
response = client.invoke(messages)
# 助手会根据保存的用户名和项目信息回答问题
```

### 5️⃣ 查看和管理内存 (View & Manage Memory)

```python
# 查看内存摘要
summary = client.memory.get_memory_summary()
print(summary)

# 输出示例：
# ## Your Long-Term Memory
#
# ### User Preferences
# - language: Chinese
# - style: concise
# - timezone: Asia/Shanghai
#
# ### Context Information
# - user_name: Alice
# - project: AI Assistant
# - team_size: 3
#
# ### Conversation History
# Total messages: 15

# 获取短期消息
short_term = client.memory.get_short_term_messages()

# 获取完整对话历史
history = client.memory.get_history()

# 导出内存备份
client.memory.export_long_term_memory("memory_backup.json")

# 导入内存备份
client.memory.import_long_term_memory("memory_backup.json")

# 清除所有内存
client.memory.clear_all_memory()
```

---

## 当前项目状态 (Current Project Status)

### 集成点 (Integration Points)

| 组件 | 集成方式 | 状态 |
|------|---------|------|
| **glm_langchain_client.py** | 主要实现，包含MemoryManager初始化和自动注入 | ✅ 活跃 |
| **memory_manager.py** | 核心内存管理类 | ✅ 实现完整 |
| **example_memory_usage.py** | 使用示例脚本 | ✅ 可运行 |
| **tests/test_memory.py** | 单元测试覆盖 | ✅ 13个测试 |
| **glm_terminal.py** | 终端命令集成 | ⏳ 部分支持 |

### 存储状态 (Storage Status)

```
.memories/
├─ history.json          (主要使用)
│  └─ 8+条对话记录
│  └─ 最新更新: 2026-02-14T11:37:28
│
├─ preferences.json      (未创建 - 需要手动调用)
│  └─ 等待: save_preference() 调用
│
└─ context.json          (未创建 - 需要手动调用)
   └─ 等待: save_context() 调用
```

---

## 关键功能 (Key Features)

### 🔐 隐私和安全

- ✅ 所有内存存储在本地 `.memories/` 目录
- ✅ 绝不上传到远程服务器
- ✅ 可通过 `.gitignore` 从版本控制中排除
- ✅ 支持导出/导入备份

### ⚡ 自动化

- ✅ 自动初始化 (如果 `enable_memory=True`)
- ✅ 自动注入内存到系统提示词
- ✅ 自动保存对话到历史记录
- ✅ 自动格式化内存摘要

### 🛠️ 可配置性

- ✅ 可启用/禁用内存系统
- ✅ 自定义内存存储位置
- ✅ 细粒度的内存操作

### 📊 功能完整性

- ✅ 短期内存 (会话级)
- ✅ 长期内存 (持久化)
- ✅ 用户偏好管理
- ✅ 上下文管理
- ✅ 对话历史
- ✅ 内存导出/导入
- ✅ 内存清除

---

## 实现细节 (Implementation Details)

### GLMClient 中的内存流程

```python
# 初始化
def __init__(self, enable_memory=True, memory_dir=None):
    if enable_memory:
        self.memory = MemoryManager(memory_dir=memory_dir)
    else:
        self.memory = None

# 发送消息时
def invoke(self, messages):
    # 1. 加载内存摘要
    if self.memory:
        memory_summary = self.memory.get_memory_summary()
        # 2. 注入到系统消息
        for i, msg in enumerate(messages):
            if isinstance(msg, SystemMessage):
                messages[i] = SystemMessage(
                    content=f"{msg.content}\n\n{memory_summary}"
                )
    
    # 3. 调用LLM
    response = self.chat.invoke(messages)
    
    # 4. 保存到历史
    if self.memory:
        self.memory.add_to_history(
            messages[-1],  # 用户消息
            response       # AI响应
        )
    
    return response
```

### 文件存储格式

**preferences.json:**
```json
{
  "language": "Chinese",
  "style": "concise",
  "timezone": "Asia/Shanghai",
  "updated_at": "2026-02-14T11:18:00.000000"
}
```

**context.json:**
```json
{
  "user_name": "Alice",
  "project": "AI Assistant",
  "team_size": 3,
  "updated_at": "2026-02-14T11:18:00.000000"
}
```

**history.json:**
```json
[
  {
    "timestamp": "2026-02-14T11:18:35.128205",
    "role": "user",
    "content": "User message here"
  },
  {
    "timestamp": "2026-02-14T11:18:35.129145",
    "role": "assistant",
    "content": "Assistant response here"
  }
]
```

---

## 使用示例 (Usage Examples)

### 示例 1: 基本使用

```python
from glm_langchain_client import GLMClient
from langchain_core.messages import HumanMessage, SystemMessage
import os

# 初始化客户端（自动启用内存）
client = GLMClient(api_key=os.getenv("ZHIPUAI_API_KEY"))

# 保存用户信息
client.memory.save_preference("language", "Chinese")
client.memory.save_context("name", "Bob")

# 对话 - 内存会自动注入
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is my name?")
]
response = client.invoke(messages)
# 助手会回答: "Your name is Bob"
```

### 示例 2: 多会话持久化

```python
# 会话 1
client1 = GLMClient()
client1.memory.save_preference("theme", "dark")

# 会话 2 - 同一台电脑，相同 .memories 目录
client2 = GLMClient()
theme = client2.memory.get_preference("theme")
# theme = "dark" ✅ 从会话 1 保存的数据中检索
```

### 示例 3: 跳过内存系统

```python
# 某些特殊场景可能需要禁用内存
client = GLMClient(
    enable_memory=False  # 禁用内存
)

# 此时 client.memory = None
# 不会有自动注入，也不会保存历史
```

---

## 终端集成 (Terminal Integration)

项目支持通过终端命令管理内存：

```bash
# 保存用户偏好 (Save preference)
glm_terminal.py save-pref <key> <value>

# 显示内存摘要 (Show memory summary)
glm_terminal.py show-memory
```

---

## 最佳实践 (Best Practices)

### ✅ 应该做

1. **对于重要信息使用 `save_context()`**
   ```python
   client.memory.save_context("api_endpoint", "https://api.example.com")
   ```

2. **对于用户偏好使用 `save_preference()`**
   ```python
   client.memory.save_preference("response_format", "JSON")
   ```

3. **定期导出备份**
   ```python
   client.memory.export_long_term_memory("backup.json")
   ```

4. **在关键操作前检查内存**
   ```python
   if client.memory:
       summary = client.memory.get_memory_summary()
   ```

### ❌ 不应该做

1. **不要直接编辑 `.memories/` 中的JSON文件**
   - 使用 API 方法而不是手动编辑

2. **不要在版本控制中提交 `.memories/` 目录**
   - 已由 `.gitignore` 处理

3. **不要在 `.memories/` 中存储敏感凭证**
   - 使用 `config.properties` 代替

4. **不要假设内存总是可用**
   - 总是检查 `if self.memory` 再使用

---

## 常见问题 (FAQ)

### Q: 内存何时自动保存？
**A:** 在每次 `invoke()` 调用后，用户消息和AI响应都会自动保存到 `history.json`。

### Q: 如何跨多个项目共享内存？
**A:** 初始化时传递相同的 `memory_dir` 参数：
```python
client = GLMClient(memory_dir="/shared/.memories")
```

### Q: 内存会占用多少空间？
**A:** 每条消息约 300-500 字节，1000 条消息约 300-500 KB。

### Q: 如何在生产环境中禁用内存？
**A:** 设置 `enable_memory=False` 或从环境变量控制。

### Q: 如何处理数据隐私问题？
**A:** 
- 内存完全存储在本地
- 定期备份和清理
- 使用 `clear_all_memory()` 彻底删除

---

## 相关文档 (Related Documentation)

- 📖 [MEMORY_USAGE.md](./MEMORY_USAGE.md) - 详细 API 参考
- 🚀 [MEMORY_QUICKSTART.md](./MEMORY_QUICKSTART.md) - 5分钟快速入门
- 🔧 [MEMORY_IMPLEMENTATION_SUMMARY.md](./MEMORY_IMPLEMENTATION_SUMMARY.md) - 技术实现细节

---

**最后更新**: 2026-02-14  
**状态**: ✅ 完全集成，生产就绪
