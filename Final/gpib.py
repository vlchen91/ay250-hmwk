def SynSetFreq(syn,freq):
    
    #fstr = 'F0 %12.9f GH CF0' %  freq
    fstr = ':FREQ %12.9f GHZ' % freq
    syn.write(fstr)



def SynSetPower(syn,power):

   # fstr = 'XL0 %f DM LO' % power
    fstr = 'POW:AMPL %f dBm' % power
    syn.write(fstr)
    
