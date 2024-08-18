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
    # Each non pseudoclock device needs a parent. The parent is a pseudoclock clockline. 
    # This card will use the first clockline 
    ni_6361_clockline = pb.clocklines[1] 
    
    # TODO: get capabiliites of device
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

    ao0_6361.ramp


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

if __name__ == '__main__':
    connection_table()

    # start() elicits the commencement of the shot
    start()

    # Stop the experiment shot with stop()
    stop(1.0)