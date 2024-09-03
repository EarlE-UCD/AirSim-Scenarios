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


############ Go to the Steps Test ############
print('Press "c" to fly to the Steps Test')
while True:
    if keyboard.is_pressed('c'):
        break
time.sleep(0.5)
print("Taking off...")
time.sleep(0.5)

client.takeoffAsync(vehicle_name="Drone1").join()

client.moveOnPathAsync([airsim.Vector3r(41.4, 0, -2.66)],
                       5, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()
client.moveOnPathAsync([airsim.Vector3r(46.4, 0, -2.66)],
                       2, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1").join()
time.sleep(2)


############ Perform Steps Test ############
print('Press "c" to start the Steps Test')
while True:
    if keyboard.is_pressed('c'):
        break
time.sleep(0.5)
print('Performing Steps Test...')

pose = client.simGetVehiclePose(vehicle_name="Drone1")
x_coordinate = pose.position.x_val

while (x_coordinate < 106.14631836):
    
    # Check x_coordinate
    pose = client.simGetVehiclePose(vehicle_name="Drone1")
    x_coordinate = pose.position.x_val

    # Get distance sensor data
    front_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceFront", vehicle_name="Drone1")
    distance_from_front = front_distance_sensor_data.distance
    
    bottom_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceBottom", vehicle_name="Drone1")
    distance_from_bottom = bottom_distance_sensor_data.distance

    # Control velocity direction
    if (distance_from_front < 4):
        print('Wall detected! Moving up!')
        
        while (distance_from_front < 4):
            front_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceFront", vehicle_name="Drone1")
            distance_from_front = front_distance_sensor_data.distance
            
            client.moveByVelocityAsync(0, 0, -1.2, 1, vehicle_name="Drone1").join()
        
    elif (distance_from_bottom < 1):
        print('Too close to the floor! Moving up!')
        
        while (distance_from_bottom < 1):
            bottom_distance_sensor_data = client.getDistanceSensorData(distance_sensor_name="DistanceBottom", vehicle_name="Drone1")
            distance_from_bottom = bottom_distance_sensor_data.distance
            
            client.moveByVelocityAsync(0, 0, -1.2, 1, vehicle_name="Drone1").join()
        
    else:
        client.moveByVelocityAsync(1.2, 0, 0, 1, vehicle_name="Drone1").join()

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
