Simple Task Farmer
==================
Copyright 2019, WR Saunders, wrs20@bath.ac.uk; James Grant, rjg20@bath.ac.uk

Installation
------------

To install these tools with pip:
::
    pip install --upgrade --no-cache-dir git+https://github.com/wrs20/simple_taskfarm@master


Task Batch
----------

Tool to launch processes in parallel with one process per directory in all directories that match a glob.  Execute with
::
    task-batch --glob <glob_pattern> <NUM_CONCURENT_PARALLEL_PROCS> <executable>

If we have directories:
::
    
    abc1
    abc2
    abc3
    abc4

and we want to launch a two process task in each directory that executes ``echo 'Hello World!'`` using a total of 2 concurrent parallel tasks we launch:
::
    task-batch --glob 'abc*' 2 echo 'Hello World!'

The conditions for the glob_pattern and executable are the same as for simple batch above. The default glob is `'*'`, hence we could run a command in all subdirectories of a directory with:
::
    task-batch <NUM_CONCURENT_PARALLEL_PROCS> <executable>

Further configurable options, such as starting delay and polling delay, are listed with:
::
    task-batch --help


Simple Batch
------------
Requires MPI for Python which can be installed with:
::
    pip install mpi4py


Tool to launch a serial process in all directories that match a glob using MPI to leverage multiple nodes. Execute with
::

    mpirun -n <NUM_PROCS> python simple_batch.py <glob_pattern> <executable>


For example if we have directories
::
    
    abc1
    abc2
    abc3
    abc4

and we want to launch a process in each directory that executes ``ls -l`` using 4 MPI ranks we launch
:: 
    mpirun -n 4 python simple_batch.py 'abc*' ls -l

Note that the glob_pattern needs to be in quotes to stop shell expansion.  


Notes on running scripts
------------------------

If you wish to run a script then the executable command should include the interpreter and the absolute path to the script
::
    bash /absolute/path/to/my_script.sh arg1 arg2 etc

This requirement arises as the executable command is launched as a subprocess call.
