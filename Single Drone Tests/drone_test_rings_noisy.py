import setup_path
import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2
import time
import keyboard
import random
from random import random as rand

############ Connect to the AirSim simulator ############
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True,vehicle_name="Drone1")


############ Go to the Rings Test (noisy version) ############
print('Press "c" to fly to the Rings Test (noisy version)')
while True:
    if keyboard.is_pressed('c'):
        break
time.sleep(0.5)
print("Taking off...")

client.takeoffAsync(vehicle_name="Drone1").join()

client.moveOnPathAsync([airsim.Vector3r(0, 20, -3)],
                       3, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()
time.sleep(2)


############ Perform Rings Test (noisy version) ############
print('Press "c" to start the Rings Test (noisy version)')
while True:
    if keyboard.is_pressed('c'):
        break
time.sleep(0.5)
print('Performing Rings Test (noisy version)...')

client.moveOnPathAsync([airsim.Vector3r(0, 23, -10)],
                       1, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()

client.moveOnPathAsync([airsim.Vector3r(0 + (4*rand() - 2), 56.3 + (4*rand() - 2), -10 + (4*rand() - 2)),
                        airsim.Vector3r(20 + (4*rand() - 2), 76.3 + (4*rand() - 2), -10 + (4*rand() - 2)),
                        airsim.Vector3r(-20 + (4*rand() - 2), 116.3 + (4*rand() - 2), -10 + (4*rand() - 2)),
                        airsim.Vector3r(-10 + (4*rand() - 2), 126.3 + (4*rand() - 2), -10 + (4*rand() - 2))],
                       5, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()

client.moveOnPathAsync([airsim.Vector3r(0 + (4*rand() - 2), 136.3 + (4*rand() - 2), -10 + (4*rand() - 2)),],
                       1, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()

client.moveOnPathAsync([airsim.Vector3r(0 + (4*rand() - 2), 136.3 + (4*rand() - 2), -45.5 + (4*rand() - 2)),],
                       8, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()

client.moveOnPathAsync([airsim.Vector3r(0 + (4*rand() - 2), 136.3 + (4*rand() - 2), -52.5 + (4*rand() - 2)),],
                       1, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()

client.moveOnPathAsync([airsim.Vector3r(0 + (4*rand() - 2), 76.5 + (4*rand() - 2), -52.5 + (4*rand() - 2)),],
                       4, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()

client.moveOnPathAsync([airsim.Vector3r(0 + (4*rand() - 2), 74.5 + (4*rand() - 2), -52.5 + (4*rand() - 2)),],
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
