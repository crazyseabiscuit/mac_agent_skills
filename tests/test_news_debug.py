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

from search_news import search_tavily, search_gnews

print("Testing Tavily...")
tavily_results = search_tavily("Tesla", "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", 3)
print(f"Tavily returned {len(tavily_results)} results")
for r in tavily_results[:2]:
    print(f"  - {r['title'][:50]}... | {r['publishedAt']} | {r['api']}")

print("\nTesting GNews...")
gnews_results = search_gnews("Tesla", "6248bb535bee47b909c5976e98cba7a1", 3)
print(f"GNews returned {len(gnews_results)} results")
for r in gnews_results[:2]:
    print(f"  - {r['title'][:50]}... | {r['publishedAt']} | {r['api']}")
