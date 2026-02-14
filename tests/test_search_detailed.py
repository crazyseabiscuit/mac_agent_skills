import os
import sys
from pathlib import Path
from collections import Counter

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "news-search"))

# Load configuration from config.properties
def load_config():
    """Load configuration from config.properties"""
    config_path = Path(__file__).parent.parent / "config.properties"
    config = {}
    if config_path.exists():
        for line in config_path.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    return config

config = load_config()

# Set environment variables from config
os.environ["TAVILY_API_KEY"] = config.get("tavily.api_key", "YOUR_TAVILY_API_KEY_HERE")
os.environ["GNEWS_API_KEY"] = config.get("gnews.api_key", "YOUR_GNEWS_API_KEY_HERE")

from search_news import search_tavily, search_gnews, search_newsapi

query = "AI"
limit = 5

print("1. Testing Tavily...")
tavily_results = search_tavily(query, os.getenv("TAVILY_API_KEY"), limit)
print(f"   Tavily returned: {len(tavily_results)} results")

print("\n2. Testing GNews...")
gnews_results = search_gnews(query, os.getenv("GNEWS_API_KEY"), limit)
print(f"   GNews returned: {len(gnews_results)} results")

print("\n3. Testing Bing...")
bing_results = search_newsapi(query, "", limit)
print(f"   Bing returned: {len(bing_results)} results")

print(f"\n4. Total before merge: {len(tavily_results) + len(gnews_results) + len(bing_results)}")

all_results = []
all_results.extend(gnews_results)
all_results.extend(tavily_results)
all_results.extend(bing_results)

print(f"5. After extend: {len(all_results)}")

# Remove unnecessary import from line 34
print(f"6. Sources: {dict(sources)}")
print(f"6. Sources: {dict(sources)}")
