# example file on how to send a cache export job via command line
import os

from render_manager.core.deadline.python_deadline import PythonDeadline

path = "F:/nuke/arcane/dev/RenderManager/render_manager/core/deadline/job_scripts"
SCRIPT = os.path.join(path, 'reformat_oiio.py')


args = {
    'frame_range': '999-1004',
    'resize': '50%',
    'input_file': r"G:/Temp/nuke/test_oiio/BTY/RND_BG_BTY_beauty_%04d.exr",
    'output_file': r"G:/Temp/nuke/test_oiio/BTY_REFORMAT/RND_BG_BTY_beauty_%04d.exr",
    'filter': 'cubic',
}

info = {
    'Name': 'test-ref2',
    "BatchName": 'Test_NukeReformat_oiio',
}


def submit():
    ''' Runs job '''
    dead = PythonDeadline('job_display_name')
    dead.run_job(info, args, SCRIPT)


if __name__ == '__main__':
    submit()
