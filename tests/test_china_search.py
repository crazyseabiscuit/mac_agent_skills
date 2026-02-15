#!/usr/bin/env python3
"""Test for china-search skill."""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the search module
import importlib.util
spec = importlib.util.spec_from_file_location(
    "china_search",
    Path(__file__).parent.parent / "skills" / "china-search" / "china_search.py"
)
china_search = importlib.util.module_from_spec(spec)
spec.loader.exec_module(china_search)


def test_search_function_exists():
    """Test that search function is defined."""
    assert hasattr(china_search, 'search_china_content'), "search_china_content function not found"
    print("✅ search_china_content function exists")


def test_search_returns_list():
    """Test that search returns a list."""
    result = china_search.search_china_content("test", "all", 1)
    assert isinstance(result, list), "search_china_content should return a list"
    print("✅ search_china_content returns a list")


def test_script_has_main():
    """Test script has main function."""
    assert hasattr(china_search, 'main'), "main function not found"
    print("✅ main function exists")


def test_helper_functions_exist():
    """Test helper functions exist."""
    functions = [
        'search_douban_movie',
        'search_douban_tv', 
        'search_weibo_entertainment',
        'search_bing_china'
    ]
    for func in functions:
        assert hasattr(china_search, func), f"{func} not found"
    print("✅ All helper functions exist")


def test_skill_markdown_exists():
    """Test SKILL.md documentation exists."""
    skill_path = Path(__file__).parent.parent / "skills" / "china-search" / "SKILL.md"
    assert skill_path.exists(), "SKILL.md not found"
    content = skill_path.read_text()
    assert "china-search" in content, "SKILL.md should contain skill name"
    print("✅ SKILL.md documentation exists and is valid")


if __name__ == "__main__":
    print("🧪 Testing china-search skill...\n")
    
    try:
        test_search_function_exists()
        test_search_returns_list()
        test_script_has_main()
        test_helper_functions_exist()
        test_skill_markdown_exists()
        
        print("\n✨ All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        sys.exit(1)
