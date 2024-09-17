##### Unknown import, can probably delete ##################
from multiprocessing import connection

##### Import from the official Labscript Devices ###########
from labscript_devices.PrawnBlaster.labscript_devices import PrawnBlaster
from labscript_devices.NI_DAQmx.models.NI_PXIe_6361 import NI_PXIe_6361
from labscript_devices.NI_DAQmx.models.NI_PCIe_6363 import NI_PCIe_6363
# from labscript_devices.NI_DAQmx.models.NI_PXIe_6739 import NI_PXIe_6739
# from labscript_devices.NI_DAQmx.models.NI_PXIe_6535 import NI_PXIe_6535

##### Import from the custom RaX user_devices ###############
# from user_devices.RemoteControl.labscript_devices import RemoteControl, RemoteAnalogOut, RemoteAnalogMonitor
from user_devices.NuvuCamera.labscript_devices import NuvuCamera
from labscriptlib.lyman29.connection_table import connection_table

from labscript import (
    DigitalOut,
    AnalogOut,
    AnalogIn,
    start,
    stop,
    add_time_marker
)

connection_table()

from labscriptlib.lyman29.subsequences.subsequences import *

start()

# Pulse the YAG
tYAG = 2e-3
digital_pulse(do1_6361,tYAG, 0.5e-3)

tstart = 0
tend = 10e-3
ai0_6361.acquire('Atom Absorption',tstart,tend)

stop(10e-3)
