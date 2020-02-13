#!/usr/bin/env python3
import sys
import glob
import argparse
import os
import subprocess
import time


def get_args():

    parser = argparse.ArgumentParser(
        description="Simple task farmer that launches an executable in a set of directories."
    )

    parser.add_argument("n", type=int, help="Number of concurrent processes")
    parser.add_argument("--glob", type=str, default="*", help="Glob to use to discover directories, default '*'.")
    parser.add_argument(
        "--pause-time",
        type=float,
        default="1.0",
        help="Minimum time to sleep for between launching jobs, default 1.0s.",
    )
    parser.add_argument(
        "--poll-time",
        type=float,
        default="10.0",
        help="Time to sleep for between polling running jobs to check for completion, default 10.0s.",
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress printing to stdout.")
    parser.add_argument("cmd", nargs=argparse.REMAINDER, help="Executable and parameters.")
    a = parser.parse_args()
    return a


def get_dirs(glob_pattern):
    """
    Get the dirs that match the pattern.
    """

    dirs = glob.glob(os.path.expanduser(glob_pattern))
    dirs = [dx for dx in dirs if os.path.isdir(dx)]

    return dirs


def execute(exec_cmd, sleep=1):
    """
    Execute the passed command in the current working directory.

    Optional 'sleep' argument to allow delay between jobs
    """
    # execute the command
    with open("stdout", "w") as stdout:
        with open("stderr", "w") as stderr:
            p = subprocess.Popen(exec_cmd, stdout=stdout, stderr=stderr)

    # default sleep
    time.sleep(sleep)

    return p


def poll(running, finished, sleep=10):
    """
    Poll currently 'running' subprocesses to check completion

    Poll each running subprocess if finished move to finished

    If none finished then sleep for default 10s
    """

    completed = 0

    for idx, process in enumerate(running):
        p = process.poll()
        if p != None:
            finished.append(running.pop(idx))
            completed += p

    if completed == 0:
        time.sleep(sleep)


def main():

    # store the cwd to be able to return to it.
    root_dir = os.path.abspath(os.getcwd())

    args = get_args()
    if not args.quiet:
        print("-" * 80)
        print("root directory:", root_dir)
        print("command: " + " ".join(args.cmd))
        for arg in vars(args):
            if arg != "cmd":
                print(arg + ":", getattr(args, arg))
        print("-" * 80)

    # get all the directories
    dirs = get_dirs(args.glob)

    run_dirs = []
    running = []
    finished = []

    # for each dir
    while len(dirs) > 0:

        if len(running) < args.n:

            dirx = dirs.pop(0)

            # cd into the dir
            os.chdir(dirx)

            if not args.quiet:
                print(os.path.abspath(os.getcwd()))

            # launch job
            running.append(execute(args.cmd, args.pause_time))

            # return to the root
            os.chdir(root_dir)

        else:

            poll(running, finished, args.poll_time)

    while len(running) > 0:
        poll(running, finished, args.poll_time)


if __name__ == "__main__":
    main()
