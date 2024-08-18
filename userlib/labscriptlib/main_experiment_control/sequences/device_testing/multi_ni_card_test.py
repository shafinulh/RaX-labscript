"""
multi_ni_cards_test.py

This script demonstrates the functionality of multiple NI cards working on separate clocklines.
It uses two NI cards to generate simultaneous digital and analog outputs.
"""

from labscript import start, stop, DigitalOut, AnalogOut
from labscript_devices.PrawnBlaster.labscript_devices import PrawnBlaster
from labscript_devices.NI_DAQmx.models.NI_PXIe_6361 import NI_PXIe_6361
from labscript_devices.NI_DAQmx.models.NI_PXIe_6739 import NI_PXIe_6739

########## SUBSET of CONNECTION TABLE being used in this sequence ###############
# PseudoClock
pb = PrawnBlaster(name='pb', com_port='COM5', num_pseudoclocks=2)

# NI-6361 Multi-Function Card used for.....
ni_6361_max_name = "PXI1Slot8" # NI card name configured in and obtained from NI MAX software
ni_6361_clockline = pb.clocklines[1] 

ni_6361_mio = NI_PXIe_6361(
    name='ni_6361_mio', 
    parent_device=ni_6361_clockline,
    clock_terminal=f'/{ni_6361_max_name}/PFI1',
    MAX_name=f'{ni_6361_max_name}',
    acquisition_rate=1000e3,
)

ao0_6361 = AnalogOut(name='ao0_6361', parent_device=ni_6361_mio, connection='ao0')
ao1_6361 = AnalogOut(name='ao1_6361', parent_device=ni_6361_mio, connection='ao1')
do0_6361 = DigitalOut(name='do0_6361', parent_device=ni_6361_mio, connection='port0/line0')
do1_6361 = DigitalOut(name='do1_6361', parent_device=ni_6361_mio, connection='port0/line1')

# NI-6739 Analog Output Card used for.....
ni_6739_max_name = "PXI1Slot3"
ni_6739_clockline = pb.clocklines[0] 
ni_6739_ao = NI_PXIe_6739(
    name='ni_6739_ao', 
    parent_device=ni_6739_clockline,
    clock_terminal=f'/{ni_6739_max_name}/PFI0',
    MAX_name=f'{ni_6739_max_name}',
)
ao0_6739= AnalogOut(name='ao0_6739', parent_device=ni_6739_ao, connection='ao0')
ao1_6739 = AnalogOut(name='ao1_6739', parent_device=ni_6739_ao, connection='ao4')

########## START OF EXPERIMENT LOGIC ################################################
start()

t = 0

# Generate a digital pulse on the first card
do0_6361.go_high(t)
t += 5e-3
do0_6361.go_low(t)

# Generate an analog ramp on the first card
t += 10e-3
ramp_end_time = ao0_6361.ramp(t=t, initial=0, final=5, duration=50e-3, samplerate=2e6)

# Generate a simultaneous analog sine wave on the second card
sine_end_time = ao0_6739.sine(t=t, duration=75e-3, amplitude=2.5, angfreq=2*3.14159*10, phase=0, dc_offset=0.5, samplerate=1e6)

t += max(ramp_end_time,sine_end_time)

stop(t + 10e-3)