# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
import os
import sys
import subprocess

sys.path.append("C:/Python/Python311/Lib/site-packages")
sys.path.append("F:/maya/arcane/prod/arcane_api")

from qt_log.stream_log import get_stream_logger

log = get_stream_logger("PythonScriptJob")

OIIO = "F:/main/tools/oiio/oiiotool.exe"

OIIO_ARGS = {"reformat": "--resize:filter=cubic", "resample": "--resample:interp=0"}


def get_argument(name):
    """returns the value of given argument name from sysargs"""
    for arg in sys.argv:
        if arg.startswith(name):
            return arg.split("=")[1]
    return None


def reformat(*args, **kwargs):
    log.info("Running Reformat Script")

    log.info(f"Python {sys.version} {sys.executable}")

    log.info("Commands Passed")
    log.info(sys.argv)

    FRAME_RANGE = get_argument("frame_range")
    RESIZE = get_argument("resize")
    INPUT_FILE = get_argument("input_file")
    action = get_argument("oiio_action")

    INPUT_FILE = INPUT_FILE.replace("_ACES_ACEScg", "_ACES - ACEScg")
    OUTPUT_FILE = INPUT_FILE.replace("/CG/", "/REFORMAT/")
    log.info(f"{INPUT_FILE=}")
    log.info(f"{OUTPUT_FILE=}")

    # create output folder
    if not os.path.exists(os.path.dirname(OUTPUT_FILE)):
        os.makedirs(os.path.dirname(OUTPUT_FILE))

    cmd = f'{OIIO} --frames {FRAME_RANGE} "{INPUT_FILE}" \
        {OIIO_ARGS[action]} {RESIZE} -o "{OUTPUT_FILE}"'

    _run_oiio_command(cmd)

    log.info(f"{cmd}")
    log.info("Closing Reformat oiio Script")


def _run_oiio_command(command):
    """run given command with deadlinecommand.exe"""
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    log.info("Running Command:")
    log.info(command)
    try:
        sp = subprocess.Popen(
            command,
            startupinfo=startupinfo,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = sp.communicate()
        sp.stdin.close()
        log.info(out)
        log.info(err)
    except OSError as e:
        log.error(str(e))


reformat()
