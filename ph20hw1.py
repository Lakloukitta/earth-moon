import numpy as np
import yaml
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# loading the file with orbital elements
with open("orbital_parameters.yaml", "r") as file:
    params = yaml.safe_load(file)

# defining the Constants
G = float(params['G'])  
M_sun = float(params['M_sun'])  
M_earth = float(params['M_earth'])  
M_moon = float(params['M_moon'])  

# defining time parameters
dt = 6 * 60 * 60  
num_steps = 1460  

sun_size = 50  

# initial positions of earth and moon
r_earth = np.array([float(params['d_earth_sun']), 0], dtype=float)  
r_moon = r_earth + np.array([float(params['d_moon_earth']), 0], dtype=float)  

# initial velocities 
v_earth = np.array([0, 29.78e3], dtype=float)  
v_moon_relative = np.array([0, 1.022e3], dtype=float) 
v_moon = v_earth + v_moon_relative  #

# storing positions
earth_positions = np.zeros((num_steps, 2), dtype=float)
moon_positions = np.zeros((num_steps, 2), dtype=float)


for i in range(num_steps):
    # computing distances
    r_earth_sun = np.linalg.norm(r_earth)  
    r_moon_sun = np.linalg.norm(r_moon) 
    r_moon_earth = np.linalg.norm(r_moon - r_earth) 

    # gravitational forces for sun, moon, and earth
    F_earth_sun = -G * M_sun * M_earth / r_earth_sun**2 * (r_earth / r_earth_sun)  
    F_moon_sun = -G * M_sun * M_moon / r_moon_sun**2 * (r_moon / r_moon_sun)  
    F_moon_earth = -G * M_earth * M_moon / r_moon_earth**2 * ((r_moon - r_earth) / r_moon_earth)  

    v_earth += F_earth_sun / M_earth * dt  
    v_moon += (F_moon_sun + F_moon_earth) / M_moon * dt  


    r_earth += v_earth * dt
    r_moon += v_moon * dt

    # storing positions
    earth_positions[i] = r_earth
    moon_positions[i] = r_moon

# plotting
plt.figure(figsize=(8, 8))
plt.plot(earth_positions[:, 0], earth_positions[:, 1], label="Earth Orbit")
plt.plot(moon_positions[:, 0], moon_positions[:, 1], label="Moon Orbit")
plt.scatter(0, 0, color='yellow', s=sun_size, label="Sun")
plt.xlabel("x (meters)")
plt.ylabel("y (meters)")
plt.title(" Plot of Earth-Moon-Sun System ")
plt.legend()
plt.grid(True)
plt.show()

fig, ax = plt.subplots(figsize=(6, 6))

# setting  axis 
ax.set_xlim(-2 * 1.5e11, 2 * 1.5e11)
ax.set_ylim(-2 * 1.5e11, 2 * 1.5e11)

# sun is fixed
sun = ax.scatter(0, 0, color='yellow', s=50, label="Sun")

earth, = ax.plot([], [], 'bo', markersize=10, label='Earth')
moon, = ax.plot([], [], 'ro', markersize=5, label='Moon')

def update(frame):
    earth.set_data(earth_positions[frame, 0], earth_positions[frame, 1])
    moon.set_data(moon_positions[frame, 0], moon_positions[frame, 1])
    return earth, moon

ani = FuncAnimation(fig, update, frames=num_steps, interval=10, blit=True)

plt.legend()
plt.title(" Animated Earth-Moon-Sun Orbit ")

plt.show()


########################################################################################################################
# Pseudocode Comments (Placed at the End):
#
# 1. Load Parameters
# 2. Set Initial Conditions
# 3. Prepare Arrays for Storing Positions
# 4. Main Simulation Loop (Euler’s Method):
#      - For each time step :
#      - Calculate the current distances between the Earth-Sun, Moon-Sun, and Moon-Earth 
#      - Calculate the gravitational forces acting on the Earth  and the Moon 
#      - Update the velocities of the Earth and Moon using the forces
#      - Update the positions of the Earth and Moon using their updated velocities 
#      - Store the new positions for plotting after the loop.
#
# 5.Plot of Orbits
# 6. Animation Setup
# 7. Create and Show Animation
########################################################################################################################
# M_earth * d²r_earth/dt² = -G * M_sun * M_earth / |r_earth_sun|² * (r_earth / |r_earth_sun|)
 # M_moon * d²r_moon/dt² = -G * M_sun * M_moon / |r_moon_sun|² * (r_moon / |r_moon_sun|)
#                          - G * M_earth * M_moon / |r_moon_earth|² * (r_moon - r_earth) / |r_moon_earth|)