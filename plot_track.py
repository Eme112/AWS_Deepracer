import numpy as np
import matplotlib.pyplot as plt

# Load numpy array from file
waypoints = np.load('reinvent_base.npy')

# Extract the x and y coordinates of the waypoints
x_coords = waypoints[:, 0]
y_coords = waypoints[:, 1]
waypoint_nums = np.arange(len(x_coords))

# Plot the waypoints as red circles with annotations
plt.scatter(x_coords, y_coords, color='red')
for i in range(len(x_coords)):
    plt.annotate(str(waypoint_nums[i]), xy=(x_coords[i], y_coords[i]), color='black', fontsize=8, ha='center', va='center')

# Add axis labels and title
plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.title('DeepRacer Track Waypoints')

# Show the plot
plt.show()