import sys
from mpi4py import MPI
import numpy as np
import glob
import argparse
import os
import ctypes
import subprocess

def get_args():
    """
    This would be nice but fails when the command you want to run also has flags....
    """
    parser = argparse.ArgumentParser(
        description='Simple task farmer that launches an executable in a set of directories.')

    parser.add_argument("glob", help="Glob to use to discover directories.")
    parser.add_argument("exec", nargs='+', help="Executable and parameters.")
    a = parser.parse_args()
    return a.glob, a.exec

def get_dirs(glob_pattern):
    """
    Get the dirs that match the pattern.
    """
    if MPI.COMM_WORLD.rank == 0:
        dirs = glob.glob(os.path.expanduser(glob_pattern))
    else:
        dirs = []
    dirs2 = MPI.COMM_WORLD.bcast(dirs, 0)
    return dirs2

def get_dirs_subset(dirs):
    """
    Get the dirs for this rank.
    """

    size = MPI.COMM_WORLD.size
    rank = MPI.COMM_WORLD.rank

    ndirs = len(dirs)

    if size > ndirs:
        start = rank
        if rank >= ndirs:
            end = rank
        else:
            end = rank + 1
    else:
        f,r = divmod(ndirs, size) 
        s = np.zeros(size, ctypes.c_int64)
        s[:] = f
        s[:r] += 1
        s = np.cumsum(s)
        s -= s[0]

        start = s[rank]
        if rank < (size - 1):
            end = s[rank + 1]
        else:
            end = ndirs

    return dirs[start:end]

def execute(exec_cmd):
    """
    Execute the passed command in the current working directory.
    """
    with open('stdout', 'w') as stdout:
        with open('stderr', 'w') as stderr:
            p = subprocess.Popen(exec_cmd, stdout=stdout, stderr=stderr)
            p.wait()


if __name__ == '__main__':
    
    # get glob pattern
    glob_pattern = sys.argv[1]

    # get the command
    cmd = sys.argv[2:]
    
    # get all the directories
    dirs = get_dirs(glob_pattern)

    # get the dirs for this rank
    dirs = get_dirs_subset(dirs)
    
    # store the cwd to be able to return to it.
    root_dir = os.path.abspath(os.getcwd())
    
    # for each dir
    for dirx in dirs:

        # cd into the dir
        os.chdir(dirx)

        # execute the command
        execute(cmd)

        # return to the root
        os.chdir(root_dir)



