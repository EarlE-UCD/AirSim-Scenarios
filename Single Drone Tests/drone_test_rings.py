import setup_path
import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2
import time
import keyboard

############ Connect to the AirSim simulator ############
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True,vehicle_name="Drone1")


############ Go to the Rings Test ############
print('Press "c" to fly to the Rings Test')
while True:
    if keyboard.is_pressed('c'):
        break
time.sleep(0.5)
print("Taking off...")

client.takeoffAsync(vehicle_name="Drone1").join()

client.moveOnPathAsync([airsim.Vector3r(0, 20, -3)],
                       3, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()
time.sleep(2)


############ Perform Rings Test ############
print('Press "c" to start the Rings Test')
while True:
    if keyboard.is_pressed('c'):
        break
time.sleep(0.5)
print('Performing Rings Test...')

client.moveOnPathAsync([airsim.Vector3r(0, 23, -10),],
                       1, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()

client.moveOnPathAsync([airsim.Vector3r(0, 56.3, -10),
                        airsim.Vector3r(20, 76.3, -10),
                        airsim.Vector3r(-20, 116.3, -10),
                        airsim.Vector3r(-10, 126.3, -10)],
                       5, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()

client.moveOnPathAsync([airsim.Vector3r(0, 136.3, -10),],
                       1, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()

client.moveOnPathAsync([airsim.Vector3r(0, 136.3, -45.5),],
                       8, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()

client.moveOnPathAsync([airsim.Vector3r(0, 136.3, -52.5),],
                       1, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()

client.moveOnPathAsync([airsim.Vector3r(0, 76.5, -52.5),],
                       4, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()

client.moveOnPathAsync([airsim.Vector3r(0, 74.5, -52.5),],
                       0.5, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()

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
