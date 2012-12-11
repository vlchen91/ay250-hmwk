#####
## Author: Victor Chen
## Date: 11/23/12
#####
# ------------------------------
# IMPORT STATEMENTS
# ------------------------------
import sys, os, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np
import scipy
from scipy import fft
import tables
from tables import IsDescription, Float32Col, openFile
'''
from PyDAQmx import *
from PyDAQmx.DAQmxConstants import *
from PyDAQmx.DAQmxTypes import *
import gpib
from visa import instrument
'''
# ------------------------------
# IQ_data TABLES/HDF5
# ------------------------------
class IQ_data(tables.IsDescription):
    freq    = Float32Col() # unit GHz
    I_med   = Float32Col()
    I_std   = Float32Col()
    Q_med   = Float32Col()
    Q_std   = Float32Col()

h5file = openFile("iq_data.h5", mode="w", title="IQ Data")
group = h5file.createGroup(h5file.root, "syn_test", "Synthesizer Test")
table = h5file.createTable(group, "IQ readout", IQ_data, "Syn Readout")
iq_data = table.row

# ------------------------------
# DAQ/GPIB INTERFACE METHODS
# ------------------------------
def getDAQdata():
    ''' Talks to DAQ instrument to read in data points. Returns the data from the
    2 channels.
    '''
    '''
    analog_input = Task()
    read = int32()
    data = np.zeros((20000,), dtype=np.float64)
    # DAQmx configure code
    analog_input.CreateAIVoltageChan("Dev1/ai0:1", "", DAQmx_Val_Cfg_Default,
        -1., 1., DAQmx_Val_Volts, None)
    analog_input.CfgSampClkTiming("", 8e5, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps,
        10000)
    # DAQmx start code
    analog_input.StartTask()
    # DAQmx read code
    analog_input.ReadAnalogF64(10000, 20.0, DAQmx_Val_GroupByChannel, data, 
        20000, byref(read), None)
    # data[:10000] gives the 1st channel, data[1000:] gives 2nd channel
    return data
    '''

def set_Syn(giga_freq, power):
    ''' Sets the frequency and power of the connected synthesizer.
    giga_freq=frequency in units GHz, power=power in units dBm '''
    '''
    syn = instrument("GPIB0::15")
    syn.write("*IDN?")
    # set frequency (GHz)
    gpib.SynSetFreq(syn, giga_freq)
    # set power (dBm)
    gpib.SynSetPower(syn, power)
    '''
    pass
    
def do_freq_sweep(center_freq, freq_span, n_pts, power):
    ''' Return a 2D array of dimension (n_pts, 4) of the DAQ data.
    0. frequency (GHz)
    1. I median/mean
    2. I std
    3. Q median/mean
    4. Q std

    Sweep from center_freq - freq_span / 2 --> center_freq + freq_span / 2,
    storing 1000 IQ data pts at each freq.
    
    Currently, this involves keeping Syn 1 @ const. freq, while sweeping Syn 2.
    Syn 1 freq will have be set manually at this moment.
    '''
    '''
    lowest_freq = center_freq - (freq_span * 10**-6) / 2
    highest_freq = center_freq + (freq_span * 10**-6) / 2
    freq_lst = numpy.linspace(lowest_freq, highest_freq,
        n_pts)
    arr = np.zeros((n_pts, 5))
    for i,f in enumerate(freq_lst):
        set_Syn(f, power)
        trace = getDAQdata()
        I_trace = trace[:10000]
        Q_trace = trace[10000:]
        I_med = I_trace[500]
        Q_med = Q_trace[500]
        I_std = np.std(I_trace)
        Q_std = np.std(Q_trace)
        data = (f, I_med, I_std, Q_med, Q_std)
        arr[i] = data
        
        iq_data['freq']  = f
        iq_data['I_med'] = I_med
        iq_data['I_std'] = I_std
        iq_data['Q_med'] = Q_med
        iq_data['Q_std'] = Q_std
        iq_data.append()

    # Write data to hdf5 file
    table.flush()
    
    return arr
    '''
    pass

# ------------------------------
# GUI
# ------------------------------
class AppForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        self.setWindowTitle('Resonance Frequency Sweep GUI')
        # Custom widget-creation method
        self.create_main_frame()
        
    def create_main_frame(self):
        self.main_frame = QWidget()
        # Create the mpl Figure and FigCanvas objects.
        # 8x6 inches, 100 dpi
        self.fig1 = Figure((6.0,6.0), dpi=100)
        self.axes1 = self.fig1.add_subplot(111)
        self.axes1.set_title('I vs Q resonance curve')

        fig2, (axes2_1, axes2_2) = plt.subplots(2,1, sharex=True)
        fig2.subplots_adjust(hspace=0)
        axes2_1.set_title('IQ')
        axes2_1.set_ylabel('Amplitude')
        axes2_2.set_ylabel('Amplitude')
        axes2_2.set_xlabel('Time')
        self.fig2 = fig2
        self.axes2_1 = axes2_1
        self.axes2_2 = axes2_2

        fig3, (axes3_1, axes3_2) = plt.subplots(2,1, sharex=True)
        fig3.subplots_adjust(hspace=0)
        axes3_1.set_title('IQ FFT/PSD')
        axes3_1.set_ylabel('Spectrum')
        axes3_2.set_ylabel('Spectrum')
        axes3_2.set_xlabel('Frequency')
        self.fig3 = fig3
        self.axes3_1 = axes3_1
        self.axes3_2 = axes3_2
        
        self.canvas1 = FigureCanvas(self.fig1)
        self.canvas2 = FigureCanvas(self.fig2)
        self.canvas3 = FigureCanvas(self.fig3)
        self.canvas1.setParent(self.main_frame)
        self.canvas2.setParent(self.main_frame)
        self.canvas3.setParent(self.main_frame)
        ## The following toolbars are completely optional.
        # Create the mpl navi toolbar, tied to the canvas
        self.mpl_toolbar1 = NavigationToolbar(self.canvas1, self.main_frame)
        self.mpl_toolbar2 = NavigationToolbar(self.canvas2, self.main_frame)
        self.mpl_toolbar3 = NavigationToolbar(self.canvas3, self.main_frame)
        # Create all input parameter textboxes
        self.center_freq_txtbx = QLineEdit('1.0') # default 1.0GHz
        self.freq_span_txtbx = QLineEdit('50.0') # default 50kHz
        self.n_pts_txtbx = QLineEdit('200') # default 200 sweep points
        ## The following are optional, and for deliberate testing purposes
        self.power1_txtbx = QLineEdit('0') # Syn 1 default: 0dBm
        self.power2_txtbx = QLineEdit('0') # Syn 2 default: 0dBm
        # Create all the labels
        self.center_freq_lbl = QLabel('Center Frequency (GHz)')
        self.freq_span_lbl = QLabel('Freq Span (khz)')
        self.n_pts_lbl = QLabel('# Sweep Pts')
        self.power1_lbl = QLabel('Syn 1 Power (dBm) (NOT WORKING)')
        self.power2_lbl = QLabel('Syn 2 Power (dBm)')
        # Create the button(s)
        self.sweep_btn = QPushButton("Sweep Save Data")
        self.draw_btn = QPushButton("Resonance Draw")
        # Create layout
        vbox_main = QVBoxLayout() 
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()
        # widget_lst order matters
        vbox1_w_lst = [ self.center_freq_lbl, self.center_freq_txtbx, self.freq_span_lbl,
            self.freq_span_txtbx, self.n_pts_lbl, self.n_pts_txtbx ]
        vbox2_w_lst = [ self.power1_lbl, self.power1_txtbx, self.power2_lbl,
            self.power2_txtbx, self.sweep_btn, self.draw_btn ]
        for w in vbox1_w_lst:
            vbox1.addWidget(w)
        for w in vbox2_w_lst:
            vbox2.addWidget(w)
        hbox1_w_lst = [self.canvas1, self.canvas2, self.canvas3]
        for w in hbox1_w_lst:
            hbox1.addWidget(w)
        hbox2.addLayout(vbox1)
        hbox2.addLayout(vbox2)
        #vbox_main.addWidget(self.canvas)
        #vbox_main.addWidget(self.mpl_toolbar)
        vbox_main.addLayout(hbox1)
        vbox_main.addLayout(hbox2)
        self.main_frame.setLayout(vbox_main)
        self.setCentralWidget(self.main_frame)
        
        # Event connections/signals
        self.connect(self.sweep_btn, SIGNAL("clicked()"), self.on_sweep)
        self.connect(self.draw_btn, SIGNAL("clicked()"), self.on_draw)

    def on_sweep(self):
        ''' Clear previous and draw new IQ data. Triggers when Sweep button is pushed.
            Performs do_freq_sweep'''
        '''
        center_freq = float(self.center_freq_txtbx.text())
        freq_span = float(self.freq_span_txtbx.text())
        n_pts = int(self.n_pts_txtbx.text())
        power2 = float(self.power2_txtbx.text())
        IQ_data = do_freq_sweep(center_freq, freq_span, n_pts, power2)
        
        I_meds = IQ_data[:, 1]
        Q_meds = IQ_data[:, 3]
        
        self.axes1.clear()
        self.axes1.scatter(I_meds, Q_meds)
        self.canvas1.draw()
        '''
        pass

    def on_draw(self):
        ''' Clear previous and draw new resonance data. Triggers when Draw button
            is pushed. For now, on_draw will use the center frequency, not the
            "resonance" frequency. '''
        '''
        res_freq = float(self.center_freq_txtbx.text())
        power = float(self.power2_txtbx.text())
        set_Syn(res_freq, power)
        trace = getDAQdata()
        I_trace = trace[:10000]
        Q_trace = trace[10000:]
        self.axes2_1.clear()
        self.axes2_2.clear()
        self.axes2_1.plot(I_trace)
        self.axes2_2.plot(Q_trace)
        self.canvas2.draw()
        self.axes3_1.clear()
        self.axes3_2.clear()
        self.axes3_1.plot(fft(I_trace))
        self.axes3_2.plot(fft(Q_trace))
        self.canvas3.draw()
        '''
        pass
        
        


# ------------------------------
# RUN EVENT LOOP UNTIL QUIT
# ------------------------------
def main():
    
    app = QApplication(sys.argv)
    form = AppForm()
    form.show()
    app.exec_()
    
if __name__ == '__main__':
    main()
