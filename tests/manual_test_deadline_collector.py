#!/usr/bin/env python
# ----------------------------------------------------------------------------------------
# Manual test script for deadline_collector.py
# ----------------------------------------------------------------------------------------

import sys
import os

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def test_render_collector_manually():
    """Manual test of RenderCollector functionality"""
    try:
        # Mock the JSON file path to use our test data
        from unittest.mock import patch

        test_json_file = os.path.join(
            os.path.dirname(__file__), "test_data", "jobs_KIT_0070_MayaBatch.json"
        )

        print("🧪 Manual Test: RenderCollector")
        print("=" * 50)
        print(f"Using test JSON file: {test_json_file}")

        # Check if test file exists
        if not os.path.exists(test_json_file):
            print(f"❌ Test file not found: {test_json_file}")
            return False

        # Patch the json_file variable to use our test file
        with patch(
            "render_manager.core.dl_collector_job.deadline_collector.json_file",
            test_json_file,
        ):
            from rm2.render_manager.core.dl_collector_job.deadline_collector import (
                RenderCollector,
            )

            # Create collector instance
            collector = RenderCollector()

            # Test all methods
            print(f"\n📋 Testing RenderCollector methods:")
            print(f"   Name: {collector.name()}")
            print(f"   Path: {collector.path()}")
            print(f"   Suffix: {collector.suffix()}")
            print(f"   ROL Layer: {collector.rol_layer()}")
            print(f"   ROL Main: {collector.rol_main()}")
            print(f"   Prefix ROL Layer: {collector.prefix_rol_layer()}")
            print(f"   Version: {collector.version()}")
            print(f"   Int Version: {collector.int_version()}")
            print(f"   Name Version: {collector.name_version()}")
            print(f"   AOVs: {collector.aovs()}")
            print(f"   AOVs count: {len(collector.aovs())}")
            print(f"   OIIO Action: {collector.oiio_action()}")

            print(f"\n📝 String representation:")
            print(f"   {collector}")

            print(f"\n✅ Manual test completed successfully!")
            return True

    except Exception as e:
        print(f"❌ Manual test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_json_loading():
    """Test JSON loading functionality"""
    print("\n🧪 Testing JSON Loading")
    print("=" * 30)

    try:
        from rm2.render_manager.core.dl_collector_job.deadline_collector import (
            RenderCollector,
        )

        # Test with valid JSON file
        test_json_file = os.path.join(
            os.path.dirname(__file__), "test_data", "jobs_KIT_0070_MayaBatch.json"
        )

        collector = RenderCollector.__new__(RenderCollector)  # Create without __init__
        data = collector.load_json(test_json_file)

        print(f"✅ Successfully loaded JSON data:")
        print(f"   Path: {data.get('path', 'N/A')}")
        print(f"   Name: {data.get('name', 'N/A')}")
        print(f"   AOVs count: {len(data.get('aovs', []))}")

        # Test with non-existent file
        print(f"\n🧪 Testing with non-existent file...")
        data_empty = collector.load_json("non_existent_file.json")
        print(f"   Result for non-existent file: {data_empty}")

        return True

    except Exception as e:
        print(f"❌ JSON loading test failed: {e}")
        return False


def main():
    """Run all manual tests"""
    print("🚀 Starting Manual Tests for deadline_collector.py")
    print("=" * 60)

    success = True

    # Test JSON loading
    if not test_json_loading():
        success = False

    # Test RenderCollector
    if not test_render_collector_manually():
        success = False

    print("\n" + "=" * 60)
    if success:
        print("🎉 All manual tests passed!")
    else:
        print("💥 Some tests failed!")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
