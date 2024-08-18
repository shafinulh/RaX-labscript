"""
camera_single_exposure_test.py

This script tests the NuvuCamera by taking a single exposure triggered by a digital signal.
"""

from labscript import start, stop, DigitalOut
from labscript_devices.PrawnBlaster.labscript_devices import PrawnBlaster
from labscript_devices.NI_DAQmx.models.NI_PXIe_6361 import NI_PXIe_6361
from user_devices.NuvuCamera.labscript_devices import NuvuCamera

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

# Nuvu Camera
# NOTE: The initialization of the NuvuCamera creates an implicit DO under the name "camera_trigger" at the specified connection.
camera = NuvuCamera(
    name="camera",
    parent_device=ni_6361_mio,
    connection="port0/line2",
    serial_number=0xDEADBEEF, # NUVU camera initialization does not require serial_number, no need to touch this
    mock=False
)
# NOTE: The NI-DAQmx driver requires an even number of digital output channels.
# If you have an odd number of DOs in use, create a dummy DO to satisfy this requirement.
DigitalOut(name='dummy_for_even', parent_device=ni_6361_mio, connection='port0/line3')


########## START OF EXPERIMENT LOGIC ################################################
start()

# Trigger the camera at t=50ms for an exposure time of 20ms
t = 50e-3
t += camera.expose(name='single_exposure', t=t, trigger_duration=20e-3)
t += 100e-3

# Stop the experiment
stop(t)
