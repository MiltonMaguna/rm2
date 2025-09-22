# Version: 1.0
from dl_collector_job.config import PATH, STATUS
from dl_collector_job.libs.jobs import JobDL
from dl_collector_job.libs.utils import _run_command
from qt_log.stream_log import get_stream_logger

log = get_stream_logger("Deadline Collector")


def collect_jobs(seq: str, shot: str, plugin_name: str) -> dict:
    """Collects job details for a given sequence and shot using a specified plugin.

    Args:
        seq (str): The sequence identifier.
        shot (str): The shot identifier.
        plugin_name (str): The name of the plugin to use for collecting job details.

    Returns:
        dict: A dictionary where the keys are job statuses and the values are lists of JobDL objects containing job details.
    """

    task_states = get_jobs_status(f"{seq}_{shot}", plugin_name)

    jobs_dl = {}

    for status in task_states.keys():
        job_details = []
        for job in task_states[status]:
            job_details.append(JobDL(job))

        jobs_dl[status] = job_details

    return jobs_dl


def get_jobs_status(batch_name: str, plugin_name: str) -> dict:
    """Retrieve the status of jobs for a given batch and plugin.

    Args:
        batch_name (str): The name of the batch to filter jobs.
        plugin_name (str): The name of the plugin to filter jobs.

    Returns:
        dict: A dictionary where the keys are job statuses and the values are lists of job IDs.
    """

    jobs_ids = {}

    for status in STATUS:
        log.info(f"Collecting Status {status} jobs...")
        command = f"{PATH} -GetJobsFilterAnd PluginName={plugin_name} Status={status} BatchName={batch_name}"
        output = _run_command(command)

        if not output.decode("utf-8"):
            log.info("No jobs found.")
            continue

        jobs_ids[status] = parse_output(output)

    return jobs_ids


def list_to_dicts(jobs) -> list:
    """Convert a list of strings to a list of dictionaries.

    Each string in the input list should be in the format 'key=value'.
    An empty string indicates the end of a dictionary and the start of a new one.

    Args:
        jobs (list): A list of strings where each string is in the format 'key=value'.

    Returns:
        list: A list of dictionaries created from the input list of strings.
    """
    dicts = []
    current_dict = {}

    for item in jobs:
        if item == "":
            if current_dict:
                dicts.append(current_dict)
                current_dict = {}
        else:
            key, value = item.split("=", 1)
            current_dict[key] = value

    if current_dict:
        dicts.append(current_dict)

    return dicts


def parse_output(output: bytes) -> list:
    """Parse the output from deadlinecommand.exe into a dictionary.

    Args:
        output (bytes): The output from deadlinecommand.exe as a byte string.

    Returns:
        dict: A dictionary representation of the parsed output. The dictionary
              structure is determined by the sections and key-value pairs in the
              output. Sections are denoted by lines without an '=' character,
              and key-value pairs within sections are denoted by lines with an
              '=' character.
    """

    output_str = output.decode("utf-8")
    lines = output_str.split("\r\n")

    return list_to_dicts(lines)


if __name__ == "__main__":
    # -- Collect jobs status
    plugin_name = "MayaBatch"
    shot = "1410"
    seq = "UAS"

    log.info(f"Collecting jobs for {seq}_{shot} using {plugin_name} plugin...")
    jobs_dl = collect_jobs(seq, shot, plugin_name)

    dict_temp = {}

    log.info("Running jobs")

    for status, jobs in jobs_dl.items():
        log.info(f"Status: {status}")
        for job in jobs:
            log.info(f"Name: {job.job_name()}")
            log.info(f"Batch Name: {job.batch_name()}")
            log.info(f"Render Layer: {job.rnd_layer()}")
            log.info(f"Version: {job.version_name()}")
            log.info(f"Frames: {job.frames()}")
            log.info(f"User: {job.user()}")
            log.info(f"Ouput Directories: {job.output_directories()}")
            log.info(f"Files: {job.files()}")

            log.info("Task States")
            log.info(f"Progress: {job.job_progress()}")
            log.info(f"Errors: {job.job_errors()}")
            log.info(f"Task Completed: {job.task_completed()}")
            log.info(f"Task Failed: {job.task_failed()}")
            log.info(f"Task Pending: {job.task_pending()}")
            log.info(f"Task Queued: {job.task_queued()}")
            log.info(f"Task Rendering: {job.task_rendering()}")
            log.info(f"Task Suspended: {job.task_suspended()}")
            log.info("---" * 10)
