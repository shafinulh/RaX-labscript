import lyse
from pylab import *
import numpy as np
import matplotlib.pyplot as plt

df = lyse.data()

mol_power = df["MOL_POWER"]
integrated_signal = df["lessons_with_shafin", "atom_abs integrated"]
integrated_signal_err = df["lessons_with_shafin", "atom_abs integrated err"]

plt.figure('Testing, attention please', figsize = (6,10))

plt.errorbar(mol_power, integrated_signal, yerr = integrated_signal_err,
         marker = 'o',
         ls = '')

plt.xlabel('final analog ramp voltgae')
plt.ylabel('Integrated Signal')
plt.title('Analog Ramp Voltage vs. Signal')
plt.grid(True)

plt.show()