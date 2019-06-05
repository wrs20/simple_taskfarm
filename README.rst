Simple Task Farmer
==================

Tool to launch a process in all directories that match a glob. Execute with
::

    mpirun -n 4 python simple_batch.py <glob_pattern> <executable>


For example if we have directories
::
    
    abc1
    abc2
    abc3
    abc4

and we want to launch a process in each directory that executes ``ls -l`` using 4 MPI ranks we launch
:: 
    mpirun -n 4 python simple_batch.py 'abc*' ls -l



    





