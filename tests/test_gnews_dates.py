import os
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

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
os.environ["GNEWS_API_KEY"] = config.get("gnews.api_key", "YOUR_GNEWS_API_KEY_HERE")

from search_news import search_gnews

results = search_gnews("Trump", os.getenv("GNEWS_API_KEY"), 5)
print(f"GNews returned {len(results)} results\n")

cutoff = datetime.now(timezone.utc) - timedelta(days=3)
print(f"Cutoff date (3 days ago): {cutoff}\n")

for r in results:
    date_str = r['publishedAt']
    try:
        parsed = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        within_range = parsed >= cutoff
        print(f"{'✓' if within_range else '✗'} {date_str} | {r['title'][:50]}")
    except Exception as e:
        print(f"✗ {date_str} | Parse error: {e}")
