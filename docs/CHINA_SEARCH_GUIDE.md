# China Search Skill

## 概述 (Overview)

**china-search** 是一个专门为搜索中国大陆内容设计的技能模块。它可以搜索电影、电视剧、娱乐新闻、本地活动等信息，整合了豆瓣、微博等主要中文平台的数据。

**china-search** is a specialized skill for searching Chinese mainland content including movies, TV shows, entertainment news, and local events, integrating data from major Chinese platforms like Douban and Weibo.

---

## 功能特性 (Features)

✅ **多源搜索** (Multi-source Search)
- 豆瓣 (Douban) - 电影和电视剧评分、评论
- 微博 (Weibo) - 娱乐新闻和热点话题
- 必应中国 (Bing China) - 区域优化的搜索结果

✅ **内容类型筛选** (Content Type Filtering)
- 电影 (Movies)
- 电视剧 (TV Shows)
- 娱乐新闻 (Entertainment News)
- 活动信息 (Events)
- 综合搜索 (All content)

✅ **丰富的元数据** (Rich Metadata)
- 评分信息 (Ratings from Douban)
- 发布年份 (Release year)
- 热度数据 (Popularity metrics)
- 来源链接 (Direct links)

✅ **零API密钥** (No API Keys Required)
- 使用公开网络搜索
- 无需付费API订阅
- 完全本地运行

---

## 使用方法 (Usage)

### 基本搜索 (Basic Search)

```bash
# 综合搜索 (General search)
python skills/china-search/china_search.py "流浪地球"

# 搜索电影 (Search movies)
python skills/china-search/china_search.py "流浪地球" --type movie

# 搜索电视剧 (Search TV shows)
python skills/china-search/china_search.py "三体" --type tv

# 搜索娱乐新闻 (Search entertainment news)
python skills/china-search/china_search.py "张艺谋" --type entertainment

# 搜索活动 (Search events)
python skills/china-search/china_search.py "北京演唱会" --type event
```

### 进阶选项 (Advanced Options)

```bash
# 获取更多结果 (Get more results)
python skills/china-search/china_search.py "复仇者联盟" --limit 10

# 结合多个选项 (Combine options)
python skills/china-search/china_search.py "漫威" --type movie --limit 10
```

---

## API 调用 (API Usage)

### 在 Python 中使用 (Use in Python)

```python
from skills.china_search.china_search import search_china_content

# 基础搜索
results = search_china_content("流浪地球", search_type="movie", limit=5)

# 处理结果
for item in results:
    print(f"标题: {item.get('title')}")
    print(f"评分: {item.get('rating')}")
    print(f"来源: {item.get('source')}")
    print(f"链接: {item.get('url')}")
    print()
```

### 在 GLMClient 中使用 (Use with GLMClient)

```python
from glm_langchain_client import GLMClient
from langchain_core.messages import HumanMessage, SystemMessage

client = GLMClient()

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="告诉我最近热门的电影有哪些")
]

response = client.invoke(messages)
# LLM 会自动调用 china-search 技能
```

---

## 输出格式 (Output Format)

### 电影结果 (Movie Results)

```
1. 流浪地球
   ⭐ 评分: 7.9
   📅 年份: 2019
   📌 来源: Douban | 类型: movie
   📝 描述: 太空歌剧电影，讲述地球停止公转面临灭亡的故事...
   🔗 https://www.douban.com/subject/XXXXXX/
```

### 电视剧结果 (TV Show Results)

```
1. 三体
   ⭐ 评分: 8.3
   📅 年份: 2023
   📌 来源: Douban | 类型: tv
   📝 描述: 根据刘慈欣同名小说改编的科幻电视剧...
   🔗 https://www.douban.com/subject/XXXXXX/
```

### 娱乐新闻结果 (Entertainment News Results)

```
1. 张艺谋新作首映
   🕐 时间: 2小时前
   👍 点赞: 5243
   📌 来源: Weibo | 类型: entertainment
   🔗 https://s.weibo.com/weibo?q=张艺谋
```

---

## 搜索类型详解 (Search Types Explained)

### all (综合搜索)

默认搜索所有内容类型，按相关性和评分排序。

```bash
python skills/china-search/china_search.py "哈利·波特"
# 返回: 电影 + 电视剧 + 新闻 + 活动
```

### movie (电影搜索)

专门搜索豆瓣电影数据库。

```bash
python skills/china-search/china_search.py "复仇者联盟" --type movie
# 返回: 所有复仇者联盟相关电影
```

### tv (电视剧搜索)

专门搜索豆瓣电视剧数据库。

```bash
python skills/china-search/china_search.py "甄嬛传" --type tv
# 返回: 甄嬛传及相关电视剧
```

### entertainment (娱乐新闻)

搜索微博和其他平台的娱乐新闻。

```bash
python skills/china-search/china_search.py "明星新闻" --type entertainment
# 返回: 最近的娱乐新闻和热点
```

### event (活动信息)

搜索演唱会、展览等活动信息。

```bash
python skills/china-search/china_search.py "演唱会" --type event
# 返回: 各城市的演唱会信息
```

---

## 数据源详情 (Data Sources)

### 豆瓣 (Douban)

| 属性 | 说明 |
|------|------|
| **URL** | https://www.douban.com |
| **覆盖范围** | 电影、电视剧、评分、评论 |
| **更新频率** | 实时 |
| **需要认证** | 否 (公开数据) |

**特点:**
- 最全的中文电影评分数据库
- 详细的演员和导演信息
- 用户评论和讨论

### 微博 (Weibo)

| 属性 | 说明 |
|------|------|
| **URL** | https://s.weibo.com |
| **覆盖范围** | 娱乐新闻、热点话题、明星动态 |
| **更新频率** | 实时 |
| **需要认证** | 否 (公开搜索) |

**特点:**
- 最新的娱乐新闻
- 实时热点话题
- 社交互动数据 (点赞、评论、转发)

### 必应中国 (Bing China)

| 属性 | 说明 |
|------|------|
| **URL** | https://www.bing.com |
| **覆盖范围** | 通用搜索 (中国区域优化) |
| **更新频率** | 实时 |
| **需要认证** | 否 (公开搜索) |

**特点:**
- 广泛的中文网络内容
- RSS 源支持
- 区域特定结果

---

## 示例场景 (Example Scenarios)

### 场景 1: 查找新上映电影

```bash
python skills/china-search/china_search.py "2024年新电影" --type movie --limit 10
```

**输出:**
```
1. 哈利·波特新传奇
   ⭐ 评分: 8.5
   📅 年份: 2024
   ...

2. 复仇者联盟：未来之战
   ⭐ 评分: 8.2
   📅 年份: 2024
   ...
```

### 场景 2: 获取娱乐明星新闻

```bash
python skills/china-search/china_search.py "杨紫" --type entertainment --limit 5
```

**输出:**
```
1. 杨紫新剧开机
   🕐 时间: 1小时前
   👍 点赞: 3421
   来源: Weibo
   ...
```

### 场景 3: 寻找本地活动

```bash
python skills/china-search/china_search.py "北京演唱会 2024年3月" --type event
```

**输出:**
```
1. 某歌手北京演唱会
   📌 活动类型: 演唱会
   🕐 时间: 2024年3月15日
   来源: 豆瓣活动
   ...
```

### 场景 4: 电视剧追剧指南

```bash
python skills/china-search/china_search.py "2024春季新剧" --type tv --limit 10
```

**输出:**
```
1. 新悬疑电视剧
   ⭐ 评分: 8.7
   📅 年份: 2024
   ...
```

---

## 故障排除 (Troubleshooting)

### 问题 1: "未找到相关内容"

**原因:**
- 搜索词太具体或不存在
- 网络连接问题
- 中文编码问题

**解决方案:**
```bash
# 尝试更简单的搜索词
python skills/china-search/china_search.py "电影" --type movie

# 检查网络连接
ping www.douban.com

# 确保终端支持 UTF-8 编码
export LANG=zh_CN.UTF-8
```

### 问题 2: 搜索速度慢

**原因:**
- 网络延迟
- 目标网站响应慢
- 数据量大

**解决方案:**
```bash
# 减少结果数量
python skills/china-search/china_search.py "电影" --limit 3

# 指定搜索类型 (比综合搜索更快)
python skills/china-search/china_search.py "电影名称" --type movie
```

### 问题 3: 某些搜索源无法访问

**原因:**
- 网络阻止或限制
- 目标网站维护
- DNS 问题

**解决方案:**
```bash
# 使用 VPN 或代理
# 检查网络连接
ping www.weibo.com
ping www.douban.com

# 尝试其他搜索类型
```

---

## 性能优化 (Performance Tips)

### ✅ 最佳实践

1. **使用具体的搜索词**
   ```bash
   # ✅ 好
   python skills/china-search/china_search.py "流浪地球"
   
   # ❌ 不好
   python skills/china-search/china_search.py "好看的电影"
   ```

2. **限制结果数量**
   ```bash
   # 只获取 5 个结果，快 2 倍
   python skills/china-search/china_search.py "电影" --limit 5
   ```

3. **指定搜索类型**
   ```bash
   # 搜索电影更快
   python skills/china-search/china_search.py "电影名" --type movie
   ```

4. **使用中文搜索**
   ```bash
   # ✅ 中文搜索更准确
   python skills/china-search/china_search.py "流浪地球"
   ```

---

## 集成示例 (Integration Examples)

### 与 GLMClient 集成

```python
from glm_langchain_client import GLMClient
from langchain_core.messages import HumanMessage, SystemMessage

# 初始化客户端（自动加载 china-search 技能）
client = GLMClient(
    api_key="your_api_key",
    skills_dir="skills"
)

# 发送包含搜索的消息
messages = [
    SystemMessage(content="You are a helpful movie recommender."),
    HumanMessage(content="推荐一些最新的科幻电影")
]

response = client.invoke(messages)
# 客户端会自动在必要时调用 china-search 技能
print(response)
```

### 在自定义代理中使用

```python
from skills.china_search.china_search import search_china_content

class MovieAgent:
    def find_movies(self, query: str, limit: int = 5):
        """Find movies using china-search."""
        results = search_china_content(
            query=query,
            search_type="movie",
            limit=limit
        )
        return self._format_results(results)
    
    def find_tv_shows(self, query: str, limit: int = 5):
        """Find TV shows using china-search."""
        results = search_china_content(
            query=query,
            search_type="tv",
            limit=limit
        )
        return self._format_results(results)
    
    def _format_results(self, results):
        """Format results for display."""
        output = []
        for item in results:
            output.append(f"📌 {item['title']} ({item.get('rating', 'N/A')}⭐)")
        return "\n".join(output)

# 使用
agent = MovieAgent()
print(agent.find_movies("2024年新电影", limit=5))
```

---

## 技术细节 (Technical Details)

### 支持的参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `query` | str | 必需 | 搜索关键词 |
| `search_type` | str | "all" | 搜索类型 (all/movie/tv/entertainment/event) |
| `limit` | int | 5 | 返回结果数量 |

### 返回结果结构

```python
[
    {
        "title": "电影/内容名称",
        "rating": "8.5",              # 可选
        "year": "2024",                # 可选
        "type": "movie",               # movie/tv/entertainment/event
        "description": "简短描述...",   # 可选
        "source": "Douban",            # Douban/Weibo/Bing
        "url": "https://...",
        "api": "Douban",               # API来源
        "timestamp": "2小时前",         # 可选
        "likes": "5243"                # 可选
    },
    ...
]
```

### 错误处理

```python
results = search_china_content("test", "all", 5)

if results and "error" in results[0]:
    error_msg = results[0]["error"]
    tips = results[0].get("tips", "")
    print(f"错误: {error_msg}")
    if tips:
        print(f"提示: {tips}")
```

---

## 常见问题 (FAQ)

**Q: 需要 API 密钥吗？**
A: 不需要。使用公开搜索，无需 API 密钥。

**Q: 能搜索国外内容吗？**
A: 可以，但内容主要优化用于中文内容。

**Q: 搜索结果准确度如何？**
A: 基于豆瓣和微博的官方数据，准确度较高。

**Q: 可以用于生产环境吗？**
A: 可以，但要注意网络延迟和目标网站的可用性。

**Q: 能缓存搜索结果吗？**
A: 可以在应用层面实现缓存策略。

---

## 更新日志 (Changelog)

### v1.0.0 (2026-02-14)
- ✅ 初始版本发布
- ✅ 支持豆瓣、微博、必应搜索
- ✅ 5 种搜索类型
- ✅ 完整文档和测试

---

## 许可证 (License)

MIT License - 详见项目 LICENSE 文件

---

**最后更新**: 2026-02-14  
**维护者**: Mac Agent Skills Team
