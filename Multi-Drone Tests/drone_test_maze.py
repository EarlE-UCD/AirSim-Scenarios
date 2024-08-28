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


############ Go to the Maze Test ############
print('Press "c" to fly to the Maze Test')
while True:
    if keyboard.is_pressed('c'):
        break
print("Taking off...")
time.sleep(0.5)

client.takeoffAsync(vehicle_name="Drone1").join()
client.takeoffAsync(vehicle_name="Drone2").join()

takeoff1_1 = client.moveOnPathAsync([airsim.Vector3r(-158.08, 0, -6)],
                       8, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1")
takeoff1_2 = client.moveOnPathAsync([airsim.Vector3r(-158.08, 0, -1)],
                       8, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2")
takeoff1_1.join()
takeoff1_2.join()


takeoff2_1 = client.moveOnPathAsync([airsim.Vector3r(-162.08, 0, -6)],
                       2, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1")
takeoff2_2 = client.moveOnPathAsync([airsim.Vector3r(-162.08, 0, 7)],
                       2, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2")
takeoff2_1.join()
takeoff2_2.join()

takeoff3_1 = client.moveOnPathAsync([airsim.Vector3r(-162.08, 23.70, -6)],
                       2, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1")
takeoff3_2 = client.moveOnPathAsync([airsim.Vector3r(-162.08, 18.70, 8)],
                       1.5, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2")
takeoff3_1.join()
takeoff3_2.join()

takeoff4_1 = client.moveOnPathAsync([airsim.Vector3r(-162.08, 27.70, -5)],
                       0.5, 5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1")
takeoff4_2 = client.moveOnPathAsync([airsim.Vector3r(-162.08, 22.70, 10)],
                       0.5, 5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2")
takeoff4_1.join()
takeoff4_2.join()

time.sleep(2)


############ Perform Maze Test ############
print('Press "c" to start the Maze Test')
while True:
    if keyboard.is_pressed('c'):
        break
time.sleep(0.5)
print('Performing Maze Test...')

pose1 = client.simGetVehiclePose(vehicle_name="Drone1")
x_coordinate1 = pose1.position.x_val
y_coordinate1 = pose1.position.y_val
z_coordinate1 = pose1.position.z_val

client.moveByVelocityAsync(0, 1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1").join()
direction_code = 0

front_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceFront", vehicle_name="Drone1")
distance_from_front = front_distance_sensor_data.distance
    
left_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceLeft", vehicle_name="Drone1")
distance_from_left = left_distance_sensor_data.distance

right_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceRight", vehicle_name="Drone1")
distance_from_right = right_distance_sensor_data.distance

x_checkpoint = []
y_checkpoint = []
z_checkpoint = []

# Direction Codes:
#
#       0: forward
#       1: left
#       2: right
#       3: backward

while (y_coordinate1 < 116):
    
    # Move
    
    if (direction_code == 0):
        client.moveByVelocityAsync(0, 1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1").join()
        
    elif (direction_code == 1):
        client.moveByVelocityAsync(1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1").join()
        
    elif (direction_code == 2):
        client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1").join()
        
    elif (direction_code == 3):
        client.moveByVelocityAsync(0, -1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1").join()
    
    # Get distance sensor data
    
    front_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceFront", vehicle_name="Drone1")
    distance_from_front = front_distance_sensor_data.distance
    
    left_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceLeft", vehicle_name="Drone1")
    distance_from_left = left_distance_sensor_data.distance
    
    right_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceRight", vehicle_name="Drone1")
    distance_from_right = right_distance_sensor_data.distance

    # Choose direction
    
    if (direction_code == 0):
        if (distance_from_front < 6):
            
            temporary = client.simGetVehiclePose(vehicle_name="Drone1")
            temporary_x = temporary.position.x_val
            temporary_y = temporary.position.y_val
            temporary_z = temporary.position.z_val + 15
            
            x_checkpoint.append(temporary_x)
            y_checkpoint.append(temporary_y)
            z_checkpoint.append(temporary_z)
            
            if (distance_from_left > distance_from_right):
                
                direction_code = 1
                print('Turning left!')
                client.moveByVelocityAsync(1, 0, 0, 3, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1").join()
                
            elif (distance_from_left < distance_from_right):
                
                direction_code = 2
                print('Turning right!')
                client.moveByVelocityAsync(-1, 0, 0, 3, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1").join()
                
    elif (direction_code == 1):
        if (distance_from_front < 6):
            
            temporary = client.simGetVehiclePose(vehicle_name="Drone1")
            temporary_x = temporary.position.x_val
            temporary_y = temporary.position.y_val
            temporary_z = temporary.position.z_val + 15
            
            x_checkpoint.append(temporary_x)
            y_checkpoint.append(temporary_y)
            z_checkpoint.append(temporary_z)
            
            if (distance_from_left > distance_from_right):
                
                direction_code = 3
                print('Turning left!')
                client.moveByVelocityAsync(0, -1, 0, 3, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1").join()
                
            elif (distance_from_left < distance_from_right):
                
                direction_code = 0
                print('Turning right!')
                client.moveByVelocityAsync(0, 1, 0, 3, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1").join()
                
    elif (direction_code == 2):
        if (distance_from_front < 6):
            
            temporary = client.simGetVehiclePose(vehicle_name="Drone1")
            temporary_x = temporary.position.x_val
            temporary_y = temporary.position.y_val
            temporary_z = temporary.position.z_val + 15
            
            x_checkpoint.append(temporary_x)
            y_checkpoint.append(temporary_y)
            z_checkpoint.append(temporary_z)
            
            if (distance_from_left > distance_from_right):
                
                direction_code = 0
                print('Turning left!')
                client.moveByVelocityAsync(0, 1, 0, 3, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1").join()
                
            elif (distance_from_left < distance_from_right):
                
                direction_code = 3
                print('Turning right!')
                client.moveByVelocityAsync(0, -1, 0, 3, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1").join()
                
    elif (direction_code == 3):
        if (distance_from_front < 6):
            
            temporary = client.simGetVehiclePose(vehicle_name="Drone1")
            temporary_x = temporary.position.x_val
            temporary_y = temporary.position.y_val
            temporary_z = temporary.position.z_val + 15
            
            x_checkpoint.append(temporary_x)
            y_checkpoint.append(temporary_y)
            z_checkpoint.append(temporary_z)
            
            if (distance_from_left > distance_from_right):
                
                direction_code = 2
                print('Turning left!')
                client.moveByVelocityAsync(-1, 0, 0, 3, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1").join()
                
            elif (distance_from_left < distance_from_right):
                
                direction_code = 1
                print('Turning right!')
                client.moveByVelocityAsync(1, 0, 0, 3, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1").join()

    # Get coordinates
    
    pose1 = client.simGetVehiclePose(vehicle_name="Drone1")
    x_coordinate1 = pose1.position.x_val
    y_coordinate1 = pose1.position.y_val
    z_coordinate1 = pose1.position.z_val

temporary = client.simGetVehiclePose(vehicle_name="Drone1")
temporary_x = temporary.position.x_val
temporary_y = temporary.position.y_val
temporary_z = temporary.position.z_val + 10
            
x_checkpoint.append(temporary_x)
y_checkpoint.append(temporary_y)
z_checkpoint.append(temporary_z)

print('Copying flight path with 2nd drone...')
time.sleep(1)

for i in range(0, len(x_checkpoint)):
    
    client.moveOnPathAsync([airsim.Vector3r(x_checkpoint[i], y_checkpoint[i], z_checkpoint[i])],
                           5, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2").join()
    
    if (i < (len(x_checkpoint) - 1)):
        print('Turning corner!')

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
