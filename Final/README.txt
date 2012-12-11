Author: Victor Chen
Date: 12/11/12

Instructions: run "python resonance_sweep.py" or double-click the file icon.

"resonance_sweep.py" is a gui that talks with a GPIB controller that in turn programs 2 synthesizers. This program allows the user to set frequency sweeping parameters as well as visualizing resonance curves within the window.

Data is retrieved from DAQ device, which "resonance_sweep.py" also provides an interface for, plotted, and stored in an HDF5 file for later viewing (primarily for MATLAB).

This version of "resonance_sweep.py" shows only the bare essentials of the program and does not use any of the modules required to interface between the DAQ and GPIB. I hope this program, however, will show how I have implemented GUI with PyQt, plotted and formatted data with Matplotlib/Pyplot, and store large datasets with HDF5.

The functions of this program have been edited out.