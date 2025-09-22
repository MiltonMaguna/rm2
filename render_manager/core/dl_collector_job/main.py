from arcane_api.api import get_projects
from dl_collector_job.collector_jobs import collect_jobs
from dl_collector_job.config import STATUS
from qt_log.stream_log import get_stream_logger

from arcane import get_session

log = get_stream_logger("Deadline Info")


def get_pid_project() -> int:
    """Get the project ID."""
    projects = get_projects()

    temp = {}
    for id, project in enumerate(reversed(list(projects))):
        print(f" {id} - {project['name']}")
        temp[id] = project["pid"]

    _pid = input("Select the project ID: ")
    return temp[int(_pid)]


def get_seq(pid):
    """Get the sequence."""
    session = get_session()
    session.initialize_project(pid)

    temp = {}
    for id, seq in enumerate((session.sequences())):
        print(f" {id} - {seq['name']}")
        temp[id] = seq["name"]

    _seq = int(input("Select the sequence: "))
    return temp[_seq]


def get_shot(pid, seq):
    """Get the shot."""
    session = get_session()
    session.initialize_project(pid)

    temp = {}
    for id, shots in enumerate(session.shots_from_sequence(seq)):
        print(f" {id} - {shots['name']}")
        temp[id] = shots["name"]

    _seq = int(input("Select the sequence: "))
    return temp[_seq]


def select_plugin():
    """Select the plugin."""
    plugins = ["MayaBatch", "Nuke"]

    for id, plugin in enumerate(plugins):
        print(f" {id} - {plugin}")

    _plugin = int(input("Select plugin: "))
    return plugins[_plugin]


def select_status():
    """Select the status."""
    for id, status in enumerate(STATUS):
        print(f" {id} - {status}")

    _status = int(input("Select status: "))
    return STATUS[_status]


def run():
    """Run the Deadline collector job."""
    pid = get_pid_project()
    seq = get_seq(pid)
    shot = get_shot(pid, seq)
    plugin_name = select_plugin()
    # status = select_status()

    print(f"pid: {pid}")
    print(f"seq: {seq}")
    print(f"shot: {shot}")
    print(f"plugin_name: {plugin_name}")
    # print(f'status: {status}')

    log.info(f"Collecting jobs for {seq}_{shot} using {plugin_name} plugin...")
    jobs_dl = collect_jobs(seq, shot, plugin_name)

    for status, jobs in jobs_dl.items():
        log.info(f"{'-' * 50}")
        log.info(f"STATUS - {status}")

        for job in jobs:
            if status == STATUS[-2]:  # STATUS RENDERING
                log.info(f"Job: {job.job_name()} - {job.frames()}")
                log.info(f"Progress: {job.job_progress()}")
            else:
                log.info(f"Job: {job.job_name()} - {job.frames()}")
                log.info(f"Output directory: {job.output_directories()}")

        log.info(f"{'-' * 50}")


run()
