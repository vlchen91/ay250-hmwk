from matplotlib import pyplot as plt
import numpy as np
import re
import os

# File processing
filenames = ['google_data.txt','yahoo_data.txt','ny_temps.txt']
newfilenames = ['google_data_temp.txt','yahoo_data_temp.txt',
                'ny_temps_temp.txt']
for i in range(3):
    datafile = open(filenames[i], 'r')
    newdatafile = open(newfilenames[i], 'w')
    for line in datafile:
        m_obj = re.search(r"\d", line)
        if m_obj:
            newdatafile.write(line)
        
    datafile.close()
    newdatafile.close()
    
# Plot
figure(figsize=(12,9))    
    
###### Google Data ######
dt = [  ('Date',np.int64),
        ('Stock Value',np.float64)  ]
tab = np.loadtxt(newfilenames[0], dtype=dt)
ax0 = plt.gca()
plot1 = ax0.plot(tab['Date'],tab['Stock Value'],
    label="Google Stock Value")

###### Yahoo! Data ######
dt = [  ('Date',np.int64),
        ('Stock Value',np.float64)  ]
tab = np.loadtxt(newfilenames[1], dtype=dt)
plot2 = ax0.plot(tab['Date'],tab['Stock Value'],
    color='m', label='Yahoo! Stock Value')


######   NY Temps  ######
ax1 = ax0.twinx()
dt = [  ('Date',np.int64),
        ('Temperature',np.int64)  ]
tab = np.loadtxt(newfilenames[2], dtype=dt)
plot3 = ax1.plot(tab['Date'],tab['Temperature'],
    linestyle='--',color='r',
    label="NY Mon. High Temp")

# Configure plot
ax1.set_ylim(-150,100)
ax0.autoscale_view()
plt.title("New York Temperature, Google, and Yahoo!")
ax0.set_ylabel('Value (Dollars)')
ax0.set_xlabel('Date (MJD)')
ax1.set_ylabel(u"Temperature (°F)")
plots = plot1 + plot2 + plot3
labs = [p.get_label() for p in plots]
l = ax0.legend(plots,labs,loc='center left')
    # optional kwarg: prop={'size':14}
l.draw_frame(False)

plt.minorticks_on()
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
majorLocator   = MultipleLocator(1000)
majorFormatter = FormatStrFormatter('%d')
minorLocator   = MultipleLocator(200)

ax0.xaxis.set_major_locator(majorLocator)
ax0.xaxis.set_major_formatter(majorFormatter)
ax0.xaxis.set_minor_locator(minorLocator)
ax0.xaxis.tick_bottom()

# Delete temporary files
for nf in newfilenames:
    os.system('rm ' + nf)