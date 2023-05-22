# BLINKA_MCP2221=1 python3 main.py

import numpy as np
import board
import busio
import adafruit_mlx90640

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C!")

# Set refresh rate
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_1_HZ
print("MLX refresh rate: ", pow(2, (mlx.refresh_rate-1)), "Hz")


# Set up plot
fig, ax = plt.subplots()
grid_x, grid_y = np.mgrid[0:31:32j, 0:23:24j]

def update(i):
    # read in frame from thermal camera and split into 32 x 24 numpy array of thermal readings
    frame = [0] * 768
    mlx.getFrame(frame)
    pixels = np.split(np.asarray(frame), 24)
    # rotate it around so its right side
    pixels = np.rot90(pixels, 3)
    # Clear the current figure
    plt.clf()
    # Create a color plot with a rectangular grid
    plt.pcolormesh(grid_x, grid_y, pixels)
    plt.colorbar()
    plt.title("Animated MLX Thermal Camera (32x24)")
    plt.show()
    plt.pause(10)


animation = FuncAnimation(fig, update)

# writergif = PillowWriter(fps=0.1) 
# animation.save("animation.gif" , writer=writergif)

plt.show()