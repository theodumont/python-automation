# encoding: utf-8
"""Functions used by the cli.py script.

Makes the process of cleaning a folder easier and simplifies the
video logging process.

"""

import os
import time
import json
import subprocess
from moviepy.video.io.VideoFileClip import VideoFileClip
from progress.bar import Bar, IncrementalBar



def folder_sort(EXTENSIONS):
    r"""Sort the files into directories according to their extension.

    Create the extensions directories if they don't exist.
    """
    check_parent()
    n = get_number_files(EXTENSIONS)
    bar = IncrementalBar("Sorting files...", max=n)

    for file in os.listdir():
        time.sleep(.001)
        name, extension = os.path.splitext(file)
        if os.path.isdir(file):
            if name not in EXTENSIONS:
                move_to_dir(file, 'Folders')
            else:
                pass
        else:
            treated = False
            for directory in EXTENSIONS:
                if extension in EXTENSIONS[directory]:
                    move_to_dir(file, directory)
                    treated = True
                    break
            if not treated:
                move_to_dir(file, 'Other')
        bar.next()
    bar.finish()
    print("Files sorted by type.")


def trash_videos(time_limit, EXTENSIONS):
    r"""Trash the videos that are shorter than time_limit to get rid of
    the shooting errors.

    Parameters
    ----------
    time_limit : int
        Duration limit.
    """
    def move_to_trash(file, duration):
        r"""Move a video to trash if it is too short.

        Check if a directory named `Trash` exists in current directory. If not,
        create it. Then, move `file` in `Trash` if `duration` is smaller than
        `time_limit`.

        Parameters
        ----------
        file : string
            File to check.
        duration : int
            Duration of video file.
        """
        if duration < time_limit:
            if not os.path.isdir('Trash'):
                os.mkdir('./Trash')
            os.rename(file, os.path.join('Trash', file))
            return True
        return False

    check_parent()
    n = get_number_files(EXTENSIONS, directory='Videos')
    print(n)
    bar = IncrementalBar(f"Trashing videos of duration <= {time_limit}s...", max=n)

    nb_trashed = 0
    for file in os.listdir():
        extension = os.path.splitext(file)[1]
        if extension in EXTENSIONS['Videos']:
            with VideoFileClip(file) as clip:
                time.sleep(.001)
                duration = clip.duration
            if move_to_trash(file, duration):
                nb_trashed += 1
            bar.next()

    bar.finish()
    term = 's' * (nb_trashed >= 2)
    print(f"{nb_trashed} file{term} trashed.")


def sort_by_date():
    r"""Sort files in directories by creation date.

    The repositories will be in the form of 'YYMMDD-Day'.
    """
    check_parent()
    n = len(os.listdir())
    bar = IncrementalBar(f"Sorting files by date...", max=n)
    for file in os.listdir():
        if not os.path.isdir(file):
            time.sleep(.001)
            creation = time.localtime(os.path.getmtime(file))
            directory = time.strftime('%y%m%d-%a', creation)
            move_to_dir(file, directory)
        bar.next()

    bar.finish()
    print("Videos sorted by date.")


def move_to_dir(file, directory):
    r"""Move file to directory.

    Check if a directory named `directory` exists in current directory. If not,
    create it. Then, move `file` in `directory`.

    Parameters
    ----------
    file : string
        File to move.
    directory : string
        Target directory.
    """
    if not os.path.isdir(directory):
        os.mkdir('./{}'.format(directory))
    os.rename(file, os.path.join(directory, file))


def check_parent():
    """
    Check if 'video-logging' scripts are in cwd.
    """
    for root, dirs, files in os.walk("./"):
        if ".videolog" in files:
            raise OSError(
                "! Warning: the current directory contains the 'video-logging' scripts.\n"
                "! Moving files may do bad things.\n"
                "! Please move the 'video-logging' folder somewhere else then navigate to the folder you want to sort using the 'cd' command."
            )


def get_number_files(EXTENSIONS, directory='all'):
    """
    Return number of file of a certain type in cwd.
    """
    if directory == 'all':
        return len(os.listdir())
    count = 0
    for file in os.listdir():
        extension = os.path.splitext(file)[1]
        if extension in EXTENSIONS[directory]:
            count += 1
    return count
