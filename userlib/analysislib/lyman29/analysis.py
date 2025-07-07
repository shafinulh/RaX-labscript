#Post-shot analysis code. Adjusted from Lyse website 
# example, "Single shot analysis with global file opening"

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

# # Get a dictionary of the global variables used in this shot
# run_globals = run.get_globals()
# print(run_globals)

# extract the traces
trace_data = {}
trace_data["Absorption"] = run.get_trace("Absorption")


#extract the image
image_data = run.get_image("camera","fluorescence", "frame")

fig = plt.figure(4, figsize=(10, 4))
# Create a gridspec layout with 1 row and 2 columns, and set the width ratio
gs = fig.add_gridspec(1, 2, width_ratios=[2, 1])

#get global variable
global_dict = run.get_globals()
tYAG = float(global_dict['tYAG'])

################Comment this out if you don't want to view##################
# First subplot (top-left) - analog output vs time
ax1 = fig.add_subplot(gs[0, 0])  # The first subplot
for (name, analog_data) in trace_data.items():
    times = analog_data[0].reshape(1, np.shape(analog_data)[1])
    times = times.flatten()
    values = analog_data[1].reshape(1, np.shape(analog_data)[1])
    values = values.flatten()
    # print(type(values))
    ax1.plot(times*1000, values, 'b')
    ax1.axvline(x=tYAG*1000, color='r', linestyle='--', label='Ablation')
    ax1.set_xlim([0, 15])
ax1.set_xlabel('Time [ms]', fontsize=16)
ax1.set_ylabel('Values', fontsize=16)
ax1.set_title('Analog Output vs Time')
ax1.grid(True)

# Second subplot (top-right) - fluorescence image
ax2 = fig.add_subplot(gs[0, 1])  # The second subplot
ax2.imshow(image_data, extent=[0, 512, 0, 512], cmap='magma',vmin=1568,vmax=1700) # you may want to chenge vmin, vmax depending on your LIF probe power
ax2.set_title('Fluorescence Image', fontsize=16)
ax2.set_xlabel('x', fontsize=16)
ax2.set_ylabel('y', fontsize=16)
#########################################################################################


# Adjust layout
plt.tight_layout()  # Automatically adjusts subplot params for better spacing
plt.show()




# Compute a result based on the data processing and save it to the 'results' group of
# the shot file
analog_int = trace_data["Absorption"][1].mean()
analog_int_err = trace_data["Absorption"][1].std()/np.sqrt(len(trace_data["Absorption"][1])) #Why divide with sqrt of N?
run.save_result('BaF_abs integrated', analog_int)
run.save_result('BaF_abs integrated err', analog_int_err)

# print(np.shape(image_data))
### For scatter reduction purposes
#pixel_sum = np.sum(image_data) #just to look at the sum
photon_counting_threshold = 1810#1570 #for 1x1 binning! #1810 for 4x4 binning
pixel_sum = np.mean(image_data > photon_counting_threshold)
###
run.save_result('pixel_sum', pixel_sum)


 