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
client.enableApiControl(True, vehicle_name="Drone1")


############ Go to the Tube Test ############
print('Press "c" to fly to the Tube Test')
while True:
    if keyboard.is_pressed('c'):
        break
print("Taking off...")
time.sleep(0.5)

client.takeoffAsync(vehicle_name="Drone1").join()

client.moveOnPathAsync([airsim.Vector3r(-72.18, 0, -10)],
                       8, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()
client.moveOnPathAsync([airsim.Vector3r(-78.18, 0, -10)],
                       2, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()
client.moveOnPathAsync([airsim.Vector3r(-78.18, 23.91, -10)],
                       2, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()
client.moveOnPathAsync([airsim.Vector3r(-78.18, 25.91, -8)],
                       1, 5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()
time.sleep(2)


############ Perform Tube Test ############
print('Press "c" to start the Tube Test')
while True:
    if keyboard.is_pressed('c'):
        break
time.sleep(0.5)
print('Performing Tube Test...')

pose = client.simGetVehiclePose(vehicle_name="Drone1")
x_coordinate = pose.position.x_val
y_coordinate = pose.position.y_val
z_coordinate = pose.position.z_val

client.moveByVelocityAsync(0, 1, 0, 1, vehicle_name="Drone1").join()
direction_code = 0

front_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceFront", vehicle_name="Drone1")
distance_from_front = front_distance_sensor_data.distance
    
back_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceBack", vehicle_name="Drone1")
distance_from_back = back_distance_sensor_data.distance
    
left_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceLeft", vehicle_name="Drone1")
distance_from_left = left_distance_sensor_data.distance

right_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceRight", vehicle_name="Drone1")
distance_from_right = right_distance_sensor_data.distance
    
top_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceTop", vehicle_name="Drone1")
distance_from_top = top_distance_sensor_data.distance
    
bottom_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceBottom", vehicle_name="Drone1")
distance_from_bottom = bottom_distance_sensor_data.distance

# Direction Codes:
#
#       0: forward
#       1: backward
#       2: left
#       3: right
#       4: up
#       5: down

while (y_coordinate < 102.44):
    
    # Move
    if (direction_code == 0):
        client.moveByVelocityAsync(0, 1, 0, 0.5, vehicle_name="Drone1").join()

    elif (direction_code == 1):
        client.moveByVelocityAsync(0, -1, 0, 0.5, vehicle_name="Drone1").join()
        
    elif (direction_code == 2):
        client.moveByVelocityAsync(1, 0, 0, 0.5, vehicle_name="Drone1").join()
        
    elif (direction_code == 3):
        client.moveByVelocityAsync(-1, 0, 0, 0.5, vehicle_name="Drone1").join()

    elif (direction_code == 4):
        client.moveByVelocityAsync(0, 0, -2, 1, vehicle_name="Drone1").join()
        
    elif (direction_code == 5):
        client.moveByVelocityAsync(0, 0, 2, 1, vehicle_name="Drone1").join()
    
    # Get distance sensor data
    front_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceFront", vehicle_name="Drone1")
    distance_from_front = front_distance_sensor_data.distance
    
    back_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceBack", vehicle_name="Drone1")
    distance_from_back = back_distance_sensor_data.distance
    
    left_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceLeft", vehicle_name="Drone1")
    distance_from_left = left_distance_sensor_data.distance

    right_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceRight", vehicle_name="Drone1")
    distance_from_right = right_distance_sensor_data.distance
    
    top_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceTop", vehicle_name="Drone1")
    distance_from_top = top_distance_sensor_data.distance
    
    bottom_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceBottom", vehicle_name="Drone1")
    distance_from_bottom = bottom_distance_sensor_data.distance
    
    # Detect corner and change direction
    if (direction_code == 0):
        if (distance_from_front < 2.8):
            
            client.hoverAsync(vehicle_name="Drone1").join()
            
            temporary = [0, 0, distance_from_left, distance_from_right, distance_from_top, distance_from_bottom]
            direction_code = temporary.index(np.max(temporary))
            
            print('Turning corner!')
            
    elif (direction_code == 1):
        if (distance_from_back < 2.8):
            
            client.hoverAsync(vehicle_name="Drone1").join()
            
            temporary = [0, 0, distance_from_left, distance_from_right, distance_from_top, distance_from_bottom]
            direction_code = temporary.index(np.max(temporary))
            
    elif (direction_code == 2):
        if (distance_from_left < 2.8):
            
            client.hoverAsync(vehicle_name="Drone1").join()
            
            temporary = [distance_from_front, distance_from_back, 0, 0, distance_from_top, distance_from_bottom]
            direction_code = temporary.index(np.max(temporary))
            
            print('Turning corner!')
            
    elif (direction_code == 3):
        if (distance_from_right < 2.8):
            
            client.hoverAsync(vehicle_name="Drone1").join()
            
            temporary = [distance_from_front, distance_from_back, 0, 0, distance_from_top, distance_from_bottom]
            direction_code = temporary.index(np.max(temporary))
            
            print('Turning corner!')
            
    elif (direction_code == 4):
        if (distance_from_top < 2.8):
            
            client.hoverAsync(vehicle_name="Drone1").join()
            
            temporary = [distance_from_front, distance_from_back, distance_from_left, distance_from_right, 0, 0]
            direction_code = temporary.index(np.max(temporary))
            
            print('Turning corner!')
            
    elif (direction_code == 5):
        if (distance_from_bottom < 2.8):
            
            client.hoverAsync(vehicle_name="Drone1").join()
            
            temporary = [distance_from_front, distance_from_back, distance_from_left, distance_from_right, 0, 0]
            direction_code = temporary.index(np.max(temporary))
            
            print('Turning corner!')
    
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
