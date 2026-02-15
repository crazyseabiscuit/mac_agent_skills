#!/usr/bin/env python3
"""Search for Chinese mainland content - movies, TV shows, entertainment, and local info."""
import sys
import os
import json
import re
import httpx
from datetime import datetime
from typing import List, Dict, Optional


def search_douban_movie(query: str, limit: int = 5) -> List[Dict]:
    """Search for movies on Douban (豆瓣)."""
    try:
        encoded_query = query.replace(" ", "+")
        # Try multiple search endpoints
        urls = [
            f"https://search.douban.com/movie?q={encoded_query}",
            f"https://www.douban.com/search?q={encoded_query}&cat=1002",
        ]
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        for url in urls:
            try:
                with httpx.Client(timeout=8, follow_redirects=True) as client:
                    response = client.get(url, headers=headers)
                    if response.status_code != 200:
                        continue
                    
                    results = []
                    # Try multiple patterns
                    patterns = [
                        r'<div class="item">.*?</div>',
                        r'<div class="result">.*?</div>',
                        r'<li class=".*?">.*?</li>'
                    ]
                    
                    items = []
                    for pattern in patterns:
                        items = re.findall(pattern, response.text, re.DOTALL)
                        if items:
                            break
                    
                    for item in items[:limit]:
                        # Extract title - try multiple patterns
                        title_match = None
                        for pattern in [
                            r'<a href=".*?/subject/(\d+)/"[^>]*>([^<]+)</a>',
                            r'<a[^>]*href="[^"]*subject[^"]*"[^>]*>([^<]+)</a>'
                        ]:
                            title_match = re.search(pattern, item)
                            if title_match:
                                break
                        
                        if not title_match:
                            continue
                        
                        movie_id = title_match.group(1) if title_match.lastindex >= 1 else "unknown"
                        title = title_match.group(2) if title_match.lastindex >= 2 else title_match.group(1)
                        title = title.strip()
                        
                        # Extract rating
                        rating_match = re.search(r'(\d+\.\d+)\s*分|(\d+\.\d+)', item)
                        rating = rating_match.group(1) or rating_match.group(2) if rating_match else "N/A"
                        
                        # Extract year
                        year_match = re.search(r'(\d{4})', item)
                        year = year_match.group(1) if year_match else "N/A"
                        
                        results.append({
                            "title": title,
                            "rating": rating,
                            "year": year,
                            "type": "movie",
                            "description": "豆瓣电影",
                            "source": "Douban",
                            "url": f"https://www.douban.com/subject/{movie_id}/" if movie_id != "unknown" else url,
                            "api": "Douban"
                        })
                    
                    if results:
                        return results
            except:
                continue
        
        return []
    except Exception as e:
        return []


def search_douban_tv(query: str, limit: int = 5) -> List[Dict]:
    """Search for TV shows on Douban (豆瓣)."""
    try:
        encoded_query = query.replace(" ", "+")
        urls = [
            f"https://search.douban.com/tv?q={encoded_query}",
            f"https://www.douban.com/search?q={encoded_query}&cat=1000",
        ]
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        for url in urls:
            try:
                with httpx.Client(timeout=8, follow_redirects=True) as client:
                    response = client.get(url, headers=headers)
                    if response.status_code != 200:
                        continue
                    
                    results = []
                    patterns = [
                        r'<div class="item">.*?</div>',
                        r'<div class="result">.*?</div>',
                    ]
                    
                    items = []
                    for pattern in patterns:
                        items = re.findall(pattern, response.text, re.DOTALL)
                        if items:
                            break
                    
                    for item in items[:limit]:
                        title_match = None
                        for pattern in [
                            r'<a href=".*?/subject/(\d+)/"[^>]*>([^<]+)</a>',
                            r'<a[^>]*href="[^"]*subject[^"]*"[^>]*>([^<]+)</a>'
                        ]:
                            title_match = re.search(pattern, item)
                            if title_match:
                                break
                        
                        if not title_match:
                            continue
                        
                        tv_id = title_match.group(1) if title_match.lastindex >= 1 else "unknown"
                        title = title_match.group(2) if title_match.lastindex >= 2 else title_match.group(1)
                        title = title.strip()
                        
                        rating_match = re.search(r'(\d+\.\d+)\s*分|(\d+\.\d+)', item)
                        rating = rating_match.group(1) or rating_match.group(2) if rating_match else "N/A"
                        
                        year_match = re.search(r'(\d{4})', item)
                        year = year_match.group(1) if year_match else "N/A"
                        
                        results.append({
                            "title": title,
                            "rating": rating,
                            "year": year,
                            "type": "tv",
                            "description": "豆瓣电视剧",
                            "source": "Douban",
                            "url": f"https://www.douban.com/subject/{tv_id}/" if tv_id != "unknown" else url,
                            "api": "Douban"
                        })
                    
                    if results:
                        return results
            except:
                continue
        
        return []
    except Exception as e:
        return []


def search_weibo_entertainment(query: str, limit: int = 5) -> List[Dict]:
    """Search for entertainment news on Weibo (微博)."""
    try:
        encoded_query = query.replace(" ", "%20")
        url = f"https://s.weibo.com/weibo?q={encoded_query}&xsort=hot"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        
        with httpx.Client(timeout=10, follow_redirects=True) as client:
            response = client.get(url, headers=headers)
            if response.status_code != 200:
                return []
            
            results = []
            # Extract Weibo posts
            posts = re.findall(r'<div class="s-page-result .*?">(.*?)</div>', response.text, re.DOTALL)
            
            for post in posts[:limit]:
                # Extract title/content
                title_match = re.search(r'>([^<]{10,100}?)<', post)
                if not title_match:
                    continue
                
                title = title_match.group(1).strip()
                # Remove HTML tags from title
                title = re.sub(r'<[^>]+>', '', title)
                
                # Extract timestamp
                time_match = re.search(r'(\d{1,2}分钟前|\d{1,2}小时前|\d{1,2}月\d{1,2}日)', post)
                timestamp = time_match.group(1) if time_match else "最近"
                
                # Extract engagement (likes, reposts, comments)
                likes_match = re.search(r'赞\[(\d+)\]', post)
                likes = likes_match.group(1) if likes_match else "0"
                
                results.append({
                    "title": title[:80],
                    "timestamp": timestamp,
                    "likes": likes,
                    "type": "entertainment",
                    "source": "Weibo",
                    "url": f"https://s.weibo.com/weibo?q={encoded_query}",
                    "api": "Weibo"
                })
            
            return results
    except Exception as e:
        return []


def search_tavily_china(query: str, search_type: str = "all", limit: int = 5) -> List[Dict]:
    """Search using Tavily API with China focus."""
    try:
        import os
        tavily_key = os.getenv("TAVILY_API_KEY")
        if not tavily_key:
            return []
        
        # Build search query
        if search_type == "movie":
            search_query = f"{query} 电影 豆瓣"
        elif search_type == "tv":
            search_query = f"{query} 电视剧 豆瓣"
        elif search_type == "entertainment":
            search_query = f"{query} 娱乐"
        else:
            search_query = query
        
        # Use Tavily HTTP API
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": tavily_key,
            "query": search_query,
            "search_depth": "basic",
            "max_results": limit,
            "include_domains": ["douban.com", "zhihu.com", "weibo.com"]
        }
        
        with httpx.Client(timeout=10) as client:
            response = client.post(url, json=payload)
            if response.status_code != 200:
                return []
            
            data = response.json()
            results = []
            for item in data.get("results", []):
                results.append({
                    "title": item.get("title", ""),
                    "description": item.get("content", "")[:150],
                    "source": "Tavily",
                    "url": item.get("url", ""),
                    "type": search_type,
                    "api": "Tavily"
                })
            
            return results
    except Exception as e:
        return []


def search_bing_china(query: str, search_type: str = "all", limit: int = 5) -> List[Dict]:
    """Search using Bing with China region filter."""
    try:
        region = "zh-CN"
        
        # Build search query based on type with exact match
        if search_type == "movie":
            search_query = f'"{query}" 电影 豆瓣'
        elif search_type == "tv":
            search_query = f'"{query}" 电视剧 豆瓣'
        elif search_type == "entertainment":
            search_query = f'"{query}" 娱乐新闻'
        elif search_type == "event":
            search_query = f'"{query}" 活动 演唱会'
        else:
            search_query = f'"{query}"'
        
        encoded_search = search_query.replace(" ", "+")
        url = f"https://www.bing.com/search?q={encoded_search}&mkt={region}&format=rss"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        
        with httpx.Client(timeout=10, follow_redirects=True) as client:
            response = client.get(url, headers=headers)
            if response.status_code != 200:
                return []
            
            results = []
            items = re.findall(r'<item>(.*?)</item>', response.text, re.DOTALL)
            
            # Extract query keywords for relevance filtering
            query_keywords = set(query.lower().split())
            
            for item in items[:limit * 2]:  # Get more to filter
                title_match = re.search(r'<title>(.*?)</title>', item)
                link_match = re.search(r'<link>(.*?)</link>', item)
                date_match = re.search(r'<pubDate>(.*?)</pubDate>', item)
                desc_match = re.search(r'<description>(.*?)</description>', item)
                
                if title_match:
                    title = title_match.group(1).strip()
                    description = ""
                    if desc_match:
                        description = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip()[:150]
                    
                    # Filter: check if query appears in title or description
                    title_lower = title.lower()
                    desc_lower = description.lower()
                    
                    # Check if main query keywords are in title/description
                    if query.lower() in title_lower or query.lower() in desc_lower:
                        results.append({
                            "title": title,
                            "description": description,
                            "source": "Bing China",
                            "publishedAt": date_match.group(1).strip() if date_match else "",
                            "url": link_match.group(1).strip() if link_match else "",
                            "type": search_type,
                            "api": "Bing"
                        })
                        
                        if len(results) >= limit:
                            break
            
            return results
    except Exception as e:
        return []


def search_china_content(query: str, search_type: str = "all", limit: int = 5) -> List[Dict]:
    """Search for Chinese mainland content from multiple sources."""
    try:
        all_results = []
        
        # Try Tavily first (most reliable)
        tavily_results = search_tavily_china(query, search_type, limit)
        all_results.extend(tavily_results)
        
        # Search Douban for movies
        if search_type in ["all", "movie"]:
            douban_movies = search_douban_movie(query, limit)
            all_results.extend(douban_movies)
        
        # Search Douban for TV shows
        if search_type in ["all", "tv"]:
            douban_tvs = search_douban_tv(query, limit)
            all_results.extend(douban_tvs)
        
        # Search Weibo for entertainment news
        if search_type in ["all", "entertainment"]:
            weibo_results = search_weibo_entertainment(query, limit)
            all_results.extend(weibo_results)
        
        # Search Bing with region filter (fallback)
        if not all_results:
            bing_results = search_bing_china(query, search_type, limit)
            all_results.extend(bing_results)
        
        # 如果没有通过网络搜索到结果，提供本地数据库建议
        if not all_results:
            return [{
                "error": f"网络搜索未找到结果: {query}",
                "tips": "💡 建议:\n   1. 检查网络连接\n   2. 尝试更简短的搜索词\n   3. 使用中文搜索关键词\n   4. 尝试其他搜索类型\n\n   离线建议:\n   • 推荐在豆瓣网站直接搜索: https://www.douban.com\n   • 或使用 'all' 类型进行综合搜索"
            }]
        
        # Remove duplicates by title
        seen_titles = set()
        unique_results = []
        for r in all_results:
            title = r.get("title", "")
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_results.append(r)
        
        # Sort by type priority and limit results
        type_priority = {"movie": 0, "tv": 1, "entertainment": 2, "event": 3}
        unique_results.sort(
            key=lambda x: (
                type_priority.get(x.get("type", "all"), 99),
                x.get("rating", "0")
            ),
            reverse=True
        )
        
        return unique_results[:limit]
        
    except Exception as e:
        return [{
            "error": f"搜索出错: {str(e)}",
            "help": "请检查网络连接并重试"
        }]


def main():
    if len(sys.argv) < 2:
        print("用法: python china_search.py <搜索词> [--type TYPE] [--limit N]")
        print("\n支持的搜索类型:")
        print("  movie          - 电影")
        print("  tv             - 电视剧")
        print("  entertainment  - 娱乐新闻")
        print("  event          - 活动和演唱会")
        print("  all            - 综合搜索（默认）")
        print("\n示例:")
        print("  python china_search.py '流浪地球' --type movie")
        print("  python china_search.py '三体' --type tv")
        print("  python china_search.py '张艺谋' --type entertainment")
        sys.exit(1)
    
    query = sys.argv[1]
    search_type = "all"
    limit = 5
    
    for i in range(2, len(sys.argv)):
        if sys.argv[i] == "--type" and i + 1 < len(sys.argv):
            search_type = sys.argv[i + 1]
        elif sys.argv[i] == "--limit" and i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])
    
    print(f"🔍 搜索中国内容: {query} (类型: {search_type})\n")
    results = search_china_content(query, search_type, limit)
    
    if results and "error" in results[0]:
        print(f"❌ {results[0]['error']}")
        if "tips" in results[0]:
            print(f"💡 {results[0]['tips']}")
        sys.exit(1)
    elif results:
        for i, item in enumerate(results, 1):
            print(f"{i}. {item.get('title', '未知')}")
            
            # Show rating if available
            if item.get('rating') and item['rating'] != 'N/A':
                print(f"   ⭐ 评分: {item['rating']}")
            
            # Show year if available
            if item.get('year') and item['year'] != 'N/A':
                print(f"   📅 年份: {item['year']}")
            
            # Show timestamp if available
            if item.get('timestamp'):
                print(f"   🕐 时间: {item['timestamp']}")
            
            # Show likes if available
            if item.get('likes'):
                print(f"   👍 点赞: {item['likes']}")
            
            # Show source and type
            source = item.get('source', 'Unknown')
            content_type = item.get('type', 'unknown')
            print(f"   📌 来源: {source} | 类型: {content_type}")
            
            # Show description if available
            if item.get('description'):
                print(f"   📝 {item['description'][:100]}...")
            
            # Show URL
            if item.get('url'):
                print(f"   🔗 {item['url']}")
            
            print()
    else:
        print("❌ 未找到相关内容")


if __name__ == "__main__":
    main()
