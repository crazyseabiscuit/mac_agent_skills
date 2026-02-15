---
name: china-search
description: Search for Chinese mainland content including movies, TV shows, entertainment news, and local information
---

# china-search

## Overview

This skill allows you to search for content specific to Chinese mainland, including:
- 🎬 Movies (电影) and TV shows (电视剧)
- 📺 Entertainment news (娱乐新闻)
- 🏙️ Local events and information (本地信息)
- 🎵 Music and celebrities (音乐和明星)
- 📰 Regional news (地方新闻)

## Instructions

### Search Chinese Content

Use `china_search.py` to search for content on China's major platforms:

## Usage Examples

**Search for movies:**
```bash
python skills/china-search/china_search.py "流浪地球" --type movie
```

**Search for TV shows:**
```bash
python skills/china-search/china_search.py "三体" --type tv
```

**Search for entertainment news:**
```bash
python skills/china-search/china_search.py "张艺谋" --type entertainment
```

**Search for local events:**
```bash
python skills/china-search/china_search.py "北京演唱会" --type event
```

**General search across all platforms:**
```bash
python skills/china-search/china_search.py "哈利·波特"
```

**Get top 10 results:**
```bash
python skills/china-search/china_search.py "复仇者联盟" --limit 10
```

## Features

- ✅ Multiple search sources (Douban, Maoyan, IMDB China, Weibo)
- ✅ Content filtering by type (movie, tv, entertainment, event)
- ✅ Rating and review information from Douban
- ✅ Real-time data from Chinese platforms
- ✅ Support for Chinese and English queries
- ✅ Detailed results with ratings, descriptions, and links

## Supported Content Types

| Type | Source | Examples |
|------|--------|----------|
| `movie` | Douban, Maoyan | 流浪地球, 三体 |
| `tv` | Douban, iQiyi | 沙漠沙漠, 甄嬛传 |
| `entertainment` | Weibo, Sina | 明星新闻, 娱乐热点 |
| `event` | Douban Events, Local | 演唱会, 展览, 活动 |
| `all` | Multiple sources | 综合搜索 |

## API Integration

The skill searches through:
1. **Douban (豆瓣)** - Movies, TV shows, ratings
2. **Maoyan (猫眼)** - Real-time box office, reviews
3. **Weibo (微博)** - Entertainment news and trending topics
4. **QQ Music** - Music and celebrities

No API keys required - uses public web search and RSS feeds.
