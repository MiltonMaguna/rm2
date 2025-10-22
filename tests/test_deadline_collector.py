from rm2.render_manager.core.dl_collector_job.deadline_collector import (
    collect_render_layers_from_deadline,
)
import json

# json_file_path = r'D:\repo\rm2\tests\test_data\jobs_UAS_1410_MayaBatch.json'
json_file_path = r"D:\repo\rm2\tests\test_data\jobs_KIT_0070_MayaBatch.json"


def test_render_collector_manually():
    """Test RenderCollector manually"""
    print("\n🧪 Testing RenderCollector")
    print("=" * 30)

    try:
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Collect render layers
        render_layers = collect_render_layers_from_deadline(data)

        # print(f"✅ Collected {len(render_layers)} render layers:")
        for rol in render_layers.keys():
            print(f"Render Layer: {rol}")

            for layer in render_layers[rol]:
                # print(f"Full Name: {layer.full_name()}")
                print(f"Int Version: {layer.int_version()}")
                # print(f"Rol Main: {layer.rol_main()}")
                # print(f"Rol layer: {layer.rol_layer()}")
                # print(f"Name:{layer.name()}")
                # print(f"Frames: {layer.frames()}")
                # print(f"Frame Range: {layer.frame_range()}")
                # print(f"Output: {layer.path()}")
                # print(f"Progress: {layer.progress_bar()}")
                # print(f"User: {layer.user()}")
                # print(f"Version: {layer.version()}")
                # print(f"Name Version: {layer.name_version()}")
                # print('-'*30)

    except ImportError:
        print("❌ ImportError: RenderCollector module not found.")


test_render_collector_manually()
