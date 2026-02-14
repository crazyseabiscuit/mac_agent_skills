#!/usr/bin/env python3
"""Test runner for all test modules."""
import sys
from pathlib import Path
import subprocess

# Add parent directory to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def run_test(test_file):
    """Run a single test file."""
    print(f"\n{'=' * 80}")
    print(f"Running: {test_file.name}")
    print('=' * 80)
    
    try:
        result = subprocess.run(
            [sys.executable, str(test_file)],
            cwd=PROJECT_ROOT,
            capture_output=False,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✅ {test_file.name} passed")
            return True
        else:
            print(f"⚠️  {test_file.name} returned code {result.returncode}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏱️  {test_file.name} timed out")
        return False
    except Exception as e:
        print(f"❌ {test_file.name} failed: {e}")
        return False


def main():
    """Run all tests."""
    tests_dir = Path(__file__).parent
    test_files = sorted(tests_dir.glob("test_*.py"))
    
    print(f"\n🧪 Found {len(test_files)} test files\n")
    
    results = {}
    for test_file in test_files:
        results[test_file.name] = run_test(test_file)
    
    # Summary
    print(f"\n{'=' * 80}")
    print("📊 Test Summary")
    print('=' * 80)
    
    passed = sum(1 for v in results.values() if v)
    failed = sum(1 for v in results.values() if not v)
    
    for test_name, passed_test in sorted(results.items()):
        status = "✅" if passed_test else "⚠️"
        print(f"{status} {test_name}")
    
    print(f"\nTotal: {passed} passed, {failed} skipped/failed out of {len(results)}")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
