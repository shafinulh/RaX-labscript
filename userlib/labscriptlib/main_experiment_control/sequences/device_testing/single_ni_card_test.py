"""
single_ni_card_test.py

This script demonstrates basic functionality of a single NI multifunction card.
It generates a digital pulse, an analog ramp, and acquires analog data.
"""

from labscript import start, stop, DigitalOut, AnalogOut, AnalogIn
from labscript_devices.PrawnBlaster.labscript_devices import PrawnBlaster
from labscript_devices.NI_DAQmx.models.NI_PXIe_6361 import NI_PXIe_6361

########## SUBSET of CONNECTION TABLE being used in this sequence ###############
# PseudoClock
pb = PrawnBlaster(
    name='pb',
    com_port='COM5',
    num_pseudoclocks=2
)

# NI-6361 Multi-Function Card used for.....
ni_6361_max_name = "PXI1Slot8" # NI card name configured in and obtained from NI MAX software
ni_6361_clockline = pb.clocklines[1] 

ni_6361_mio = NI_PXIe_6361(
    name='ni_6361_mio', 
    parent_device=ni_6361_clockline,
    clock_terminal=f'/{ni_6361_max_name}/PFI1',
    MAX_name=f'{ni_6361_max_name}',
    acquisition_rate=ACQ_RATE,
)

# I/O channels
ao0_6361 = AnalogOut(name='ao0_6361', parent_device=ni_6361_mio, connection='ao0')
ao1_6361 = AnalogOut(name='ao1_6361', parent_device=ni_6361_mio, connection='ao1')
do0_6361 = DigitalOut(name='do0_6361', parent_device=ni_6361_mio, connection='port0/line0')
do1_6361 = DigitalOut(name='do1_6361', parent_device=ni_6361_mio, connection='port0/line1')
ai0_6361 = AnalogIn(name='ai0_6361', parent_device=ni_6361_mio, connection='ai0')
ai1_6361 = AnalogIn(name='ai1_6361', parent_device=ni_6361_mio, connection='ai1')

########## START OF EXPERIMENT LOGIC ################################################
start()

t = 0

ao0_6361.constant(t, 0)

# Generate a digital pulse
do0_6361.go_high(t)
t += 5e-3
do0_6361.go_low(t)

# Generate an analog ramp
t += 10e-3

ramp_start_time = t
t += ao0_6361.ramp(t=t, initial=0, final=1.0, duration=5e-3, samplerate=1e4)
ramp_end_time = t

ao0_6361.constant(t, 0)

# Acquire and save analog data
ai0_6361.acquire(label='test_acquisition', start_time=ramp_start_time, end_time=ramp_end_time+5e-3)

stop(t+10e-3)
