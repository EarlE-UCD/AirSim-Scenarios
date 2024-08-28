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

#


############ Define movement function ############

def moveAlongPath(x_checkpoint, y_checkpoint):
    
    while (np.sqrt( (x_checkpoint - x_coordinate1)**2 + (y_checkpoint - x_coordinate1)**2 ) < 1):
        
        pose1 = client.simGetVehiclePose(vehicle_name="Drone1")
        x_coordinate1 = pose1.position.x_val
        y_coordinate1 = pose1.position.y_val
        z_coordinate1 = pose1.position.z_val

        pose2 = client.simGetVehiclePose(vehicle_name="Drone2")
        x_coordinate2 = pose2.position.x_val
        y_coordinate2 = pose2.position.y_val
        z_coordinate2 = pose2.position.z_val - 15
        
        x_diff = x_checkpoint - x_coordinate1
        y_diff = y_checkpoint - y_coordinate1
        
        vx = np.cos( np.arctan( np.absolute( y_diff / x_diff ) ) )
        vy = np.sin( np.arctan( np.absolute( y_diff / x_diff ) ) )
        
        if ( (x_diff > 0) and (y_diff > 0) ):
            client.moveByVelocityAsync(vx, vy, 0, 0.5, vehicle_name="Drone1")
            
        elif ( (x_diff < 0) and (y_diff > 0) ):
            client.moveByVelocityAsync(-vx, vy, 0, 0.5, vehicle_name="Drone1")
            
        elif ( (x_diff < 0) and (y_diff < 0) ):
            client.moveByVelocityAsync(-vx, -vy, 0, 0.5, vehicle_name="Drone1")
            
        elif ( (x_diff > 0) and (y_diff < 0) ):
            client.moveByVelocityAsync(vx, -vy, 0, 0.5, vehicle_name="Drone1")
            

############ Go to the Broadcast Test ############
print('Press "c" to fly to the Broadcast Test')
while True:
    if keyboard.is_pressed('c'):
        break
print("Taking off...")
time.sleep(0.5)

client.takeoffAsync(vehicle_name="Drone1").join()
client.takeoffAsync(vehicle_name="Drone2").join()

takeoff1_1 = client.moveOnPathAsync([airsim.Vector3r(-127.98508789, 0, -4)],
                       10, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1")
takeoff1_2 = client.moveOnPathAsync([airsim.Vector3r(-233.991875, 0, -4)],
                       10, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2")
takeoff1_1.join()
takeoff1_2.join()

takeoff1_1 = client.moveOnPathAsync([airsim.Vector3r(-137.98508789, 0, -4)],
                       2, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1")
takeoff1_2 = client.moveOnPathAsync([airsim.Vector3r(-243.991875, 0, -4)],
                       2, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2")
takeoff1_1.join()
takeoff1_2.join()

takeoff3_1 = client.moveOnPathAsync([airsim.Vector3r(-137.98508789, -19.76316162, -2)],
                       4, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1")
takeoff3_2 = client.moveOnPathAsync([airsim.Vector3r(-243.991875, -125.73412109, 13)],
                       6, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2")
takeoff3_1.join()
takeoff3_2.join()

takeoff4_1 = client.moveOnPathAsync([airsim.Vector3r(-137.98508789, -23.76316162, -2)],
                      0.5, 5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1")
takeoff4_2 = client.moveOnPathAsync([airsim.Vector3r(-243.991875, -129.73412109, 13)],
                      0.5, 5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2")
takeoff4_1.join()
takeoff4_2.join()

takeoff5_2 = client.moveOnPathAsync([airsim.Vector3r(-243.991875, -129.73412109, 13)],
                      0.1, 5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2")
takeoff5_2.join()

time.sleep(2)

client.hoverAsync(vehicle_name="Drone1").join()
client.hoverAsync(vehicle_name="Drone2").join()

pose1 = client.simGetVehiclePose(vehicle_name="Drone1")
x_coordinate1 = pose1.position.x_val
y_coordinate1 = pose1.position.y_val
z_coordinate1 = pose1.position.z_val

pose2 = client.simGetVehiclePose(vehicle_name="Drone2")
x_coordinate2 = pose2.position.x_val
y_coordinate2 = pose2.position.y_val
z_coordinate2 = pose2.position.z_val - 15


############ Select maximum broadcast distance ############
print('...')
time.sleep(1)
print('Select a maximum broadcast distance by pressing one of the following keys:')
print('1: 25 meters')
print('2: 50 meters')
print('3: 75 meters')
print('4: 100 meters')

while True:
    if keyboard.is_pressed('1'):
        maxBroadcastDistance = 25
        break
    
    elif keyboard.is_pressed('2'):
        maxBroadcastDistance = 50
        break
    
    elif keyboard.is_pressed('3'):
        maxBroadcastDistance = 75
        break
    
    elif keyboard.is_pressed('4'):
        maxBroadcastDistance = 100
        break

print('...')
time.sleep(1)
print('Maximum broadcast distance sleected: ' + str(maxBroadcastDistance) + ' meters')

############ Perform Broadcast Test ############
print('Press "c" to start the Broadcast Test')
while True:
    if keyboard.is_pressed('c'):
        break
time.sleep(0.5)

print('Performing Broadcast Test...')

# First Segment
moveAlongPath(-322.99244141, -153.20548828)

# # Second Segment
# moveAlongPath(-189.15558594, -164.93179688)

# # Third Segment
# moveAlongPath(-238.64027344, -115.510)

# # Fourth Segment
# moveAlongPath(-157.42811523, -101.18171875)

# # Fifth Segment
# moveAlongPath(-137.98508789, -235.80910156)

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
