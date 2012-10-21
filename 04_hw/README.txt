Author: Victor Chen
Modified: 10/6/12

---------------------------------
Instructions
---------------------------------

Run

    ipython notebook --pylab inline

and open the .ipynb files. 04_hw_client and 04_hw_server correspond to part 1.


Part 1

Start the server and connect locally (on the same computer) with the provided client script. The client script provides a demonstration of all 3 image manipulation methods. A brief description for each method is provided in the respective method docstring/comment-block.


Part 2

#.aif	Peak Hz	Note
1	390.75	G4 
2	349.25	F4
3	1316.0	E6
4	258.25	C4
5	293.31	D4
6	523.44	C5
7	1171.6	D6
8	696.06	F5
9	390.75	G4
10	391.25	G4
11	1319.9	E6
12	391.13	G4


---------------------------------
Future Improvements
---------------------------------

Part 2: Implement a filter that has peaks at note frequencies and their multiples, i.e. any multiple of C, C#, D, D#, E, F, F#, G, G#, A, A#, B. Any other freq will collapse to zero.

Secondly, implement an overtone_checker function to collapse any overtone frequencies that made it through the optimal filter. The first occurence of the multiples of a peak frequency is called the "dominant tone." The other multiples are called "overtones" and will have smaller power values. The overtone_checker will recognize the dominant tone and subsequently reject its multiples (overtones). If an octave is performed (e.g. A2 + A3), overtone_checker will assume that the 2 frequencies are played at the same power, so the larger frequency will not be treated as an overtone.





