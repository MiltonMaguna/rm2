from dl_collector_job.config import PATH
from dl_collector_job.libs.utils import _run_command


class JobDL:
    def __init__(self, data: dict) -> None:
        """Deadline Job Data Layer."""
        self._path = data
        self._cached_details = None

    def __str__(self) -> str:
        """Returns job name."""
        return f'Render Layer: {self._path["Name"]}'

    # Job

    def job_id(self) -> str:
        """Returns job id."""
        return self._path.get('ID', None)

    def job_name(self) -> str:
        """Returns job name."""
        # return self._path['Name']
        return self._path.get('JobName', None)

    def batch_name(self) -> str:
        """Returns job name."""
        return self._path.get('BatchName', None)

    def version_name(self) -> str:
        """Returns job name."""
        _version = self._path.get('BatchName', None).split('_')[-1]
        return _version[1:]

    def rnd_layer(self) -> str:
        """Returns job render layer."""
        rnd_layer = self.job_name().rsplit('RND', 1)[-1]
        return f'RND{rnd_layer}'

    def frames(self) -> str:
        """Returns job frames."""
        return self._path.get('FramesList', None)

    def user(self) -> str:
        """Returns user name."""
        return self._path.get('UserName', None)

    def status(self) -> str:
        """Returns job status."""
        return self._path.get('Status', None)

    def job_progress(self) -> str:
        """Returns job progress."""
        return self.job_details().get('Progress', None)

    def job_errors(self) -> str:
        """Returns job errors."""
        return self.job_details().get('Errors', None)

    # Job Details

    def job_details(self) -> dict:
        """Returns job details."""
        if self._cached_details is None:
            self._cached_details = self._get_job_details(self.job_id())
        return self._cached_details

    def _get_job_details(self, job_id: str) -> dict:
        """Get the details of a specific job."""

        command = f'{PATH} -GetJobDetails {job_id}'
        output = _run_command(command)
        output_str = output.decode('utf-8')

        current_dict = {}

        for line in output_str.splitlines():
            line = line.strip()
            if not line:
                continue

            _line = line.split(':', 1)
            if len(_line) != 2:
                continue

            key, value = _line
            current_dict[key] = value
        return current_dict

    # Task States

    def task_completed(self) -> str:
        """Returns task completed."""
        return self.job_details().get('Completed', None)

    def task_failed(self) -> str:
        """Returns task failed."""
        return self.job_details().get('Failed', None)

    def task_pending(self) -> str:
        """Returns task pending."""
        return self.job_details().get('Pending', None)

    def task_queued(self) -> str:
        """Returns task queued."""
        return self.job_details().get('Queued', None)

    def task_rendering(self) -> str:
        """Returns task rendering."""
        return self.job_details().get('Rendering', None)

    def task_suspended(self) -> str:
        """Returns task suspended."""
        return self.job_details().get('Suspended', None)

    # Extras
    def output_directories(self) -> str:
        """Returns output directories."""
        return self._path.get('OutputDirectories', None)

    def files(self) -> str:
        """Returns maya files."""
        return self._path.get('AuxiliarySubmissionFileNames', None)
