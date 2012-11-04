import numpy as np
import numpy.random
import numexpr as ne

def numexpr_darts(nd=200000, nprocs=1):
    """'nd' is the number of darts. 'nprocs' is number of processors. """
    ne.set_num_threads(nprocs)
    
    # Let us define a numpy version of a throw_dart helper function
    def throw_dart():
        ''' Throw "n" darts at a square of length 1.0, and return
            how many times they landed in a concentric circle of radius
            0.5.
        '''
        x = np.random.uniform(size = nd)
        y = np.random.uniform(size = nd)
        expr1 = ne.evaluate('(x - 0.5)**2 + (y - 0.5)**2')
        radius = np.sqrt(expr1)
        in_or_out = ne.evaluate('radius <= 0.5')
        in_or_out = in_or_out.astype(np.int)
        total_inside = ne.evaluate('sum(in_or_out)')
        return total_inside
    
    number_of_darts_in_circle = 0
    
    # Record the simulation time
    start_time = time()
    number_of_darts_in_circle = throw_dart()
    end_time = time()
    execution_time = end_time - start_time
    
    number_of_darts = nd
    pi_approx = 4 * number_of_darts_in_circle / float(number_of_darts)

    # Return a tuple containing:
    # (0) Number of darts
    # (1) Execution time
    # (2) Darts Thrown per second
    return (number_of_darts, execution_time, number_of_darts / execution_time)