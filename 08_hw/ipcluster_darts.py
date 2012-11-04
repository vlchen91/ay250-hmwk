import numpy as np
from IPython.parallel import Client
rc = Client()
dview = rc.direct_view()
dview.block = False
# Make sure ipcluster is running
## ipcluster start --n=4
## ...
## ipcluster stop

def ipcluster_darts(nd=200000):
    """ 'nd' is the number of darts. The number of engines is an
        external parameter set by user-agent. Please configure the
        IPython Cluster. """
    
    # dview doesn't share global namespace
    dview.execute("from random import uniform")
    dview.execute('from math import sqrt')
    dview.execute("""def helper(q):
                         num = 0
                         for i in range(q.shape[0]):
                             x, y = uniform(0, 1), uniform(0, 1)
                             num += int(sqrt((x - 0.5)**2 + (y - 0.5)**2) \
                                 <= 0.5)
                         return num""")
    
    # Start time
    start_time = time()
    # For the IPython.parallel.Client to work, we need an iterable of size
    # 'number_of_darts'.
    dview.scatter('darts',np.arange(nd))
    dview.execute('y = helper(darts)')
    number_of_darts_in_circle = np.sum(dview.gather('y').get())
    # End time
    end_time = time()
    execution_time = end_time - start_time
    
    number_of_darts = nd

    # Return a tuple containing:
    # (0) Number of darts
    # (1) Execution time
    # (2) Darts Thrown per second
    return (number_of_darts, execution_time, number_of_darts / execution_time)