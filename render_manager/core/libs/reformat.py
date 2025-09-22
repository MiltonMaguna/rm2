# ----------------------------------------------------------------------------------------
# ACME RenderManager Nuke
# Reformat Operation Launcher
# Maximiliano Rocamora / Milton Maguna
# ----------------------------------------------------------------------------------------
import contextlib
import os

with contextlib.suppress(ImportError):
    from arcane import get_session

from pyside_ui_backpack import wait_cursor
from qt_log.stream_log import get_stream_logger
from render_manager.render.render_layer_types import Render
# from render_manager.core.deadline.python_deadline import PythonDeadline

log = get_stream_logger("RenderManager")

# TODO
# Take env [dev, prod] from current arcane env
path = "F:/nuke/arcane/dev/RenderManager/render_manager/core/deadline/job_scripts"
SCRIPT_REFORMAT = os.path.join(path, "reformat_oiio.py")


class ReformatRenderLayer:
    def __init__(self, render_layer: Render):
        """runs reformat module on this render_layer"""
        log.info(f"Submit Reformat RenderLayer {render_layer.name()}")

        self.submit(render_layer)

    @wait_cursor
    def submit(self, render_layer):
        """launch deadline python script for each aov of this render layer"""

        args = {
            "frame_range": render_layer.frame_range(),
            "resize": "50%",
        }

        info = {
            "BatchName": f"{get_session.project_folder()}_{render_layer.version()}",
        }

        # build paths
        base_path = render_layer.path()
        # fix aces-cg passed as separated arguments, collapsing spaces
        base_path = base_path.replace("_ACES - ACEScg", "_ACES_ACEScg")

        for aov_name in render_layer.aovs():
            # build deadline args, batch name, input_file, oiio action
            data = render_layer.get_aov_data(aov_name)
            info["Name"] = f"{render_layer.name()}_{aov_name}_reformat"
            input_filename = f"{data['files']}_%04d.{data['extension']}"
            args["input_file"] = os.path.join(base_path, aov_name, input_filename)
            args["input_file"] = args["input_file"].replace("\\", "/")
            args["oiio_action"] = render_layer.oiio_action()

            # submit
            dead = PythonDeadline(job_name=info["Name"])
            dead.run_job(info, args, SCRIPT_REFORMAT)
