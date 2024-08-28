import setup_path
import airsim

import numpy as np
from numpy import pi
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
client.enableApiControl(True,vehicle_name="Drone2")


############ Go to the Corner Test ############
print('Press "c" to fly to the Corner Test')
while True:
    if keyboard.is_pressed('c'):
        break
time.sleep(0.5)
print("Taking off...")

client.takeoffAsync(vehicle_name="Drone1").join()
client.takeoffAsync(vehicle_name="Drone2").join()

turn2 = client.moveByAngleRatesThrottleAsync(0, 0, -pi/2, 0.6, 1, vehicle_name="Drone2")
turn2.join()

takeoff1_1 = client.moveToPositionAsync(-108.34, 0, -15, 8, vehicle_name="Drone1")
takeoff1_2 = client.moveToPositionAsync(-87.59, 0, -5, 8, vehicle_name="Drone2")
takeoff1_1.join()
takeoff1_2.join()

takeoff2_1 = client.moveToPositionAsync(-112.34, 0, -15, 0.5, vehicle_name="Drone1")
takeoff2_2 = client.moveToPositionAsync(-91.59, 0, -5, 0.5, vehicle_name="Drone2")
takeoff2_1.join()
takeoff2_2.join()

time.sleep(3)

takeoff3_1 = client.moveToPositionAsync(-112.34, -31.46, -15.5, 3, vehicle_name="Drone1")
takeoff3_2 = client.moveToPositionAsync(-91.59, -52.20, -0.5, 3, vehicle_name="Drone2")
takeoff3_1.join()
takeoff3_2.join()

takeoff4_1 = client.moveToPositionAsync(-112.34, -35.46, -15.5, 0.5, vehicle_name="Drone1")
takeoff4_2 = client.moveToPositionAsync(-91.59, -56.20, -0.5, 0.5, vehicle_name="Drone2")
takeoff4_1.join()
takeoff4_2.join()

client.hoverAsync(vehicle_name="Drone1")
client.hoverAsync(vehicle_name="Drone2")

time.sleep(1)

pose1 = client.simGetVehiclePose(vehicle_name="Drone1")
x_coordinate1 = pose1.position.x_val
y_coordinate1 = pose1.position.y_val
z_coordinate1 = pose1.position.z_val

pose2 = client.simGetVehiclePose(vehicle_name="Drone2")
x_coordinate2 = pose2.position.x_val
y_coordinate2 = pose2.position.y_val
z_coordinate2 = pose2.position.z_val - 15

time.sleep(2)


############ Perform Corner Test ############
print('Press "c" to start the Corner Test')
while True:
    if keyboard.is_pressed('c'):
        break
time.sleep(0.5)
print('Performing Corner Test...')

while (x_coordinate1 < -90):
    
    test1_1 = client.moveByVelocityAsync(1.5, 0, 0, 1, vehicle_name="Drone1")
    test1_2 = client.moveByVelocityAsync(0, 1.5, 0, 1, vehicle_name="Drone2")
    test1_1.join()
    test1_2.join()
    
    pose1 = client.simGetVehiclePose(vehicle_name="Drone1")
    x_coordinate1 = pose1.position.x_val
    y_coordinate1 = pose1.position.y_val
    z_coordinate1 = pose1.position.z_val

    pose2 = client.simGetVehiclePose(vehicle_name="Drone2")
    x_coordinate2 = pose2.position.x_val
    y_coordinate2 = pose2.position.y_val
    z_coordinate2 = pose2.position.z_val - 15
    
    if (np.sqrt( (x_coordinate1 - x_coordinate2)**2 + (y_coordinate1 - y_coordinate2)**2 + (z_coordinate1 - z_coordinate2)**2) < 5):
        
        print("Close drone detected!")

        test2_1 = client.moveByVelocityAsync(0, 0, -3.5, 1, vehicle_name="Drone1")
        test2_2 = client.moveByVelocityAsync(0, 0, 3.5, 1, vehicle_name="Drone2")
        test2_1.join()
        test2_2.join()

test3_1 = client.moveToPositionAsync(-91.59, -56.70, -15.5, 2, vehicle_name="Drone1")
test3_1.join()

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
client.armDisarm(False, vehicle_name="Drone2")
client.enableApiControl(False, vehicle_name="Drone2")
