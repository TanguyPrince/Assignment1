from stepcounter import read_data
from stepcounter import count_steps



timestamps, x_array, y_array, z_array = read_data("out.csv")


print(count_steps(timestamps, x_array, y_array, z_array))
