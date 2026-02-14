#!/usr/bin/env python3
"""Search for latest news articles."""
import sys
import os
import json
import urllib.parse
import httpx
from datetime import datetime


def search_gnews(query, api_key, limit=5):
    """Search using GNews API."""
    try:
        lang = "zh" if any('\u4e00' <= c <= '\u9fff' for c in query) else "en"
        
        url = "https://gnews.io/api/v4/search"
        params = {"q": query, "lang": lang, "max": limit, "apikey": api_key}
        
        with httpx.Client(timeout=15) as client:
            response = client.get(url, params=params)
            if response.status_code != 200:
                return []
            
            data = response.json()
            results = []
            for article in data.get("articles", []):
                results.append({
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "source": article.get("source", {}).get("name", ""),
                    "publishedAt": article.get("publishedAt", ""),
                    "url": article.get("url", ""),
                    "api": "GNews"
                })
            return results
    except:
        return []


def search_newsapi(query, api_key, limit=5):
    """Search using Bing News RSS (no API key needed)."""
    try:
        import re
        encoded = urllib.parse.quote(query)
        url = f"https://www.bing.com/news/search?q={encoded}&format=rss"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        
        with httpx.Client(timeout=15, follow_redirects=True) as client:
            response = client.get(url, headers=headers)
            if response.status_code != 200:
                return []
            
            results = []
            items = re.findall(r'<item>(.*?)</item>', response.text, re.DOTALL)
            
            for item in items[:limit]:
                title_match = re.search(r'<title>(.*?)</title>', item)
                link_match = re.search(r'<link>(.*?)</link>', item)
                date_match = re.search(r'<pubDate>(.*?)</pubDate>', item)
                desc_match = re.search(r'<description>(.*?)</description>', item)
                
                if title_match:
                    results.append({
                        "title": title_match.group(1).strip(),
                        "description": re.sub(r'<[^>]+>', '', desc_match.group(1)).strip()[:200] if desc_match else "",
                        "source": "Bing News",
                        "publishedAt": date_match.group(1).strip() if date_match else "",
                        "url": link_match.group(1).strip() if link_match else "",
                        "api": "Bing"
                    })
            
            return results
    except:
        return []


def search_tavily(query, api_key, limit=5):
    """Search using Tavily API."""
    try:
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": api_key,
            "query": query,
            "search_depth": "basic",
            "include_answer": False,
            "max_results": limit,
            "topic": "news"
        }
        
        with httpx.Client(timeout=15) as client:
            response = client.post(url, json=payload)
            if response.status_code != 200:
                return []
            
            data = response.json()
            results = []
            for item in data.get("results", []):
                results.append({
                    "title": item.get("title", ""),
                    "description": item.get("content", "")[:200],
                    "source": "Tavily",
                    "publishedAt": item.get("published_date", ""),
                    "url": item.get("url", ""),
                    "api": "Tavily"
                })
            return results
    except:
        return []


def search_news(query, days=7, limit=5):
    """Search news from multiple sources and merge results."""
    try:
        from datetime import datetime, timedelta, timezone
        
        # Load API keys from config
        config_path = os.path.join(os.path.dirname(__file__), "../../config.properties")
        gnews_key = os.getenv("GNEWS_API_KEY", "")
        tavily_key = os.getenv("TAVILY_API_KEY", "")
        
        if os.path.exists(config_path):
            for line in open(config_path):
                if line.startswith("gnews.api_key="):
                    gnews_key = line.split("=", 1)[1].strip()
        
        all_results = []
        
        # Search GNews
        if gnews_key:
            all_results.extend(search_gnews(query, gnews_key, limit))
        
        # Search Tavily
        if tavily_key:
            all_results.extend(search_tavily(query, tavily_key, limit))
        
        # Search Bing News (no key needed)
        all_results.extend(search_newsapi(query, "", limit))
        
        if not all_results:
            return [{"error": "未找到新闻或 API key 未配置"}]
        
        # Filter by date
        from email.utils import parsedate_to_datetime
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        filtered_results = []
        
        for r in all_results:
            pub_date_str = r.get("publishedAt", "")
            if not pub_date_str:
                continue
            
            try:
                # Parse ISO format (GNews) or RFC 2822 (Bing/Tavily RSS)
                if "T" in pub_date_str and "Z" in pub_date_str:
                    pub_date = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
                else:
                    pub_date = parsedate_to_datetime(pub_date_str)
                
                if pub_date >= cutoff_date:
                    filtered_results.append(r)
            except:
                continue
        
        # Remove duplicates by URL
        seen_urls = set()
        unique_results = []
        for r in filtered_results:
            if r["url"] not in seen_urls:
                seen_urls.add(r["url"])
                unique_results.append(r)
        
        # Sort by date (newest first)
        unique_results.sort(key=lambda x: x.get("publishedAt", ""), reverse=True)
        
        return unique_results[:limit]
                
    except Exception as e:
        return [{"error": str(e)}]


def main():
    if len(sys.argv) < 2:
        print("Usage: python search_news.py <query> [--days N] [--limit N]")
        print("\n需要设置环境变量: export GNEWS_API_KEY=your_key")
        print("免费注册: https://gnews.io")
        sys.exit(1)
    
    query = sys.argv[1]
    days = 7
    limit = 5
    
    for i in range(2, len(sys.argv)):
        if sys.argv[i] == "--days" and i+1 < len(sys.argv):
            days = int(sys.argv[i+1])
        elif sys.argv[i] == "--limit" and i+1 < len(sys.argv):
            limit = int(sys.argv[i+1])
    
    print(f"搜索新闻: {query}\n")
    results = search_news(query, days, limit)
    
    if results and "error" in results[0]:
        print(f"错误: {results[0]['error']}")
        if "help" in results[0]:
            print(results[0]["help"])
        sys.exit(1)
    elif results:
        for i, article in enumerate(results, 1):
            print(f"{i}. {article['title']}")
            print(f"   来源: {article['source']} ({article.get('api', 'Unknown')}) | 时间: {article['publishedAt']}")
            if article.get('description'):
                print(f"   {article['description']}")
            print(f"   链接: {article['url']}\n")
    else:
        print("未找到相关新闻")


if __name__ == "__main__":
    main()
