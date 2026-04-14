# ----------------------------------------------------------------------------------------
# Deadline Python Jobs Submitter
# ----------------------------------------------------------------------------------------
# from acme.core.cmd.deadline.deadline_command import deadline_command

from PreRender.pre_render_tool.libs.deadline.deadline_command import deadline_command
from PreRender.pre_render_tool.libs.deadline.deadline_command import (
    job_filepath,
    write_job_file,
)

from qt_log.stream_log import get_stream_logger

log = get_stream_logger("PythonSubmitter")


class PythonDeadline:
    """command line deadline submitter"""

    def __init__(self, job_name):
        self.job_name = job_name

    def job_info(self, custom_info):
        """returns constructed info dict from its defaults values"""
        info = {
            "Plugin": "Python",
            "ForceReloadPlugin": "false",
            "Frames": "1001",
            "ChunkSize": "1",
            "Priority": "50",
            "Pool": "comp",
            "Group": "nuke",
            "TaskTimeoutMinutes": "0",
            "Name": "unnamed",
            "EnableAutoTimeout": "False",
            "ConcurrentTasks": "1",
            "LimitConcurrentTasksToNumberOfCpus": "True",
            "MachineLimit": "0",
            "JobDependencies": "",
            "OnJobComplete": "Nothing",
            "Department": "Comp",
            "Comment": "Reformat oiio 4k2k",
            "InitialStatus": "Active",
            "BatchName": "BatchRender",
            # 'OutputFilename0': "",
            # 'OutputDirectory0': ""
        }

        for k, v in custom_info.items():
            info[k] = v

        return info

    def job_plugin(self, args):
        """returns constructed plugin dict from its defaults values
        Note:
            the arguments value is a feature only for python jobs, any extra
            key=val argument passed is passed to the script as a sys.args
        """
        return {
            "Version": "3.11",
            "StrictErrorChecking": "False",
            "MaxProcessors": "0",
            "IgnoreError211": "False",
            "OutputFilePrefix": "",
            "OutputPath": "",
            "Arguments": "".join(f"{key}={val} " for key, val in args.items()),
        }

    def run_job(self, extra_info, extra_plugin, script_file):
        """adds a job files to the system for submission
        Args:
            info (dict) extra values for deadline info file
            plugin (dict) extra values for deadline plugin file
        Returns:
            out
        """

        info = self.job_info(extra_info)
        plugin = self.job_plugin(extra_plugin)
        info_filepath = job_filepath(self.job_name, "reformat_info")
        plugin_filepath = job_filepath(self.job_name, "reformat_plugin")
        write_job_file(info_filepath, info)
        write_job_file(plugin_filepath, plugin)

        cmd = f'''"{info_filepath} " "{plugin_filepath}" "{script_file}"'''

        log.info(f"Running Python Command: {cmd}")

        return deadline_command(cmd)
