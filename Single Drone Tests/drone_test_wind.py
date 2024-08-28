import setup_path
import airsim

import numpy as np
from numpy import abs
import os
import tempfile
import pprint
import cv2
import time
import keyboard

############ Connect to the AirSim simulator ############
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True, vehicle_name="Drone1")


############ Go to the Wind Test ############
print('Press "c" to fly to the Wind Test')
while True:
    if keyboard.is_pressed('c'):
        break
print("Taking off...")
time.sleep(0.5)

client.takeoffAsync(vehicle_name="Drone1").join()

client.moveOnPathAsync([airsim.Vector3r(0, -19.52, -3)],
                       3, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()
time.sleep(2)


############ Perform Rings Test ############
print('Press "c" to start the Wind Test')
while True:
    if keyboard.is_pressed('c'):
        break
time.sleep(0.5)
print('Performing Wind Test...')

client.moveOnPathAsync([airsim.Vector3r(0, -22.52, -8.3)],
                       1, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()
time.sleep(2)

# Enable wind
wind = airsim.Vector3r(-20, 0, 0)
client.simSetWind(wind)
client.simEnableWeather(True)
client.simSetWeatherParameter(airsim.WeatherParameter.Dust,0.5)

pose = client.simGetVehiclePose(vehicle_name="Drone1")
x_coordinate = pose.position.x_val
y_coordinate = pose.position.y_val
z_coordinate = pose.position.z_val

while (y_coordinate > -78):
    
    # Adjust velocity
    if ( (abs(x_coordinate) > 5) or (abs(-8.3 - z_coordinate) > 5) ):
        velocity = 8
    else:
        velocity = 4
        
    client.moveToPositionAsync(0, (y_coordinate - 6), -8.3, velocity).join()
    
    # Get coordinates
    pose = client.simGetVehiclePose(vehicle_name="Drone1")
    x_coordinate = pose.position.x_val
    y_coordinate = pose.position.y_val
    z_coordinate = pose.position.z_val

print('Finished!')
time.sleep(2)


############ Reset to spawn ############
print('Press "x" to return to spawn')
while True:
    if keyboard.is_pressed('x'):
        break
time.sleep(0.5)

client.reset()
client.armDisarm(False, vehicle_name="Drone1")
client.enableApiControl(False, vehicle_name="Drone1")

# Disable wind
wind = airsim.Vector3r(0, 0, 0)
client.simSetWind(wind)
client.simEnableWeather(False)
