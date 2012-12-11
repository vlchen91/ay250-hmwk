import numpy
from matplotlib import pyplot as plt
from PyDAQmx import *
from PyDAQmx.DAQmxConstants import *
from PyDAQmx.DAQmxTypes import *

analog_input = Task()
read = int32()
data = numpy.zeros((1000,), dtype=numpy.float64)

#DAQmx Configure Code
analog_input.CreateAIVoltageChan("Dev1/ai0","",DAQmx_Val_Cfg_Default,-1,1,DAQmx_Val_Volts,None)
analog_input.CfgSampClkTiming("",8e5,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,1000)

# DAQmxSetAICoupling("Dev1/ai0",DAQmx_Val_DC)

#DAQmx Start Code
analog_input.StartTask()

#DAQmx Read Code
analog_input.ReadAnalogF64(1000,20.0,DAQmx_Val_GroupByChannel,data,1000,byref(read),None)

print "Acquired %d points\n"%read.value


x = numpy.arange(0,1000,1)
#print data
plt.plot(x,data)
plt.show()
