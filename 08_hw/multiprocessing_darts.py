from random import uniform
from math import sqrt
from time import time
from multiprocessing import Process, Queue
import numpy as np

def dart_thrower(tests, nprocs):
    ''' Give "dart_thrower" a dummy list of darts (e.g. to throw 200,000 darts,
    	input range(200000) ). "nprocs" is the number of processors.
        
		Returns the total darts thrown inside the circle.
	'''
	
    def worker(test):
        """ The worker function, invoked in a process. 'test' is a
            list of dummy values.
        """
        num_in_circle = 0
        for j in test:
            num_in_circle += throw_dart()
        
        out_q.put(num_in_circle)
        
    def throw_dart():
        ''' Throw a dart. Find a random position in the unit square for it
            to fall. Test if it falls within the circle by calculating the
            distance from the origin (0.5,0.5) to the dart. Darts that
            fall within 0.5 of the origin are within the circle.
            
            Returns 1 if dart is inside circle, else returns 0 '''
        x, y = uniform(0, 1), uniform(0, 1)
        return int(sqrt((x - 0.5)**2 + (y - 0.5)**2) \
            <= 0.5)
        
    # Each process will get 'chunksize' tests and output results into
    # the 'out_q' Queue (to handle asynchronous results)
    out_q = Queue()
    chunksize = int(math.ceil(len(tests) / float(nprocs)))
    procs = []
    
    # Avoid the GIL by running (4) processes pseudo-simultaneously
    # (because of the for-loop initiating p.start() nprocs times).
    for i in range(nprocs):
        p = Process( target=worker,
                	 args=(tests[chunksize*i : chunksize * (i + 1)],) )
        procs.append(p)
        p.start()
    
    # Add up all the darts that landed in the circle.
    total_num_in_circle = 0
    for i in range(nprocs):
        total_num_in_circle += out_q.get()
    
    # Wait for all worker processes to finish
    for p in procs:
        p.join()
    
    return total_num_in_circle


def multiprocessing_darts(nd=200000, nprocs=1):
    """ 'nd' is the number of darts. 'nprocs' is the num processors """

    number_of_darts = nd
    number_of_darts_in_circle = -1 # dummy value
    # How many processors do we want to divide the work up for?
    num_processors = nprocs
    
    # Record the simulation time.
    start_time = time()
    # For the multiprocessing module to work, we need an iterable of size
    # 'number_of_darts'
    darts = range(nd)
    number_of_darts_in_circle = dart_thrower(darts, num_processors)
    end_time = time()
    execution_time = end_time - start_time
    
    # Return a tuple containing:
    # (0) Number of darts
    # (1) Execution time
    # (2) Darts Thrown per second
    return (number_of_darts, execution_time, number_of_darts / execution_time)