from random import uniform
from math import sqrt
from time import time

def serial_darts(nd=200000):
    """ 'nd' is the number of darts. """
    # Define the total number of darts we'll throw.
    number_of_darts = nd
    # Define a variable to store the number of darts that fall inside the circle.
    number_of_darts_in_circle = 0
    
    # We will use time() to record the execution time of a loop that runs the
    # dart throwing simulation.
    start_time = time()
    
    # This loop simulates the dart throwing. For each dart, find a random position
    # in the unit sqare for it to fall. Test if it falls within the circle by
    # calculating the dstaince from the origin (0.5,0.5) to the dart. Darts that
    # fall within 0.5 of the origin are within the circle.
    for n in range(number_of_darts):
        x, y = uniform(0,1), uniform(0,1)
        if sqrt((x - 0.5) ** 2 + (y - 0.5) ** 2) <= 0.5:
            number_of_darts_in_circle += 1
    
    # Record the time after the conclusion of the loop.
    end_time = time()
    # The total time required to run the loop is the difference.
    execution_time = end_time - start_time
    
    # Return a tuple containing:
    # (0) Number of darts
    # (1) Execution time
    # (2) Darts Thrown per second
    return (number_of_darts, execution_time, number_of_darts / execution_time)