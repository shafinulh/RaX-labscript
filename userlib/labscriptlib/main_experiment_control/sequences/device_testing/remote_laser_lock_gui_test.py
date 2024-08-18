"""
laser_lock_gui_test.py

This script tests communication with a remote LaserLockGUI.
It sets wavelength setpoints and reads actual values.
"""

from labscript import start, stop
from labscript_devices.PrawnBlaster.labscript_devices import PrawnBlaster
from user_devices.RemoteControl.labscript_devices import RemoteControl, RemoteAnalogOut, RemoteAnalogMonitor

# PseudoClock
pb = PrawnBlaster(
    name='pb',
    com_port='COM5',
    num_pseudoclocks=2
)

# Remote communication with laser locking program
LaserLockGUI = RemoteControl(name='LaserLockGUI', host="localhost", reqrep_port=55535, pubsub_port=55536, mock=False) # use IP address and Port of the host software

# Remote Analog Outputs for laser control
cwave_setpoints = RemoteAnalogOut(
    name='cwave_setpoints', 
    parent_device=LaserLockGUI, 
    connection='cwave_gtr_set',
    units="nm",
    decimals=6
)
Titanium_Sapphire_setpoints = RemoteAnalogOut(
    name='Titanium_Sapphire_setpoints', 
    parent_device=LaserLockGUI, 
    connection='TiSa_set',
    units="nm",
    decimals=6
)

# Remote Analog Monitors for laser feedback
RemoteAnalogMonitor(
    name='cwave_actual_values', 
    parent_device=LaserLockGUI, 
    connection='cwave_gtr_act',
    units="nm",
    decimals=6
)
RemoteAnalogMonitor(
    name='Titanium_Sapphire_actual_values', 
    parent_device=LaserLockGUI, 
    connection='TiSa_act',
    units="nm",
    decimals=6
)

########## START OF EXPERIMENT LOGIC ################################################

# Set initial wavelength setpoints for the lasers
# These values are programmed at the beginning of each experimental shot
cwave_setpoints.constant(value=379.0)
Titanium_Sapphire_setpoints.constant(value=435.0)

# NOTE: No active commands during the sequence, but laser frequencies will be logged at the start and end of the shot
start()
t = 0
t += 1
stop(t)