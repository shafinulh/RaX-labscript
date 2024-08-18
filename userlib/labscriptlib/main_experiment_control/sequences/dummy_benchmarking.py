###### COPY IN THE NECESSARY PARTS OF THE CONNECTION TABLE
from multiprocessing import connection
from labscript_devices.PrawnBlaster.labscript_devices import PrawnBlaster
from labscript_devices.NI_DAQmx.models.NI_PXIe_6361 import NI_PXIe_6361

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

def digital_start_ref():
    t=0
    do1_6361.go_high(t)
    t+=10e-3
    do1_6361.go_low(t)
    return t

def digital_pwm_stream():
    t=CONTROL_PWM_TI
    # add_time_marker(t, "D0 PWM CTRL")
    while t<=CONTROL_PWM_TF:
        do0_6361.go_high(t)
        t+=((1/CONTROL_PWM_FREQ) * CONTROL_DUTY_CYCLE)
        do0_6361.go_low(t)
        t+=((1/CONTROL_PWM_FREQ) * (1-CONTROL_DUTY_CYCLE))
    return t

def analog_output_ramp(ao_chan: AnalogOut):
    t=RAMP_TI
    add_time_marker(t, f"Analog Ramp for {ao_chan.name}", verbose=True)
    t+=ao_chan.ramp(
        t=t, 
        initial=RAMP_VI, 
        final=RAMP_VF, 
        duration=RAMP_DUR, 
        samplerate=RAMP_RATE
    )
    ao_chan.constant(t=t, value=0.1)
    return t

def collect_AO_0():
    t=RAMP_TI
    t+=ai0_6361.acquire(label='AO_ramp', start_time=t, end_time=RAMP_TF)
    return t

def collect_AO_1():
    t=DIP_TI
    t+=ai1_6361.acquire(label='AI_signal', start_time=0, end_time=DIP_TF)
    return t

t=0
start()
t=max(t, digital_start_ref())
t=max(t, digital_pwm_stream())
t=max(t, analog_output_ramp(ao1_6361))
t=max(t, absorption_signal(ao0_6361))
t=max(t, collect_AO_0())
t=max(t, collect_AO_1())
print(t)
stop(t)