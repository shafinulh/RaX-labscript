"""
This file defines the hardware configuration for ALL the experiment hardware.
This example sets up various National Instruments (NI) data acquisition devices, a PrawnBlaster for timing,
a NuvuCamera, and remote control for laser locking.

The connection_table() function initializes all devices and their connections. This function can be imported
into the experiment sequence scripts you write, but this is NOT recommended. Please see documentation in the
sequence files to understand why.

Example Devices:
1. PrawnBlaster: Used as a PseudoClock for timing control
2. NI_PXIe_6361: Multi-Function I/O device
3. NI_PXIe_6535: Digital Output device
4. NI_PXIe_6739: Analog Output device
5. NuvuCamera: For image acquisition
6. RemoteControl: For communication with LabVIEW laser locking system

Each device is configured with physical connections and their settings

For more detailed discussions about writing the connection table, see the Confluence Page 
"""

##### Unknown import, can probably delete ##################
from multiprocessing import connection

##### Import from the official Labscript Devices ###########
from labscript_devices.PrawnBlaster.labscript_devices import PrawnBlaster
from labscript_devices.NI_DAQmx.models.NI_PXIe_6361 import NI_PXIe_6361
from labscript_devices.NI_DAQmx.models.NI_PXIe_6363 import NI_PXIe_6363
# from labscript_devices.NI_DAQmx.models.NI_PXIe_6739 import NI_PXIe_6739
# from labscript_devices.NI_DAQmx.models.NI_PXIe_6535 import NI_PXIe_6535

##### Import from the custom RaX user_devices ###############
# from user_devices.RemoteControl.labscript_devices import RemoteControl, RemoteAnalogOut, RemoteAnalogMonitor
# from user_devices.NuvuCamera.labscript_devices import NuvuCamera

from labscript import (
    DigitalOut,
    AnalogOut,
    AnalogIn,
    start,
    stop,
    add_time_marker
)

def connection_table():
    # PseudoClock
    pb = PrawnBlaster(
        name='pb',
        com_port='COM12',
        # num_pseudoclocks=2
    )

    # NI-6363 Multi-Function Card used for.....
    ni_6363_max_name = "PXI1Slot2" # NI card name configured in and obtained from NI MAX software
    ni_6363_clockline = pb.clocklines[0] 

    ni_6363_mio = NI_PXIe_6363(
        name='ni_6363_mio', 
        parent_device=ni_6363_clockline,
        clock_terminal=f'/{ni_6363_max_name}/PFI1',
        MAX_name=f'{ni_6363_max_name}',
        acquisition_rate=100e3,
    )


    do0_6363 = DigitalOut(name='do0_6363', parent_device=ni_6363_mio, connection='port0/line0')
    do1_6363 = DigitalOut(name='do1_6363', parent_device=ni_6363_mio, connection='port0/line1')
    ai0_6363 = AnalogIn(name='ai0_6363', parent_device=ni_6363_mio, connection='ai0')

    # Remote communication with laser locking program
    # LaserLockGUI = RemoteControl(name='LaserLockGUI', host="localhost", reqrep_port=55535, pubsub_port=55536, mock=False) # use IP address and Port of the host software

    # Remote Analog Outputs for laser control
    # cwave_setpoints = RemoteAnalogOut(
    #     name='cwave_setpoints', 
    #     parent_device=LaserLockGUI, 
    #     connection='cwave_gtr_set',
    #     units="nm",
    #     decimals=6
    # )
    # Titanium_Sapphire_setpoints = RemoteAnalogOut(
    #     name='Titanium_Sapphire_setpoints', 
    #     parent_device=LaserLockGUI, 
    #     connection='TiSa_set',
    #     units="nm",
    #     decimals=6
    # )

    # Remote Analog Monitors for laser feedback
    # RemoteAnalogMonitor(
    #     name='cwave_actual_values', 
    #     parent_device=LaserLockGUI, 
    #     connection='cwave_gtr_act',
    #     units="nm",
    #     decimals=6
    # )
    # RemoteAnalogMonitor(
    #     name='Titanium_Sapphire_actual_values', 
    #     parent_device=LaserLockGUI, 
    #     connection='TiSa_act',
    #     units="nm",
    #     decimals=6
    # )

if __name__ == '__main__':
    connection_table()

    # start() elicits the commencement of the shot
    start()

    # Stop the experiment shot with stop()
    stop(1.0)