import setup_path
import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2

# Client
client = airsim.MultirotorClient()

# Reset Drone1
client.armDisarm(False, vehicle_name="Drone1")
client.enableApiControl(False, vehicle_name="Drone1")

# Reset Drone2
client.armDisarm(False, vehicle_name="Drone2")
client.enableApiControl(False, vehicle_name="Drone2")

# Reset wind
wind = airsim.Vector3r(0, 0, 0)
client.simSetWind(wind)
client.simEnableWeather(False)

# Reset
client.reset()