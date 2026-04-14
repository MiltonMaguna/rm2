import subprocess

from qt_log.stream_log import get_stream_logger

log = get_stream_logger("Deadline Collector Tools")


def _run_command(command) -> str:
    """Run given command with deadlinecommand.exe."""
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    # log.info('Running Command:')
    # log.info(command)
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
        return out
    except OSError as e:
        log.error(str(e))
        log.error(err)
