import numpy as np
import matplotlib.pyplot as plt

TS = 0.002

# Reading Data
with open("data-battery.txt", "r") as data_file:
    data = data_file.read()

points = []
for line in data.split("\n"):
    if not line:
        break
    parts = line.split(",")
    time_millis = int(parts[0])
    left_angle_encoder = int(parts[1])
    right_angle_encoder = int(parts[2])
    left_angle_rad = left_angle_encoder / 780.0 * np.pi
    right_angle_rad = right_angle_encoder / 780.0 * np.pi
    command = int(parts[3])
    points.append((time_millis, left_angle_rad, right_angle_rad, command))

points = np.array(points)

# Find best model parameters
def float_range(start, end, steps):
    diff = end - start
    for i in range(steps + 1):
        percentage = i / steps
        yield start + diff * percentage


best_error = np.Infinity
best_c0 = None
best_c1 = None
for c0 in float_range(0.02, 0.03, 20):
    for c1 in float_range(0.002, 0.003, 20):
        print(c0, c1)

        a = np.array(((1, TS), (0, 1 - c0)))
        b = np.array([[0], [c1]])

        left_state = np.array((0, 0))

        cumulative_error = 0
        for i in range(len(points)):
            point = points[i]
            _, left_angle_rad, right_angle_rad, command = point

            avg_angle_rad = (left_angle_rad + right_angle_rad) / 2

            cumulative_error += np.square(avg_angle_rad - left_state[0])

            left_state = np.matmul(a, left_state) + np.matmul(b, np.array((command,)))

        if cumulative_error < best_error:
            print("---best_error---", cumulative_error)
            best_error = cumulative_error
            best_c0 = c0
            best_c1 = c1

# Simulation
print("best:", best_c0, best_c1)
a = np.array(((1, TS), (0, 1 - best_c0)))
b = np.array([[0], [best_c1]])

curr_time = 0
right_state = np.array((0, 0))
simulated_points = []
for i in range(len(points)):
    command = np.array((points[i][3],))
    right_state = np.matmul(a, right_state) + np.matmul(b, command)

    simulated_points.append((curr_time, right_state[0]))

    curr_time += 2
simulated_points = np.array(simulated_points)

plt.plot(points[:, 0], points[:, 1], label="left")
plt.plot(points[:, 0], points[:, 2], label="right")
plt.plot(points[:, 0], points[:, 3] / 255, label="command")
plt.plot(simulated_points[:, 0], simulated_points[:, 1], label="simulated")
plt.legend(loc="upper center")
plt.savefig("model-tuning.png", dpi=500)
plt.show()
