#!/usr/bin/env python
# ----------------------------------------------------------------------------------------
# Test runner for deadline_collector tests
# ----------------------------------------------------------------------------------------

import sys
import os

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def run_tests():
    """Run the deadline_collector tests"""
    try:
        import pytest
        
        # Run the specific test file
        test_file = os.path.join(os.path.dirname(__file__), 'test_deadline_collector.py')
        
        print("Running deadline_collector tests...")
        print(f"Test file: {test_file}")
        print("-" * 50)
        
        # Run pytest with verbose output
        exit_code = pytest.main([
            '-v',           # verbose output
            '-s',           # don't capture output
            '--tb=short',   # shorter traceback format
            test_file
        ])
        
        if exit_code == 0:
            print("\n✅ All tests passed!")
        else:
            print(f"\n❌ Tests failed with exit code: {exit_code}")
            
        return exit_code
        
    except ImportError:
        print("❌ pytest not found. Please install pytest:")
        print("pip install pytest")
        return 1
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1

if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
