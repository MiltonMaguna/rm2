import json
import os
from datetime import datetime

from dl_collector_job.collector_jobs import collect_jobs
from dl_collector_job.config import STATUS
from qt_log.stream_log import get_stream_logger

log = get_stream_logger("collect_by_shot - Deadline Collector Job")


def collect_by_shot(seq: str, shot: str, plugin_name: str) -> None:
    """Collects job details for a given sequence and shot using a specified plugin.

    Args:
        seq (str): The sequence identifier.
        shot (str): The shot identifier.
        plugin_name (str): The name of the plugin to use for collecting job details.
    """

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

    # Create JSON file with jobs data
    create_jobs_json(jobs_dl, seq, shot, plugin_name)


def create_jobs_json(
    jobs_dl: dict, seq: str, shot: str, plugin_name: str, output_dir: str = None
) -> str:
    """Creates a JSON file with job details from jobs_dl dictionary.

    Args:
        jobs_dl (dict): Dictionary containing job data organized by status.
        seq (str): The sequence identifier.
        shot (str): The shot identifier.
        plugin_name (str): The name of the plugin used.
        output_dir (str, optional): Directory to save the JSON file. If None, saves in current directory.

    Returns:
        str: Path to the created JSON file.
    """

    # Prepare JSON data structure
    json_data = {
        "metadata": {
            "sequence": seq,
            "shot": shot,
            "plugin": plugin_name,
            "collection_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_jobs": sum(len(jobs) for jobs in jobs_dl.values()),
        },
        "jobs_by_status": {},
    }

    # Convert job objects to serializable dictionaries
    for status, jobs in jobs_dl.items():
        json_data["jobs_by_status"][status] = []

        for job in jobs:
            job_data = {
                "job_name": job.job_name(),
                "batch_name": job.batch_name(),
                "render_layer": job.rnd_layer(),
                "version": job.version_name(),
                "user": job.user(),
                "frames": job.frames(),
                "output_directories": job.output_directories(),
            }

            # Add progress for rendering jobs
            if status == STATUS[-2]:  # STATUS RENDERING
                job_data["progress"] = job.job_progress()

            json_data["jobs_by_status"][status].append(job_data)

    # Create filename and path
    filename = f"jobs_{seq}_{shot}_{plugin_name}.json"

    if output_dir is None:
        output_dir = os.getcwd()

    file_path = os.path.join(output_dir, filename)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Write JSON file
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        log.info(f"JSON file created: {file_path}")
        return file_path

    except Exception as e:
        log.error(f"❌ Error creating JSON file: {e}")
        raise


def collect_by_shot_with_json(
    seq: str, shot: str, plugin_name: str, output_dir: str = None
) -> str:
    """Collects job details and creates a JSON file with the results.

    Args:
        seq (str): The sequence identifier.
        shot (str): The shot identifier.
        plugin_name (str): The name of the plugin to use for collecting job details.
        output_dir (str, optional): Directory to save the JSON file.

    Returns:
        str: Path to the created JSON file.
    """

    log.info(f"Collecting jobs for {seq}_{shot} using {plugin_name} plugin...")

    jobs_dl = collect_jobs(seq, shot, plugin_name)

    if not jobs_dl:
        log.warning("No jobs found for the specified sequence and shot.")
        return ""

    log.info(f"Collected {sum(len(jobs) for jobs in jobs_dl.values())} jobs.")
    return create_jobs_json(jobs_dl, seq, shot, plugin_name, output_dir)


if __name__ == "__main__":
    # Example usage
    sequence = "KIT"
    shot = "0070"
    plugin = "MayaBatch"  # or any other plugin you want to use

    # Option 1: Use original function (now also creates JSON)
    # collect_by_shot(sequence, shot, plugin)

    # Option 2: Use new function with custom output directory
    json_file_path = collect_by_shot_with_json(
        sequence, shot, plugin, output_dir=r"C:\temp\deadline_jobs"
    )

    print(f"JSON file created at: {json_file_path}")
