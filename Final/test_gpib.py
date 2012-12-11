import sys, os, random, visa, gpib
from visa import instrument

syn = instrument("GPIB0::15")
syn.write("*IDN?")
print syn.read()

# set frequency (GHz)
gpib.SynSetFreq(syn,0.81)

# set power (dBm)
gpib.SynSetPower(syn,-1.1)
