import lyse
import numpy as np
import matplotlib.pyplot as plt

# Is this script being run from within an interactive lyse session?
if lyse.spinning_top:
    # If so, use the filepath of the current shot
    h5_path = lyse.path
else:
    # If not, get the filepath of the last shot of the lyse DataFrame
    df = lyse.data()
    h5_path = df.filepath.iloc[-1]

run = lyse.Run(h5_path)

# Get a dictionary of the global variables used in this shot
run_globals = run.get_globals()
print(run_globals)

# extract the traces
trace_names = [
    "Atom Absorption",
    "Molecule Absorption",
]
trace_data = {}

for trace_name in trace_names:
    trace_data[trace_name] = run.get_trace(trace_name)

plt.figure(figsize=(10, 6))

for trace_name, (time, values) in trace_data.items():
    plt.plot(time, values, label=trace_name)


plt.ylim(0, 1.6)

plt.xlabel('Time')
plt.ylabel('Values')
plt.title('Trace Plots')
plt.legend()
plt.grid(True)

plt.show()

# Compute a result based on the data processing and save it to the 'results' group of
# the shot file
ai1_int = trace_data["Atom Absorption"][1].mean()
ai1_int_err = trace_data["Atom Absorption"][1].std()/np.sqrt(len(trace_data["Atom Absorption"][1]))
run.save_result('atom_abs integrated', ai1_int)
run.save_result('atom_abs integrated err', ai1_int_err)
