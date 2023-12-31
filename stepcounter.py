import numpy as np
import matplotlib.pyplot as plt
import csv


#Simple function to visualize 4 arrays that are given to it
def visualize_data(timestamps, x_arr,y_arr,z_arr,s_arr):
  #Plotting accelerometer readings
  plt.figure(1)
  plt.plot(timestamps, x_arr, color = "blue",linewidth=1.0)
  plt.plot(timestamps, y_arr, color = "red",linewidth=1.0)
  plt.plot(timestamps, z_arr, color = "green",linewidth=1.0)
  plt.show()
  #magnitude array calculation
  m_arr = []
  for i, x in enumerate(x_arr):
    m_arr.append(magnitude(x_arr[i],y_arr[i],z_arr[i]))
  plt.figure(2)
  #plotting magnitude and steps
  plt.plot(timestamps, s_arr, color = "black",linewidth=1.0)
  plt.plot(timestamps, m_arr, color = "red",linewidth=1.0)
  plt.show()

#Function to read the data from the log file
#TODO Read the measurements into array variables and return them
def read_data(filename):
  #TODO implementation
  timestamps, x_array, y_array, z_array = [], [], [], []
  with open(filename) as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
    for row in reader:  # each row is a list
      timestamps.append(row[0])
      x_array.append(row[1])
      y_array.append(row[2])
      z_array.append(row[3])
  return timestamps, x_array, y_array, z_array
  #return [0],[0],[0],[0]

#Function to count steps.
#Should return an array of timestamps from when steps were detected
#Each value in this arrray should represent the time that step was made.
def count_steps(timestamps, x_arr, y_arr, z_arr):
  #TODO: Actual implementation
  # Calculate the magnitude of acceleration
  # Set static threshold values for peak detection
  threshold = 13 # Adjust this threshold based on your data

  # Initialize step count
  step_count = 0

  # Convert input arrays to NumPy arrays
  x_arr = np.array(x_arr)
  y_arr = np.array(y_arr)
  z_arr = np.array(z_arr)

  # Calculate the magnitude of acceleration for each data point
  acceleration_magnitude = []
  for i in range(len(x_arr)):
    magnitude = np.sqrt(x_arr[i] ** 2 + y_arr[i] ** 2 + z_arr[i] ** 2)
    acceleration_magnitude.append(magnitude)

  i = 1  # Start from the second data point
  while i < len(acceleration_magnitude) - 1:
    if (
            acceleration_magnitude[i] > threshold and
            acceleration_magnitude[i] > acceleration_magnitude[i - 1] and
            acceleration_magnitude[i] > acceleration_magnitude[i + 1]
    ):
      step_count += 1
      i += 1  # Increment i to avoid double counting a step
    i += 1  # Always increment i to move to the next data point

  return step_count


#Calculate the magnitude of the given vector
def magnitude(x,y,z):
  return np.linalg.norm((x,y,z))

#Function to convert array of times where steps happened into array to give into graph visualization
#Takes timestamp-array and array of times that step was detected as an input
#Returns an array where each entry is either zero if corresponding timestamp has no step detected or 50000 if the step was detected
def generate_step_array(timestamps, step_time):
  s_arr = []
  ctr = 0
  for i, time in enumerate(timestamps):
    if(ctr<len(step_time) and step_time[ctr]<=time):
      ctr += 1
      s_arr.append( 50000 )
    else:
      s_arr.append( 0 )
  while(len(s_arr)<len(timestamps)):
    s_arr.append(0)
  return s_arr

#Check that the sizes of arrays match
def check_data(t,x,y,z):
  if( len(t)!=len(x) or len(y)!=len(z) or len(x)!=len(y) ):
    print("Arrays of incorrect length")
    return False
  print("The amount of data read from accelerometer is "+str(len(t))+" entries")
  return True

def main():
  #read data from a measurement file, change the inoput file name if needed
  timestamps, x_array, y_array, z_array = read_data("accelerometer_data.csv")
  #Chek that the data does not produce errors
  if(not check_data(timestamps, x_array,y_array,z_array)):
    return
  #Count the steps based on array of measurements from accelerometer
  st = count_steps(timestamps, x_array, y_array, z_array)
  #Print the result
  print("This data contains "+str(len(st))+" steps according to current algorithm")
  #convert array of step times into graph-compatible format
  s_array = generate_step_array(timestamps, st)
  #visualize data and steps
  visualize_data(timestamps, x_array,y_array,z_array,s_array)


