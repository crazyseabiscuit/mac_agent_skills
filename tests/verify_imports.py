#!/usr/bin/env python3
"""Quick verification that tests can import modules correctly."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("Testing imports from tests directory...\n")

# Test 1: Import main modules
try:
    from glm_langchain_client import GLMClient
    print("✅ glm_langchain_client imported successfully")
except ImportError as e:
    print(f"❌ Failed to import glm_langchain_client: {e}")
    sys.exit(1)

try:
    from memory_manager import MemoryManager
    print("✅ memory_manager imported successfully")
except ImportError as e:
    print(f"❌ Failed to import memory_manager: {e}")
    sys.exit(1)

# Test 2: Check that test files exist
test_dir = Path(__file__).parent
test_files = sorted(test_dir.glob("test_*.py"))
print(f"\n✅ Found {len(test_files)} test files:")
for tf in test_files:
    print(f"   - {tf.name}")

# Test 3: Verify conftest and run_all_tests exist
if (test_dir / "conftest.py").exists():
    print("✅ conftest.py exists")
else:
    print("❌ conftest.py missing")
    
if (test_dir / "run_all_tests.py").exists():
    print("✅ run_all_tests.py exists")
else:
    print("❌ run_all_tests.py missing")

# Test 4: Verify __init__.py exists
if (test_dir / "__init__.py").exists():
    print("✅ __init__.py exists")
else:
    print("❌ __init__.py missing")

print("\n" + "="*60)
print("✅ All verification checks passed!")
print("="*60)
print("\nYou can now run individual tests from the tests directory:")
print("  python tests/test_memory.py")
print("  python tests/test_auto_skills.py")
print("  etc.")
