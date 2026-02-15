#!/usr/bin/env python3
"""Quick examples for using the china-search skill."""

# Example 1: Search for movies
print("=" * 60)
print("示例 1: 搜索电影")
print("=" * 60)
print("""
from skills.china_search.china_search import search_china_content

# 搜索流浪地球电影
results = search_china_content("流浪地球", search_type="movie", limit=3)

for item in results:
    print(f"标题: {item['title']}")
    print(f"评分: {item.get('rating', 'N/A')}")
    print(f"年份: {item.get('year', 'N/A')}")
    print(f"链接: {item['url']}")
    print()
""")

# Example 2: Search for TV shows
print("\n" + "=" * 60)
print("示例 2: 搜索电视剧")
print("=" * 60)
print("""
# 搜索三体电视剧
results = search_china_content("三体", search_type="tv", limit=5)

for item in results:
    if item.get('rating'):
        print(f"⭐ {item['title']} ({item['rating']}分)")
    else:
        print(f"📺 {item['title']}")
""")

# Example 3: Entertainment news
print("\n" + "=" * 60)
print("示例 3: 娱乐新闻")
print("=" * 60)
print("""
# 搜索明星新闻
results = search_china_content("杨紫", search_type="entertainment", limit=5)

for item in results:
    print(f"新闻: {item['title']}")
    if item.get('timestamp'):
        print(f"时间: {item['timestamp']}")
    if item.get('likes'):
        print(f"点赞: {item['likes']}")
    print()
""")

# Example 4: Command line usage
print("\n" + "=" * 60)
print("示例 4: 命令行使用")
print("=" * 60)
print("""
# 电影搜索
python skills/china-search/china_search.py "流浪地球" --type movie --limit 5

# 电视剧搜索
python skills/china-search/china_search.py "三体" --type tv --limit 5

# 娱乐新闻
python skills/china-search/china_search.py "明星" --type entertainment --limit 5

# 活动信息
python skills/china-search/china_search.py "北京演唱会" --type event --limit 5

# 综合搜索（默认）
python skills/china-search/china_search.py "哈利·波特" --limit 10
""")

# Example 5: Integration with GLMClient
print("\n" + "=" * 60)
print("示例 5: 与 GLMClient 集成")
print("=" * 60)
print("""
from glm_langchain_client import GLMClient
from langchain_core.messages import HumanMessage, SystemMessage

# 初始化客户端（自动加载所有技能）
client = GLMClient(
    api_key="your_api_key",
    skills_dir="skills"
)

# 发送消息，客户端会自动使用 china-search 技能
messages = [
    SystemMessage(content="You are a helpful movie recommender."),
    HumanMessage(content="推荐一些最新的科幻电影")
]

response = client.invoke(messages)
print(response)
""")

# Example 6: Error handling
print("\n" + "=" * 60)
print("示例 6: 错误处理")
print("=" * 60)
print("""
results = search_china_content("invalid_query_xyz", "all", 5)

if results and "error" in results[0]:
    print(f"错误: {results[0]['error']}")
    if "tips" in results[0]:
        print(f"提示: {results[0]['tips']}")
else:
    print(f"找到 {len(results)} 个结果")
""")

print("\n" + "=" * 60)
print("✨ 更多示例请查看文档:")
print("docs/CHINA_SEARCH_GUIDE.md")
print("=" * 60)
