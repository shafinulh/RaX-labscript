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
from labscript_devices.NI_DAQmx.models.NI_PCIe_6363 import NI_PCIe_6363
from labscript_devices.NI_DAQmx.models.NI_PXIe_6739 import NI_PXIe_6739
from labscript_devices.NI_DAQmx.models.NI_PXIe_6535 import NI_PXIe_6535

##### Import from the custom RaX user_devices ###############
from user_devices.RemoteControl.labscript_devices import RemoteControl, RemoteAnalogOut, RemoteAnalogMonitor
from user_devices.NuvuCamera.labscript_devices import NuvuCamera

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
        acquisition_rate=1000e3,
    )

    ao0_6361 = AnalogOut(name='ao0_6361', parent_device=ni_6361_mio, connection='ao0')
    ao1_6361 = AnalogOut(name='ao1_6361', parent_device=ni_6361_mio, connection='ao1')
    do0_6361 = DigitalOut(name='do0_6361', parent_device=ni_6361_mio, connection='port0/line0')
    do1_6361 = DigitalOut(name='do1_6361', parent_device=ni_6361_mio, connection='port0/line1')
    ai0_6361 = AnalogIn(name='ai0_6361', parent_device=ni_6361_mio, connection='ai0')
    ai1_6361 = AnalogIn(name='ai1_6361', parent_device=ni_6361_mio, connection='ai1')

    # NI-6535 Digital Output Card used for.....
    ni_6535_max_name = "PXI1Slot5"
    ni_6535_clockline = pb.clocklines[0] 
    ni_6365_dio = NI_PXIe_6535(
        name='ni_6365_dio', 
        parent_device=ni_6535_clockline,
        clock_terminal=f'/{ni_6535_max_name}/PFI1',
        MAX_name=f'{ni_6535_max_name}',
    )
    do0_6535 = DigitalOut(name='do0_6535', parent_device=ni_6365_dio, connection='port0/line0')
    do1_6535 = DigitalOut(name='do1_6535', parent_device=ni_6365_dio, connection='port0/line1')
    do2_6535 = DigitalOut(name='do2_6535', parent_device=ni_6365_dio, connection='port0/line2')
    do3_6535 = DigitalOut(name='do3_6535', parent_device=ni_6365_dio, connection='port0/line3')

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
    ao2_6739 = AnalogOut(name='ao2_6739', parent_device=ni_6739_ao, connection='ao8')
    ao3_6739 = AnalogOut(name='ao3_6739', parent_device=ni_6739_ao, connection='ao12')

    # Nuvu Camera
    # NOTE: The initialization of the NuvuCamera creates an implicit DO under the name "camera_trigger" at the specified connection.
    camera = NuvuCamera(
        name="camera",
        parent_device=ni_6361_mio,
        connection="port0/line2",
        serial_number=0xDEADBEEF, # NUVU camera initialization does not require serial_number, no need to touch this
        camera_attributes={
            "readoutMode":1, #1 = EM
            "exposure_time":20, #Shafin: "Um miliseconds?"
            "timeout": 1000, #See above for units
            "square_bin": 1, #NxN bin size
            'target_detector_temp':-60, 
            "emccd_gain": 1, #Max 5000
            "trigger_mode":1, # 1 = EXT_LOW_HIGH, #0 = INT, 2 "EXT_LOW_HIGH_EXP" (minus for HIGH_LOW)
        },
        manual_mode_camera_attributes={
            "readoutMode":1,
            "exposure_time":20,
            "timeout": 1000,
            "square_bin": 1,
            'target_detector_temp':-60,
            "emccd_gain": 1,
            "trigger_mode":0,
        },
        mock=False
    )
    # NOTE: The NI-DAQmx driver requires an even number of digital output channels.
    # If you have an odd number of DOs in use, create a dummy DO to satisfy this requirement.
    DigitalOut(name='dummy_for_even', parent_device=ni_6361_mio, connection='port0/line3')

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

if __name__ == '__main__':
    connection_table()

    # start() elicits the commencement of the shot
    start()

    # Stop the experiment shot with stop()
    stop(1.0)