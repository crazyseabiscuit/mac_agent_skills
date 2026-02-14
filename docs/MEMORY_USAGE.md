# 长期记忆功能使用说明

## 概述

该项目已集成了长期和短期记忆系统，允许 AI 助手在多个会话中记住用户信息、偏好和对话历史。

## 核心特性

### 1. 长期记忆（Persistent Memory）
- **存储位置**: `.memories/` 目录
- **持久化**: 跨越多个会话和线程
- **包含内容**:
  - `preferences.json` - 用户偏好设置
  - `context.json` - 上下文信息
  - `history.json` - 完整对话历史

### 2. 短期记忆（Short-term Memory）
- **存储位置**: 内存中
- **生命周期**: 当前会话内
- **用途**: 快速访问当前对话的消息

## 使用方法

### 编程使用

#### 基础初始化
```python
from glm_langchain_client import GLMClient

# 启用长期记忆（默认启用）
client = GLMClient(
    api_key="your-api-key",
    enable_memory=True,
    memory_dir=".memories"  # 可选，指定记忆存储目录
)
```

#### 保存用户偏好
```python
# 保存偏好到长期记忆
client.memory.save_preference("language", "Chinese")
client.memory.save_preference("response_length", "concise")

# 后续会话可以读取
pref = client.memory.get_preference("language")
```

#### 保存上下文信息
```python
# 保存用户相关信息
client.memory.save_context("user_name", "Alice")
client.memory.save_context("project_name", "AI Assistant")

# 读取所有上下文
all_context = client.memory.get_all_context()
```

#### 访问对话历史
```python
# 获取最近100条消息
history = client.memory.get_history(limit=100)

# 获取所有历史
all_history = client.memory.get_history()
```

#### 导入/导出记忆
```python
# 导出所有长期记忆
client.memory.export_long_term_memory("backup.json")

# 导入记忆
client.memory.import_long_term_memory("backup.json")
```

### 终端交互使用

在 `glm_terminal.py` 中使用以下命令：

#### 保存偏好
```
> save-pref language Chinese
Preference saved: language = Chinese

> save-pref timezone Asia/Shanghai
Preference saved: timezone = Asia/Shanghai
```

#### 查看长期记忆
```
> show-memory
## Your Long-Term Memory

### User Preferences
- language: Chinese
- timezone: Asia/Shanghai
- updated_at: 2024-01-15T10:30:00Z

### Context Information
- user_name: Alice
- project_name: AI Assistant
- updated_at: 2024-01-15T10:30:00Z

### Conversation History
- Total messages: 45
```

#### 清除当前会话
```
> clear
Chat history cleared.
```

## 工作原理

### 记忆注入流程

当调用 `invoke()` 方法时：

1. **读取记忆**: 从 `.memories/` 目录加载所有长期数据
2. **生成摘要**: 构建可读的记忆摘要文本
3. **注入系统提示**: 将记忆摘要添加到 SystemMessage
4. **发送请求**: 连同技能上下文一起发送给 LLM
5. **保存历史**: LLM 响应后，自动保存到长期历史记忆

```
User Input
    ↓
Load Long-term Memory
    ↓
Create Memory Summary
    ↓
Inject into System Prompt
    ↓
Send to GLM Model
    ↓
Save to History
    ↓
Return Response
```

## 记忆数据结构

### preferences.json
```json
{
  "language": "Chinese",
  "timezone": "Asia/Shanghai",
  "response_length": "concise",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### context.json
```json
{
  "user_name": "Alice",
  "project_name": "AI Assistant",
  "department": "R&D",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### history.json
```json
[
  {
    "timestamp": "2024-01-15T10:00:00Z",
    "role": "user",
    "content": "Hello, what's your name?",
    "metadata": {}
  },
  {
    "timestamp": "2024-01-15T10:00:05Z",
    "role": "assistant",
    "content": "I'm an AI assistant...",
    "metadata": {}
  }
]
```

## 最佳实践

### 1. 定期备份
```python
# 定期导出记忆到备份文件
import shutil
from datetime import datetime

backup_file = f"memory_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
client.memory.export_long_term_memory(backup_file)
```

### 2. 清理旧数据
```python
# 在系统初始化时检查历史大小
history = client.memory.get_history()
if len(history) > 10000:
    # 实现清理逻辑
    pass
```

### 3. 隐私保护
- 敏感信息不应保存到偏好或上下文
- 确保 `.memories/` 目录访问权限设置正确
- 考虑加密存储敏感数据

### 4. 结合系统提示
```python
system_prompt = """You are a helpful assistant.
Remember the user's preferences and context to personalize your responses.
Use the long-term memory information provided to understand the user better."""
```

## 禁用长期记忆

如果需要禁用长期记忆（仅使用短期会话记忆）：

```python
client = GLMClient(
    api_key="your-api-key",
    enable_memory=False  # 禁用长期记忆
)
```

## 故障排除

### 记忆文件权限问题
```bash
# 修复 .memories/ 目录权限
chmod 755 .memories/
chmod 644 .memories/*.json
```

### 恢复默认状态
```bash
# 删除所有长期记忆
rm -rf .memories/
```

## 高级用法

### 自定义记忆目录
```python
client = GLMClient(
    api_key="your-api-key",
    memory_dir="/path/to/custom/memory"
)
```

### 在多用户环境中使用
```python
# 为每个用户维护独立的记忆
from pathlib import Path

user_id = "user123"
memory_dir = Path(".memories") / user_id
client = GLMClient(
    api_key="your-api-key",
    memory_dir=str(memory_dir)
)
```

## 相关文件

- `memory_manager.py` - 记忆管理核心模块
- `glm_langchain_client.py` - GLM 客户端（已集成记忆）
- `glm_terminal.py` - 终端交互（支持记忆命令）
