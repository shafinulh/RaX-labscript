if True:
    #This is an example connection table made on 2024/08/20
    ##### Import from the official Labscript Devices ###########

    from labscript_devices.PineBlaster import PineBlaster
    from labscript_devices.PrawnBlaster.labscript_devices import PrawnBlaster
    from labscript_devices.NI_DAQmx.models.NI_PXIe_6361 import NI_PXIe_6361

    from user_devices.NuvuCamera.labscript_devices import NuvuCamera

    from labscript import (
        DigitalOut,
        AnalogOut,
        AnalogIn,
        start,
        stop,
        add_time_marker
    )

    # PseudoClock
    prawn = PrawnBlaster(
        name='pine',
        out_pins=[11],
        com_port='COM5' #TODO: figure out if this is correct (plug and uplug and see in device manager)
    )

    # NI-6361 Multi-Function Card used for analog input, output, and digital output
    ni_6361_max_name = "PXI1Slot8" # NI card name configured in and obtained from NI MAX software #TODO: check this
    ni_6361_clockline = prawn.clocklines[0]

    ni_6361 = NI_PXIe_6361(
        name='NI_6361',
        parent_device=ni_6361_clockline,
        clock_terminal = f'/{ni_6361_max_name}/PFI1', #TODO check this
        AI_term = 'Diff',
        num_AI = 2,
        num_AO = 2,
        num_CI=1,
        acquisition_rate=100e3,
        MAX_name=f'{ni_6361_max_name}'
    )

    atom_abs = AnalogIn('atom_abs',ni_6361,'ai0')
    mol_abs = AnalogIn('mol_abs',ni_6361,'ai1')

    YAG_trig = DigitalOut('YAG_trig', ni_6361, 'port0/line0') #TODO: check this
    shutter_atom_trig = DigitalOut('shutter_atom_trig',ni_6361,'port0/line1') #TODO: check this
    shutter_mol_trig = DigitalOut('Shutter_mol_trig', ni_6361, 'port0/line2') #TODO: check this
    #'port0/line7' is reserved for camera
    dummy = DigitalOut('dummy',ni_6361,'port0/line3')


    atom_power = AnalogOut('atom_power',ni_6361,'ao0')
    mol_power = AnalogOut('mol_power',ni_6361,'ao1')

    # nuvu_camera = NuvuCamera(
    #     name="nuvu_camera",
    #     parent_device=ni_6361,
    #     connection="port0/line7",
    #     serial_number=0xDEADBEEF, # NUVU camera initialization does not require serial_number, no need to touch this
    #     camera_attributes={
    #         "readoutMode":1, #1 = EM
    #         "exposure_time":20, #Shafin: "Um miliseconds?"
    #         "timeout": 10000, #See above for units
    #         "square_bin": 1, #NxN bin size
    #         'target_detector_temp':-60, 
    #         # "emccd_gain": 2, #Max 5000
    #         "trigger_mode":1, # 1 = EXT_LOW_HIGH, #0 = INT, 2 "EXT_LOW_HIGH_EXP" (minus for HIGH_LOW)
    #     },
    #     manual_mode_camera_attributes={
    #         "readoutMode":1,
    #         "exposure_time":20,
    #         "timeout": 10000,
    #         "square_bin": 1,
    #         'target_detector_temp':-60,
    #         # "emccd_gain": 2,
    #         "trigger_mode":1,
    #     },
    #     mock=False
    # )

from labscriptlib.main_experiment_control.subsequences.subsequences import *

globals_dict = {
    'mol power': MOL_POWER,
    'mol shutter': MOL_SHUTTER_BOOL
}

start()

#Adjust powers
tpower = 0
atom_power.constant(tpower,1)
mol_power.constant(tpower,globals_dict['mol power'])

#Open shutters
tshutter = tpower+1e-3
shutter_duration = 20e-3
digital_pulse(shutter_atom_trig,tshutter, shutter_duration)
if globals_dict['mol shutter']:
    digital_pulse(shutter_mol_trig,tshutter,shutter_duration)

#Fire YAG
t_YAG = 5e-3
digital_pulse(YAG_trig,t_YAG,tdur=0.5e-3)

#Acquire data
tstart = t_YAG - 2e-3
tend = tstart + 15e-3
atom_abs.acquire('Atom Absorption',tstart,tend)
mol_abs.acquire('Molecule Absorption',tstart,tend)

stop(25e-3)



