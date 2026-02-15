# Preference 和 Memory 的使用时机

## 📝 概述

**Preference** 和 **Context** 是长期记忆的两种类型，它们在每次 AI 对话时自动注入到系统提示中。

## 🔄 使用流程

### 1. **保存时机**

#### 手动保存
```python
# 保存用户偏好
client.memory.save_preference("language", "Chinese")
client.memory.save_preference("content_type", "movies")

# 保存用户上下文
client.memory.save_context("project", "AI Assistant")
client.memory.save_context("primary_interest", "电影推荐")
```

#### AI 自动保存（glm_terminal.py）
```
用户: 我喜欢看电影
AI: 好的！
    SAVE_MEMORY: content_type=movies
    [Saved preference: content_type=movies]
```

### 2. **使用时机** ⭐

**每次调用 `client.invoke()` 时自动使用！**

```python
# glm_langchain_client.py 的 invoke() 方法
def invoke(self, messages):
    # 1. 注入技能信息
    # ...
    
    # 2. 注入长期记忆 ⭐⭐⭐
    if self.memory and messages:
        memory_summary = self.memory.get_memory_summary()  # 读取所有 preference 和 context
        if memory_summary.strip():
            for i, msg in enumerate(messages):
                if isinstance(msg, SystemMessage):
                    # 将记忆添加到系统提示中
                    messages[i] = SystemMessage(content=f"{msg.content}\n\n{memory_summary}")
                    break
    
    # 3. 发送给 AI
    response = self.chat.invoke(messages)
    
    # 4. 保存对话历史
    if self.memory:
        self.memory.add_to_history("user", user_message)
        self.memory.add_to_history("assistant", response)
    
    return response
```

### 3. **注入的内容格式**

AI 收到的系统提示会包含：

```
## Your Long-Term Memory

### User Preferences
- language: Chinese
- content_type: movies_and_tv
- region_preference: china_mainland

### Context Information
- project: AI Assistant
- primary_interest: 电影推荐
- interaction_style: 简短请求

### Conversation History
You have 50 messages in history.
```

## 🎯 实际使用场景

### 场景 1：用户偏好记忆

```python
# 第一次对话
用户: "我喜欢看电影"
AI: [保存] preference: content_type=movies

# 第二次对话（几天后）
用户: "推荐一些内容"
AI: [读取 preference] "根据您喜欢看电影的偏好，推荐..."
```

### 场景 2：项目上下文记忆

```python
# 第一次对话
用户: "我在做一个 AI 助手项目"
AI: [保存] context: project=AI_Assistant

# 第二次对话
用户: "帮我优化代码"
AI: [读取 context] "针对您的 AI 助手项目，建议..."
```

### 场景 3：glm_terminal 中的使用

```bash
# 启动 terminal
$ python glm_terminal.py

You: 我喜欢看杨幂的电视剧
Assistant: [AI 自动触发]
          SAVE_MEMORY: content_type=tv_shows
          SAVE_MEMORY: favorite_actress=杨幂
          [Saved preference: content_type=tv_shows]
          [Saved preference: favorite_actress=杨幂]
          好的，我记住了！

# 下次启动 terminal
$ python glm_terminal.py

You: 推荐一些内容
Assistant: [自动读取记忆]
          根据您喜欢杨幂的电视剧，推荐：
          1. 三生三世十里桃花
          2. 宫锁心玉
          ...
```

## 📂 存储位置

```
.memories/
├── preferences.json    # 用户偏好
├── context.json        # 用户上下文
└── history.json        # 对话历史
```

## 🔍 查看记忆

### 在代码中
```python
summary = client.memory.get_memory_summary()
print(summary)
```

### 在 glm_terminal 中
```
You: show-memory
```

## ⚡ 关键点

1. **自动注入**：每次 `invoke()` 都会自动读取并注入记忆
2. **持久化**：保存在 `.memories/` 文件夹，跨会话保持
3. **透明使用**：AI 自动获得记忆，无需手动传递
4. **两种类型**：
   - **Preference**：用户偏好（语言、内容类型等）
   - **Context**：用户背景（项目、兴趣等）

## 📊 使用频率

| 操作 | 频率 | 说明 |
|------|------|------|
| 读取记忆 | 每次 `invoke()` | 自动注入到系统提示 |
| 保存记忆 | AI 判断或手动 | 用户提到偏好/背景时 |
| 保存历史 | 每次 `invoke()` | 自动保存对话 |

## 💡 最佳实践

1. **Preference** 用于：语言、内容类型、风格偏好
2. **Context** 用于：项目信息、工作背景、兴趣爱好
3. **让 AI 决定**：在 glm_terminal 中，AI 会自动判断何时保存
4. **定期查看**：使用 `show-memory` 检查保存的内容
