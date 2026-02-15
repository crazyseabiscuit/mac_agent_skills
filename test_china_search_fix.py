#!/usr/bin/env python3
"""Test china_search improvements."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills.china_search.china_search import search_tavily_china, search_bing_china

def test_search():
    """Test search functions."""
    query = "杨幂"
    
    print("=" * 60)
    print(f"Testing search for: {query}")
    print("=" * 60)
    
    # Test Tavily
    print("\n1. Testing Tavily search...")
    tavily_results = search_tavily_china(query, "tv", 3)
    if tavily_results:
        print(f"✓ Found {len(tavily_results)} results from Tavily")
        for r in tavily_results[:2]:
            print(f"  - {r['title'][:50]}")
    else:
        print("✗ No results from Tavily (API key may not be set)")
    
    # Test Bing
    print("\n2. Testing Bing search...")
    bing_results = search_bing_china(query, "tv", 3)
    if bing_results:
        print(f"✓ Found {len(bing_results)} results from Bing")
        for r in bing_results[:2]:
            print(f"  - {r['title'][:50]}")
    else:
        print("✗ No results from Bing")
    
    print("\n" + "=" * 60)
    if tavily_results or bing_results:
        print("✅ At least one search source is working!")
    else:
        print("⚠️  No search sources returned results")
        print("💡 Suggestions:")
        print("   1. Set TAVILY_API_KEY environment variable")
        print("   2. Check network connection")
        print("   3. Try different search terms")

if __name__ == "__main__":
    test_search()
