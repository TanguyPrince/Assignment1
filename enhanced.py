import numpy as np


class StepCounter:
    def __init__(self, window_size, discard_window_size):
        self.window_size = window_size
        self.discard_window_size = discard_window_size
        self.acceleration_magnitude_window = []
        self.threshold = 8.0  # Initial threshold (you can adjust this)
        self.step_count = 0

    def update_threshold(self):
        if len(self.acceleration_magnitude_window) == self.window_size:
            # Calculate the mean and standard deviation of the windowed acceleration magnitudes
            mean = np.mean(self.acceleration_magnitude_window)
            std_dev = np.std(self.acceleration_magnitude_window)

            # Update the threshold dynamically
            self.threshold = mean + (std_dev * 1.64)  # You can adjust the multiplier

    def calculate_magnitude(self, x_values, y_values, z_values):
        # Convert input lists to NumPy arrays
        x_arr = np.array(x_values)
        y_arr = np.array(y_values)
        z_arr = np.array(z_values)

        return np.sqrt(x_arr ** 2 + y_arr ** 2 + z_arr ** 2)

    def count_steps(self, x_values, y_values, z_values):
        # Calculate the acceleration magnitude
        acceleration_magnitude = self.calculate_magnitude(x_values, y_values, z_values)

        # Add the current acceleration magnitude to the window
        self.acceleration_magnitude_window.append(acceleration_magnitude)

        # Check if the window size has been reached
        if len(self.acceleration_magnitude_window) == self.window_size:
            # Update the threshold
            self.update_threshold()

            # Check for steps within the window
            for i in range(len(self.acceleration_magnitude_window) - 1):
                if (
                        self.acceleration_magnitude_window[i] > self.threshold and
                        self.acceleration_magnitude_window[i] > self.acceleration_magnitude_window[i + 1]
                ):
                    self.step_count += 1

            # Remove the oldest value to maintain the window size
            self.acceleration_magnitude_window.pop(0)

        return self.step_count