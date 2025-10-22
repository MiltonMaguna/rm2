# example file on how to send a cache export job via command line
import os

from rm2.render_manager.core.deadline.python_deadline import PythonDeadline

path = "F:/nuke/arcane/dev/RenderManager/render_manager/core/deadline/job_scripts"
SCRIPT = os.path.join(path, "reformat_proxy_2k.py")


args = {
    "frame_range": "1001-1050",
    "resize": "50%",
    "input_file": "I:/SAND/SEQ/DEV/render_path/Comp/Frames/CG/RND_TEST/SBX_DEV_render_path_v0001_ACES - ACEScg/beauty/RND_TEST_beauty_####.exr",
    "output_file": "I:/SAND/SEQ/DEV/render_path/Comp/Frames/CG/RND_TEST/SBX_DEV_render_path_v0001_ACES - ACEScg/beauty/RND_TEST_beauty_####.exr",
    "filter": "cubic",
    "oiio_action": "reformat",
}

info = {
    "Name": "test-ref2",
    "BatchName": "Test_NukeReformat_oiio",
}


def submit():
    """Runs job"""
    dead = PythonDeadline("job_display_name")
    dead.run_job(info, args, SCRIPT)


if __name__ == "__main__":
    submit()
