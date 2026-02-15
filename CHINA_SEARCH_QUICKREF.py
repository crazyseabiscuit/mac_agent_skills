#!/usr/bin/env python3
"""
Quick Reference Guide for China-Search Skill

中国搜索功能快速参考指南
"""

# ============================================================================
# 1. 命令行快速使用 (Command Line Quick Usage)
# ============================================================================

QUICK_COMMANDS = """
🎬 搜索电影 (Search Movies)
   python skills/china-search/china_search.py "流浪地球" --type movie

📺 搜索电视剧 (Search TV Shows)
   python skills/china-search/china_search.py "三体" --type tv

📰 搜索娱乐新闻 (Search Entertainment News)
   python skills/china-search/china_search.py "明星新闻" --type entertainment

🎪 搜索活动 (Search Events)
   python skills/china-search/china_search.py "演唱会" --type event

🔍 综合搜索 (General Search)
   python skills/china-search/china_search.py "哈利·波特" --limit 10
"""

# ============================================================================
# 2. Python API 快速使用 (Python API Quick Usage)
# ============================================================================

PYTHON_API_EXAMPLES = """
from skills.china_search.china_search import search_china_content

# 搜索电影 (Search movies)
results = search_china_content("流浪地球", "movie", limit=5)
for r in results:
    print(f"{r['title']} - {r.get('rating', 'N/A')}⭐")

# 搜索电视剧 (Search TV shows)
results = search_china_content("三体", "tv", limit=5)

# 搜索娱乐新闻 (Search entertainment news)
results = search_china_content("明星", "entertainment", limit=5)

# 搜索活动 (Search events)
results = search_china_content("演唱会", "event", limit=5)

# 综合搜索 (General search)
results = search_china_content("哈利·波特", "all", limit=10)
"""

# ============================================================================
# 3. 搜索类型说明 (Search Types Explanation)
# ============================================================================

SEARCH_TYPES = {
    "movie": {
        "description": "电影搜索 (Movie Search)",
        "source": "豆瓣 (Douban)",
        "includes": ["评分", "年份", "评论", "演员"],
        "example": 'search_china_content("流浪地球", "movie")'
    },
    "tv": {
        "description": "电视剧搜索 (TV Show Search)",
        "source": "豆瓣 (Douban)",
        "includes": ["评分", "年份", "集数", "演员"],
        "example": 'search_china_content("三体", "tv")'
    },
    "entertainment": {
        "description": "娱乐新闻 (Entertainment News)",
        "source": "微博 (Weibo)",
        "includes": ["发布时间", "点赞数", "评论数", "话题"],
        "example": 'search_china_content("明星", "entertainment")'
    },
    "event": {
        "description": "活动信息 (Events)",
        "source": "豆瓣活动、本地信息",
        "includes": ["活动名称", "时间", "地点", "门票"],
        "example": 'search_china_content("演唱会", "event")'
    },
    "all": {
        "description": "综合搜索 (General Search)",
        "source": "所有来源 (All sources)",
        "includes": ["电影", "电视剧", "新闻", "活动"],
        "example": 'search_china_content("哈利·波特", "all")'
    }
}

# ============================================================================
# 4. 返回结果结构 (Result Structure)
# ============================================================================

RESULT_STRUCTURE = {
    "title": "内容标题 (Content Title)",
    "rating": "评分 (Rating) - 可选",
    "year": "年份 (Release Year) - 可选",
    "type": "内容类型 (Content Type)",
    "description": "简介 (Description) - 可选",
    "source": "数据来源 (Data Source)",
    "url": "链接 (URL)",
    "api": "API来源 (API Source)",
    "timestamp": "发布时间 (Timestamp) - 可选",
    "likes": "点赞数 (Likes) - 可选"
}

# ============================================================================
# 5. 错误处理 (Error Handling)
# ============================================================================

ERROR_HANDLING = """
results = search_china_content("query", "type", limit)

# 检查错误
if results and "error" in results[0]:
    error = results[0]["error"]
    tips = results[0].get("tips", "")
    print(f"❌ 错误: {error}")
    if tips:
        print(f"💡 提示: {tips}")
else:
    # 正常处理结果
    for item in results:
        print(f"✅ {item['title']}")
"""

# ============================================================================
# 6. 常见问题快速解答 (FAQ)
# ============================================================================

FAQ = {
    "需要API密钥吗？": "❌ 不需要。使用公开网络搜索，完全免费。",
    
    "支持什么语言？": "✅ 中文和英文。内部使用中文优化搜索。",
    
    "为什么搜索结果为空？": "📝 请尝试:\n   1. 使用更简单的搜索词\n   2. 使用中文搜索\n   3. 检查网络连接",
    
    "为什么搜索很慢？": "⚡ 请尝试:\n   1. 减少 --limit 参数值\n   2. 指定搜索类型而非 'all'\n   3. 使用简短的搜索词",
    
    "可以用于生产环境吗？": "✅ 可以，但要注意网络延迟和网站可用性。",
    
    "能缓存结果吗？": "✅ 可以在应用层实现缓存策略。",
    
    "支持批量搜索吗？": "✅ 可以在循环中多次调用函数。"
}

# ============================================================================
# 7. 与 GLMClient 集成 (Integration with GLMClient)
# ============================================================================

GLMCLIENT_INTEGRATION = """
from glm_langchain_client import GLMClient
from langchain_core.messages import HumanMessage, SystemMessage

# 初始化客户端
client = GLMClient(
    api_key="your_api_key",
    skills_dir="skills"  # 自动加载所有技能
)

# 发送消息
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="推荐最新的科幻电影")
]

# LLM 会自动调用 china-search 技能
response = client.invoke(messages)
print(response)
"""

# ============================================================================
# 8. 性能优化建议 (Performance Tips)
# ============================================================================

PERFORMANCE_TIPS = [
    "✅ 使用具体的搜索词（避免太宽泛）",
    "✅ 减少 limit 参数值（默认 5，可设为 3）",
    "✅ 指定搜索类型（比综合搜索快）",
    "✅ 使用中文搜索（比英文搜索更准确）",
    "✅ 检查网络延迟（某些时段网络较慢）"
]

# ============================================================================
# 9. 文档链接 (Documentation Links)
# ============================================================================

DOCUMENTATION = {
    "完整指南": "docs/CHINA_SEARCH_GUIDE.md",
    "技能说明": "skills/china-search/SKILL.md",
    "使用示例": "example_china_search.py",
    "测试文件": "tests/test_china_search.py",
    "功能总结": "docs/CHINA_SEARCH_FEATURE_SUMMARY.md"
}

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("中国搜索功能 (China-Search Skill) - 快速参考指南")
    print("="*70 + "\n")
    
    print("📚 搜索类型:")
    print("-" * 70)
    for search_type, info in SEARCH_TYPES.items():
        print(f"\n  {search_type.upper()}: {info['description']}")
        print(f"  来源: {info['source']}")
        print(f"  包含: {', '.join(info['includes'])}")
        print(f"  示例: {info['example']}")
    
    print("\n" + "="*70)
    print("🎯 快速命令:")
    print("-" * 70)
    print(QUICK_COMMANDS)
    
    print("\n" + "="*70)
    print("📖 Python API:")
    print("-" * 70)
    print(PYTHON_API_EXAMPLES)
    
    print("\n" + "="*70)
    print("❓ 常见问题:")
    print("-" * 70)
    for question, answer in FAQ.items():
        print(f"\nQ: {question}")
        print(f"A: {answer}")
    
    print("\n" + "="*70)
    print("🔗 文档链接:")
    print("-" * 70)
    for name, path in DOCUMENTATION.items():
        print(f"  • {name}: {path}")
    
    print("\n" + "="*70)
    print("✨ 快速开始:")
    print("-" * 70)
    print("""
  1. 查看完整指南:
     cat docs/CHINA_SEARCH_GUIDE.md
  
  2. 运行命令行搜索:
     python skills/china-search/china_search.py "流浪地球" --type movie
  
  3. 运行测试:
     python tests/test_china_search.py
  
  4. 查看使用示例:
     python example_china_search.py
    """)
    
    print("="*70 + "\n")
