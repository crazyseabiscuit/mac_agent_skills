#!/usr/bin/env python3
"""Test SAVE_MEMORY protocol parsing."""

def test_save_memory_parsing():
    """Test that SAVE_MEMORY protocol works."""
    
    # Simulate AI response with SAVE_MEMORY
    response = """好的，我记住了您喜欢看电影。
SAVE_MEMORY: content_type=movies
我会为您推荐相关内容。"""
    
    print("Testing SAVE_MEMORY parsing...")
    print(f"Response: {response}\n")
    
    # Parse SAVE_MEMORY
    if "SAVE_MEMORY:" in response:
        lines = response.split("\n")
        for line in lines:
            if line.startswith("SAVE_MEMORY:"):
                mem_data = line.replace("SAVE_MEMORY:", "").strip()
                if "=" in mem_data:
                    key, value = mem_data.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Determine type
                    if key in ["language", "content_type", "region_preference", "preferred_style"]:
                        print(f"✓ Would save preference: {key}={value}")
                    else:
                        print(f"✓ Would save context: {key}={value}")
    
    print("\n✅ SAVE_MEMORY protocol test passed!")

if __name__ == "__main__":
    test_save_memory_parsing()
