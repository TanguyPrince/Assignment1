from stepcounter import read_data
from stepcounter import count_steps
from enhanced import StepCounter

window_size = 4 # Adjust the window size as needed
discard_window_size = 10  # Adjust the discard window size as needed

timestamps, x_array, y_array, z_array = read_data("out.csv")

#print(count_steps(timestamps, x_array, y_array, z_array))

step_counter = StepCounter(window_size, discard_window_size)

for x, y, z in zip(x_array, y_array, z_array):
    step_count = step_counter.count_steps([x], [y], [z])  # Convert x, y, and z values to lists

print("Number of steps:", step_count)