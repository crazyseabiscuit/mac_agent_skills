# GLM Terminal 工具执行修复 v2

## 🐛 问题描述

### 问题 1：用户看不到搜索结果
当 AI 执行搜索命令时，用户只看到"搜索新闻: xxx"，看不到实际的新闻列表。

### 问题 2：AI 不再翻译和总结
之前 AI 会自动将英文新闻翻译成中文并总结，现在不会了。

## ✅ 最终修复方案

### 新的逻辑：

```python
# 1. AI 返回 EXECUTE 命令
response = "EXECUTE: python skills/news-search/..."

# 2. Terminal 执行命令
output = execute_command(cmd)

# 3. ✅ 直接打印完整输出给用户
print(f"\n[Executing: {cmd}]\n")
print(output)  # ✅ 用户看到原始搜索结果
print()

# 4. ✅ 让 AI 用中文总结结果
messages.append(AIMessage(content=f"Command executed: {cmd}\nResult: {output}"))
messages.append(HumanMessage(content="请用中文总结上面的搜索结果，提取关键信息。"))
summary = client.invoke(messages)

# 5. ✅ 显示 AI 的中文总结
print(f"\nAssistant: {summary}\n")
messages.append(AIMessage(content=summary))
```

## 📊 完整效果

```
You: 帮我搜索今天的足球新闻

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
