# AI 自动保存用户配置功能

## 功能说明

在 `glm_terminal.py` 中添加了 AI 自动决定何时保存用户配置的功能。

## 工作原理

使用简单的文本协议让 AI 触发保存：

1. **协议定义**: AI 在响应中包含 `SAVE_MEMORY: key=value`
2. **协议解析**: glm_terminal 检测并解析这个协议
3. **自动保存**: 根据 key 类型自动保存到 preference 或 context

## 使用示例

### 用户对话触发自动保存

```
You: 我喜欢看电影和电视剧
Assistant: 好的，我记住了您喜欢看电影和电视剧。
SAVE_MEMORY: content_type=movies_and_tv
[Saved preference: content_type=movies_and_tv]
我会为您推荐相关内容...
```

```
You: 我在做一个 AI 助手项目
Assistant: 明白了，我已经记录了您的项目信息。
SAVE_MEMORY: project=AI_Assistant
[Saved context: project=AI_Assistant]
```

## 协议格式

```
SAVE_MEMORY: key=value
```

- 必须在单独一行
- `key` 和 `value` 用 `=` 分隔
- 支持中文和英文

## 自动分类

系统根据 key 自动判断保存类型：

**Preference keys** (用户偏好):
- `language`
- `content_type`
- `region_preference`
- `preferred_style`

**Context keys** (用户上下文):
- 其他所有 key（如 `project`, `primary_interest` 等）

## AI 触发条件

AI 会在以下情况自动使用协议：

- 用户提到个人偏好（"我喜欢..."）
- 用户提到兴趣爱好
- 用户提到项目背景
- 用户提到工作方式
- 用户提到语言偏好
- 其他个人信息

## 测试

运行测试验证协议解析：

```bash
python test_save_memory_protocol.py
```

## 查看保存的记忆

在对话中输入：

```
show-memory
```

## 技术细节

- 使用文本协议而非工具调用（更简单、更可靠）
- 重用现有的 `MemoryManager` 保存数据
- 保存到 `.memories/` 目录
- 类似 `EXECUTE:` 命令的设计模式

## 优势

✅ AI 自动判断，无需手动触发  
✅ 重用现有 memory_manager 代码  
✅ 最小化代码修改  
✅ 简单可靠的文本协议  
✅ 不依赖复杂的工具调用机制
