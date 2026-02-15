# GLM Terminal 工具执行修复

## 🐛 问题描述

在使用 `glm_terminal.py` 时，当 AI 调用工具（如 news-search）时，用户看不到实际的搜索结果。

### 症状
```
You: 帮我查找今天的足球新闻

A: Command executed: python skills/news-search/search_news.py "足球 今日新闻" --limit 8
Result: 搜索新闻: 足球 今日新闻

You: ok
```

用户只看到"搜索新闻: xxx"，但看不到实际的新闻列表。

## 🔍 根本原因

### 原来的逻辑（有问题）：

```python
# 1. AI 返回 EXECUTE 命令
response = "EXECUTE: python skills/news-search/..."

# 2. Terminal 执行命令
output = execute_command(cmd)
print(f"[Output: {output}]")  # ❌ 只打印在 [] 里，不明显

# 3. 添加到消息历史
messages.append(AIMessage(content=f"Command executed: {cmd}\nResult: {output}"))

# 4. 让 AI 再次解释
messages.append(HumanMessage(content="Based on the actual result above, answer my question."))
response = client.invoke(messages)  # ❌ 第二次响应覆盖了第一次

# 5. 打印 AI 的第二次响应
print(f"\nAssistant: {response}\n")  # ❌ 用户只看到这个
```

**问题**：
1. 实际输出被包在 `[Output: ...]` 里，不明显
2. AI 的第二次响应覆盖了实际结果
3. 用户看不到完整的搜索结果

## ✅ 修复方案

### 新的逻辑：

```python
# 1. AI 返回 EXECUTE 命令
response = "EXECUTE: python skills/news-search/..."

# 2. Terminal 执行命令
output = execute_command(cmd)

# 3. ✅ 直接打印完整输出给用户
print(f"\n[Executing: {cmd}]\n")
print(output)  # ✅ 用户直接看到搜索结果
print()

# 4. 添加到消息历史（供 AI 参考）
messages.append(AIMessage(content=f"Command executed: {cmd}\nResult: {output}"))

# 5. ✅ 不再让 AI 重新解释，用户已经看到结果了
continue  # 跳过打印 AI 响应

# 6. ✅ 只有非 EXECUTE 响应才打印
if "EXECUTE:" not in response:
    print(f"\nAssistant: {response}\n")
```

## 📊 修复前后对比

### 修复前 ❌
```
You: 帮我搜索足球新闻


A: [Output: 搜索新闻: 足球 今日新闻]
   Command executed...
   
   (用户看不到实际新闻)
```

### 修复后 ✅
```
You: 帮我搜索足球新闻

[Executing: python skills/news-search/search_news.py "足球 今日新闻" --limit 3]

搜索新闻: 足球 今日新闻

1. The Super League project is officially over! - Sky Sports
   来源: Tavily | 时间: Wed, 11 Feb 2026
   链接: https://www.skysports.com/football/...

2. Harry Maguire likely to sign new contract - Sky Sports
   来源: Tavily | 时间: Tue, 10 Feb 2026
   链接: https://www.skysports.com/football/...

3. Darwin Nunez heading back to Premier League? - Sky Sports
   来源: Tavily | 时间: Thu, 12 Feb 2026
   链接: https://www.skysports.com/football/...

You: (继续对话)
```

## 🎯 关键改进

1. **直接显示结果**：用户立即看到完整的搜索结果
2. **简化流程**：不需要 AI 二次解释
3. **更好的体验**：清晰、直观、快速

## 📝 修改的文件

- `glm_terminal.py` (第 180-195 行)

## 🧪 测试

运行测试验证修复：
```bash
python test_execute_fix.py
```

## 💡 适用场景

这个修复适用于所有使用 `EXECUTE:` 协议的工具：
- ✅ news-search（新闻搜索）
- ✅ china-search（中国内容搜索）
- ✅ 任何其他返回大量文本的工具

## 🚀 使用

修复后，正常使用 glm_terminal 即可：

```bash
python glm_terminal.py

You: 帮我搜索今天的足球新闻
# 立即看到完整搜索结果

You: 搜索杨幂的电视剧
# 立即看到完整搜索结果
```
