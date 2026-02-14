import os
import sys
from pathlib import Path
import httpx

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

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

# Get API key from config
api_key = config.get("tavily.api_key", "YOUR_TAVILY_API_KEY_HERE")
query = "Tesla"

url = "https://api.tavily.com/search"
payload = {
    "api_key": api_key,
    "query": query,
    "search_depth": "basic",
    "include_answer": False,
    "max_results": 3,
    "topic": "news"
}

try:
    with httpx.Client(timeout=15) as client:
        response = client.post(url, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nFound {len(data.get('results', []))} results")
            for item in data.get("results", [])[:2]:
                print(f"- {item.get('title', 'No title')}")
                print(f"  Published: {item.get('published_date', 'No date')}")
except Exception as e:
    print(f"Error: {e}")

