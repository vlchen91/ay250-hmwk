CalCalc.py

Author: Victor Chen
Version: 1.0
License: License not to kill


------Installation------

To install the CalCalc module:

    python setup.py install


------Description-------

The CalCalc module contains only one function: calculate. It accepts a string as argument and evaluates it as a mathematical expression. The math and numpy modules are imported for calculations beyond basic arithmetic.

Calculate will attempt to calculate using eval or, if an error occurs, will ask an Wolfram|Alpha API for an answer.

------Testing-----------

To test the calculate function:

    nosetests CalCalc.py

------Caution--------------

calculate uses eval!