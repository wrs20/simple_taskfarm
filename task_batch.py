import sys
import glob
import argparse
import os
import subprocess
import time

def get_args():
    """
    This would be nice but fails when the command you want to run also has flags....
    """
    parser = argparse.ArgumentParser(
        description='Simple task farmer that launches an executable in a set of directories.')

    parser.add_argument("glob", help="Glob to use to discover directories.")
    parser.add_argument("exec_cmd", nargs='+', help="Executable and parameters.")
    a = parser.parse_args()
    return a.glob, a.exec_cmd

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
    with open('stdout', 'w') as stdout:
        with open('stderr', 'w') as stderr:
            p = subprocess.Popen(exec_cmd, stdout=stdout, stderr=stderr)


    # default sleep
    time.sleep( sleep )

    return p

def poll(running, finished, sleep=10):
    """
    Poll currently 'running' subprocesses to check completion

    Poll each running subprocess if finished move to finished

    If none finished then sleep for default 10s
    """

    completed = 0

    for idx, process in enumerate(running):
        poll = process.poll()
        if poll != None:
            finished.append( running.pop(idx) )
            completed += poll

    if completed == 0:
        time.sleep( sleep )
    

if __name__ == '__main__':
    
    # get total number of concurrent parallel tasks
    max_jobs = sys.argv[1]

    # get glob pattern
    glob_pattern = sys.argv[2]

    # get the command
    cmd = sys.argv[3:]
    
    # get all the directories
    dirs = get_dirs(glob_pattern)

    run_dirs = []

    # store the cwd to be able to return to it.
    root_dir = os.path.abspath(os.getcwd())

    print(root_dir)

    running = []
    finished = []    


    # for each dir
    while len(dirs) > 0:

        if len(running) < max_jobs:

            dirx = dirs.pop(0)

            # cd into the dir
            os.chdir(dirx)

            print(os.path.abspath(os.getcwd()))
            print(cmd)
            # launch job
            running.append( execute(cmd) )

            # return to the root
            os.chdir(root_dir)

            print(os.path.abspath(os.getcwd()))

        else:

            poll(running, finished)
            
    while len(running) > 0:
        poll(running, finished)


