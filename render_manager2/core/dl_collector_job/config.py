"""Configuration file for Deadline Collector Job.

Attributes:
    PATH (str): The file path to the Deadline command executable.
    ITEMS (list): A list of items related to the job, such as 'Job', 'Task States', 'Output Directories', and 'Auxiliary Files'.
    STATUS (list): A list of possible job statuses, including 'Completed', 'Failed', 'Pending', 'Queued', 'Rendering', and 'Suspended'.
"""

PATH = r'C:\Program Files\Thinkbox\Deadline10\bin\deadlinecommand.exe'
ITEMS = ['Job', 'Task States', 'Output Directories', 'Auxiliary Files']
STATUS = ['Completed', 'Failed', 'Queued', 'Rendering', 'Suspended']
