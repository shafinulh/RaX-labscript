##### Unknown import, can probably delete ##################
# from multiprocessing import connection

##### Import from the official Labscript Devices ###########
# from labscript_devices.PrawnBlaster.labscript_devices import PrawnBlaster
# from labscript_devices.NI_DAQmx.models.NI_PXIe_6361 import NI_PXIe_6361
# from labscript_devices.NI_DAQmx.models.NI_PCIe_6363 import NI_PCIe_6363
# from labscript_devices.NI_DAQmx.models.NI_PXIe_6739 import NI_PXIe_6739
# from labscript_devices.NI_DAQmx.models.NI_PXIe_6535 import NI_PXIe_6535

##### Import from the custom RaX user_devices ###############
# from user_devices.RemoteControl.labscript_devices import RemoteControl, RemoteAnalogOut, RemoteAnalogMonitor
# from user_devices.NuvuCamera.labscript_devices import NuvuCamera

if True:
    from labscript import (
        DigitalOut,
        AnalogOut,
        AnalogIn,
        start,
        stop,
        add_time_marker
    )
    from labscript_devices.PrawnBlaster.labscript_devices import PrawnBlaster
    from labscript_devices.NI_DAQmx.models.NI_PXIe_6361 import NI_PXIe_6361
    from labscript_devices.NI_DAQmx.models.NI_PCIe_6363 import NI_PCIe_6363
    from labscript_devices.DummyIntermediateDevice import DummyIntermediateDevice

    # from user_devices.RemoteControl.labscript_devices import RemoteControl, RemoteAnalogOut, RemoteAnalogMonitor

    # Use a pineblaster for the psuedoclock
    # PineBlaster(name='pb', usbport='COM9')

    pb = PrawnBlaster(
            name='pb',
            com_port='COM12',
            # num_pseudoclocks=2
        )

    '''
    Initialize the NI Hardware and all the channels
    to be used on each card
    '''
    ni_6363_max_name = "PXI1Slot2"
    ni_6363_clockline = pb.clocklines[0] 

    ni_6363 = NI_PCIe_6363(
        name='ni_6363', 
        parent_device=ni_6363_clockline,
        clock_terminal=f'/{ni_6363_max_name}/PFI1',
        MAX_name=f'{ni_6363_max_name}',
        acquisition_rate=1000e3,
        stop_order=-1,
    )

    # Analog Output Channels
    # The AnalogOut objects must be referenced below with the name of the object (e.g. 'ao0')
    # AnalogOut(name='ao0', parent_device=ni_6363, connection='ao0')
    # AnalogOut(name='ao1', parent_device=ni_6363, connection='ao1')

    # Digital Output Channels
    do0_6363 = DigitalOut(
        name='do0', parent_device=ni_6363, connection='port0/line0'
    )
    do1_6363 = DigitalOut(
        name='do1', parent_device=ni_6363, connection='port0/line1'
    )

    # Analog Input Channels
    ai0_6363 = AnalogIn(name="ai0", parent_device=ni_6363, connection='ai0')
    ai1_6363 = AnalogIn(name="ai1", parent_device=ni_6363, connection='ai1')


from labscriptlib.lyman29.subsequences.subsequences import *

start()

# Pulse the YAG
tYAG = 2e-3
digital_pulse(do1_6363,tYAG, 0.5e-3)

tstart = 0
tend = 10e-3
ai0_6363.acquire('Atom Absorption',tstart,tend)

stop(10e-3)
