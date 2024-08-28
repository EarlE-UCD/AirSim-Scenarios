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


############ Go to the Clash Test ############
print('Press "c" to fly to the Clash Test')
while True:
    if keyboard.is_pressed('c'):
        break
time.sleep(0.5)
print("Taking off...")

client.takeoffAsync(vehicle_name="Drone1").join()
client.takeoffAsync(vehicle_name="Drone2").join()

turn1 = client.moveByAngleRatesThrottleAsync(0, 0, pi/2, 0.6, 1, vehicle_name="Drone1")
turn2 = client.moveByAngleRatesThrottleAsync(0, 0, -pi/2, 0.6, 1, vehicle_name="Drone2")
turn1.join()
turn2.join()

takeoff1_1 = client.moveToPositionAsync(-45.41, 0, -15, 7, vehicle_name="Drone1")
takeoff1_2 = client.moveToPositionAsync(-45.41, 0, -5, 7, vehicle_name="Drone2")
takeoff1_1.join()
takeoff1_2.join()

takeoff2_1 = client.moveToPositionAsync(-47.41, 0, -15, 0.5, vehicle_name="Drone1")
takeoff2_2 = client.moveToPositionAsync(-47.41, 0, -5, 0.5, vehicle_name="Drone2")
takeoff2_1.join()
takeoff2_2.join()

time.sleep(3)

takeoff3_1 = client.moveToPositionAsync(-47.41, -19.63, -15, 3, vehicle_name="Drone1")
takeoff3_2 = client.moveToPositionAsync(-47.41, -97.19, 0, 3, vehicle_name="Drone2")
takeoff3_1.join()
takeoff3_2.join()

takeoff4_1 = client.moveToPositionAsync(-47.41, -24.63, -15, 1, vehicle_name="Drone1")
takeoff4_2 = client.moveToPositionAsync(-47.41, -102.19, 0, 1, vehicle_name="Drone2")
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


############ Perform Clash Test ############
print('Press "c" to start the Clash Test')
while True:
    if keyboard.is_pressed('c'):
        break
time.sleep(0.5)
print('Performing Clash Test...')

avoidance = False

while (y_coordinate1 > -90):
    
    test1_1 = client.moveByVelocityAsync(0, -4, 0, 1, vehicle_name="Drone1")
    test1_2 = client.moveByVelocityAsync(0, 4, 0, 1, vehicle_name="Drone2")
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
    
    if ( (np.absolute(y_coordinate1 - y_coordinate2) < 8) and (avoidance == False) ):
        
        print("Close drone detected!")
        avoidance = True

        test2_1 = client.moveByVelocityAsync(0, 0, -3, 1, vehicle_name="Drone1")
        test2_2 = client.moveByVelocityAsync(0, 0, 3, 1, vehicle_name="Drone2")
        test2_1.join()
        test2_2.join()

test3_1 = client.moveToPositionAsync(-47.41, -102.19, -15, 1, vehicle_name="Drone1")
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
