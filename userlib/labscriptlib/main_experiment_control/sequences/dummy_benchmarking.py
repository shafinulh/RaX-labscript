###### COPY IN THE NECESSARY PARTS OF THE CONNECTION TABLE
from multiprocessing import connection
from labscript_devices.PrawnBlaster.labscript_devices import PrawnBlaster
from labscript_devices.NI_DAQmx.models.NI_PXIe_6361 import NI_PXIe_6361

# Import a subsequence function from subsequences.py
from labscriptlib.main_experiment_control.subsequences.subsequences import absorption_signal

from labscript import (
    DigitalOut,
    AnalogOut,
    AnalogIn,
    start,
    stop,
    add_time_marker
)

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

ao0_6361 = AnalogOut(name='ao0_6361', parent_device=ni_6361_mio, connection='ao0')
ao1_6361 = AnalogOut(name='ao1_6361', parent_device=ni_6361_mio, connection='ao1')
do0_6361 = DigitalOut(name='do0_6361', parent_device=ni_6361_mio, connection='port0/line0')
do1_6361 = DigitalOut(name='do1_6361', parent_device=ni_6361_mio, connection='port0/line1')
ai0_6361 = AnalogIn(name='ai0_6361', parent_device=ni_6361_mio, connection='ai0')
ai1_6361 = AnalogIn(name='ai1_6361', parent_device=ni_6361_mio, connection='ai1')

########## START OF EXPERIMENT LOGIC ################################################

# A wrapper of the DO functionality to define an asynchronous start reference pulse
# It is not relevant to the actual sequence
def digital_ref():
    t=0
    do1_6361.go_high(t)
    t+=10e-3
    do1_6361.go_low(t)
    return t

# A wrapper for the labscript `acquire` primitive
def collect_AO(ai_chan: AnalogIn, start_time, end_time):
    t=start_time
    t+=ai0_6361.acquire(label='AO_ramp', start_time=t, end_time=end_time)
    return t

# start the sequence - we will write it to contain an output ramp and absorption signal
t = 0
start()

# write an output ramp, leveraging GLOBALS to define ramp parameters
t=RAMP_TI
add_time_marker(t, f"Analog Ramp for {ao_chan.name}", verbose=True)
t+=ao_chan.ramp(
    t=t,
    initial=RAMP_VI,
    final=RAMP_VF,
    duration=RAMP_DUR,
    samplerate=RAMP_RATE
)
ao_chan.constant(t=t, value=0)

# use subsequences to define the next part of the sequence
# NOTE: the timing of the absorption signal is defined in the SUBSEQUENCES GLOBALS
# but if it is more intuitive, there is no reason it can't be set in the sequence script itself
absorption_end_time = absorption_signal(ao0_6361)
t = max(t, absorption_end_time) 

# make asycnhronous call to the digital reference signal
digital_ref_end_time = digital_ref()
t=max(t, digital_ref_end_time)

# collect signals - again leveraging GLOBALS to know when the signal should be acquired
collect_AO(ai0_6361, RAMP_TI, RAMP_TF)
collect_AO(ai1_6361, DIP_TI, DIP_TF)

stop(t)
