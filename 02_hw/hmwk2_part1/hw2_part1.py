import numpy as np
import matplotlib.pyplot as plt

for i in range(1,4):
    filename = "one_c%d.1ABmag" % i
    datafile = open(filename, 'r')
    newdatafile = open(filename + '_temp', 'w')
    for line in datafile:
        if line[0] == '#':
            continue
        newdatafile.write(line)
    
    datafile.close()
    newdatafile.close()

f, (ax1,ax2) = plt.subplots(2,1, sharex=True)
for i in range(1,4):
    filename = "one_c%d.1ABmag" % i
    filename += '_temp'
    dt = [  ('log-age-yr',np.float64),
            ('Mbol',np.float64),
            ('g_AB',np.float64),
            ('(u-g)AB',np.float64),
            ('(g-r)AB',np.float64),
            ('(g-i)AB',np.float64),
            ('(g-z)AB',np.float64)  ]
    tab = np.loadtxt(filename,dt)
    f.subplots_adjust(hspace=0)
    linepattern = ""
    ilabel = ""
    if i == 1:
        linepattern += "-"
        ilabel += "SSP"
    elif i == 2:
        linepattern += "--"
        ilabel += "constant"
    else:
        linepattern += "-."
        ilabel += r"$\tau=1$"
    
    ax1.plot(tab['log-age-yr'],tab['(u-g)AB'], 
        linestyle=linepattern,color='k',
        label=ilabel)
    plt.xlim(5,10)
    ax1.set_ylim(-0.5,2.0)
    ax1.legend(loc='best').draw_frame(False)
    ax1.set_ylabel('u-g')
    
    ax2.plot(tab['log-age-yr'],tab['(g-r)AB'],
        linestyle=linepattern,color='k')
    ax2.set_ylabel('g-r')
    ax2.set_xlabel('Age (Log yrs)')
    ax2.set_ylim(bottom=-0.6,top=1.0)

import os

for i in range(1,4):
    filename = "one_c%d.1ABmag" % i
    filename += "_temp"
    os.system('rm ' + filename + '_temp')