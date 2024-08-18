from labscript import (
    DigitalOut,
    AnalogOut,
    AnalogIn,
    start,
    stop,
    add_time_marker
)

def absorption_signal(ao_chan: AnalogOut):
    t=0
    ao_chan.constant(t=t, value=SIGNAL_VI)
    t=DIP_TI
    t+=ao_chan.sine4_reverse_ramp(
        t=t,
        initial=DIP_VF,
        final=SIGNAL_VI,
        duration=DIP_DOWN_DUR,
        samplerate=DIP_RATE,
        truncation=0.8
    )
    t+=ao_chan.sine_ramp(
        t=t,
        initial=DIP_VF,
        final=SIGNAL_VI,
        duration=DIP_UP_DUR,
        samplerate=DIP_RATE,
    )
    return t
