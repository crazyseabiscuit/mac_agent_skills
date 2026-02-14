---
name: news-search
description: Search and retrieve latest news articles on any topic
---

# news-search

## Overview

This skill allows you to search for and retrieve the latest news articles on any topic using web search.

## Instructions

### Search News

Use `search_news.py` to search for latest news:
- Search by keyword or topic
- Get recent news articles
- Filter by date range

## Usage Examples

**Search for latest news:**
```bash
python skills/news-search/search_news.py "AI technology"
```

**Search with date filter:**
```bash
python skills/news-search/search_news.py "climate change" --days 7
```

**Get top headlines:**
```bash
python skills/news-search/search_news.py "breaking news" --limit 5
```
