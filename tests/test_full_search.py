import os
import sys
from pathlib import Path

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

from search_news import search_news

results = search_news("AI", days=7, limit=10)
print(f"Total results: {len(results)}")

tavily_count = sum(1 for r in results if r.get('api') == 'Tavily')
gnews_count = sum(1 for r in results if r.get('api') == 'GNews')
bing_count = sum(1 for r in results if r.get('api') == 'Bing')

print(f"Tavily: {tavily_count}, GNews: {gnews_count}, Bing: {bing_count}")

print("\nFirst 3 results:")
for r in results[:3]:
    print(f"  [{r['api']}] {r['title'][:40]}... | {r['publishedAt']}")
