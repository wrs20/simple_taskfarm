Simple Task Farmer
==================
Copyright 2019, WR Saunders, wrs20@bath.ac.uk; James Grant, rjg20@bath.ac.uk

Simple Batch
------------

Tool to launch a serial process in all directories that match a glob. Execute with
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
If you wish to run a script then the executable include the shell, and absolute path:

::
    bash /absolute/path/to/my_script.sh arg1 arg2 etc

Task Batch
----------

Tool to launch parallel processes in all directories that match a glob.  Execute with
::
    python task_batch.py <NUM_CONCURENT_PARALLEL_PROCS> <glob_pattern> <executable>

Again if we have directories:
::
    
    abc1
    abc2
    abc3
    abc4

and we want to launch a two process task in each directory that executes ``echo 'Hello World!'`` using a total of 2 concurrent parallel tasks we launch:
::
    python task_batch.py 2 'abc*' mprun -n 2 echo 'Hellow World!'

The conditions for the glob_pattern and executable are the same as for simple batch above.
