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
client.enableApiControl(True, vehicle_name="Drone1")
client.enableApiControl(True, vehicle_name="Drone2")


############ Define broadcast function ############



############ Go to the Gauge Test ############
print('Press "c" to fly to the Gauge Test')
while True:
    if keyboard.is_pressed('c'):
        break
print("Taking off...")
time.sleep(0.5)

client.takeoffAsync(vehicle_name="Drone1").join()
client.takeoffAsync(vehicle_name="Drone2").join()

takeoff1_1 = client.moveOnPathAsync([airsim.Vector3r(-415.405, 0, -2)],
                       15, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1")
takeoff1_2 = client.moveOnPathAsync([airsim.Vector3r(-441.27527344, 0, -1)],
                       15, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2")
takeoff1_1.join()
takeoff1_2.join()

takeoff2_1 = client.moveOnPathAsync([airsim.Vector3r(-421.405, 0, -2)],
                       3.5, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1")
takeoff2_2 = client.moveOnPathAsync([airsim.Vector3r(-445.27527344, 0, -1)],
                       7, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2")
takeoff2_1.join()
takeoff2_2.join()

takeoff3_1 = client.moveOnPathAsync([airsim.Vector3r(-421.405, -22.90003906, -1)],
                       2, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1")
takeoff3_2 = client.moveOnPathAsync([airsim.Vector3r(-445.27527344, -28.96500244, 14.5)],
                       2, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2")
takeoff3_1.join()
takeoff3_2.join()

takeoff4_1 = client.moveOnPathAsync([airsim.Vector3r(-421.405, -25.90003906, -1)],
                      1, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1")
takeoff4_2 = client.moveOnPathAsync([airsim.Vector3r(-445.27527344, -32.96500244, 14.5)],
                      1, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2")
takeoff4_1.join()
takeoff4_2.join()

time.sleep(2)

pose1 = client.simGetVehiclePose(vehicle_name="Drone1")
x_coordinate1 = pose1.position.x_val
y_coordinate1 = pose1.position.y_val
z_coordinate1 = pose1.position.z_val

pose2 = client.simGetVehiclePose(vehicle_name="Drone2")
x_coordinate2 = pose2.position.x_val
y_coordinate2 = pose2.position.y_val
z_coordinate2 = pose2.position.z_val - 15


############ Perform Gauge Test ############
print('Press "c" to start the Gauge Test')
while True:
    if keyboard.is_pressed('c'):
        break
time.sleep(0.5)

print('Performing Gauge Test...')

z_dev1 = 0
vz1 = 0
vz2 = 0
d = 0

moveUp = False
hasMovedUp = False

while (y_coordinate1 > -100.90004883):
    
    # Get distance sensor data
    right_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceRight", vehicle_name="Drone1")
    distance_from_right = right_distance_sensor_data.distance
    
    # Determine Drone1 movement
    if (z_dev1 < -0.1):
        vz1 = -0.1
        
    elif (z_dev1 > 0.1):
        vz1 = 0.1
        
    else:
        vz1 = 0
        
    m1 = client.moveByVelocityAsync(0, -1, vz1, 1, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
    
    # Determine Drone2 movement
    if (distance_from_right < 5):
        moveUp = True
        
    else:
        moveUp = False
    
    if ((distance_from_right > 5) and (hasMovedUp == True)):
        hasMovedUp = False

    if ((moveUp == True) and (hasMovedUp == False)):
        vz2 = -4.8
        hasMovedUp = True
        
        d = d + 10
        print(str(d) + 'm reached!')
        
    else:
        vz2 = 0

    m2 = client.moveToPositionAsync(x_coordinate2, y_coordinate2, (z_coordinate2 + 15) + vz2, 4.8, vehicle_name="Drone2")

    # Move
    m1.join()
    m2.join()
    
    # Get coordinates
    pose1 = client.simGetVehiclePose(vehicle_name="Drone1")
    x_coordinate1 = pose1.position.x_val
    y_coordinate1 = pose1.position.y_val
    z_coordinate1 = pose1.position.z_val

    pose2 = client.simGetVehiclePose(vehicle_name="Drone2")
    x_coordinate2 = pose2.position.x_val
    y_coordinate2 = pose2.position.y_val
    z_coordinate2 = pose2.position.z_val - 15
    
    z_dev1 = -2.5 - z_coordinate1
    

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
