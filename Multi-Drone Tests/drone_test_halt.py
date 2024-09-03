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


############ Go to the Halt Test ############
print('Press "c" to fly to the Halt Test')
while True:
    if keyboard.is_pressed('c'):
        break
print("Taking off...")
time.sleep(0.5)

client.takeoffAsync(vehicle_name="Drone1").join()
client.takeoffAsync(vehicle_name="Drone2").join()

takeoff1_1 = client.moveOnPathAsync([airsim.Vector3r(-215.79189453, 0, -1)],
                       15, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1")
takeoff1_2 = client.moveOnPathAsync([airsim.Vector3r(-187.66736328, 0, -1)],
                       15, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2")
takeoff1_1.join()
takeoff1_2.join()

takeoff1_1 = client.moveOnPathAsync([airsim.Vector3r(-220.79189453, 0, -1)],
                       2, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1")
takeoff1_2 = client.moveOnPathAsync([airsim.Vector3r(-192.66736328, 0, -1)],
                       2, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2")
takeoff1_1.join()
takeoff1_2.join()

takeoff3_1 = client.moveOnPathAsync([airsim.Vector3r(-220.79189453, 18.92218018, -4.5)],
                       3, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1")
takeoff3_2 = client.moveOnPathAsync([airsim.Vector3r(-192.66736328, 39.92217773, 10.5)],
                       3, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2")
takeoff3_1.join()
takeoff3_2.join()

takeoff4_1 = client.moveOnPathAsync([airsim.Vector3r(-220.79189453, 22.92218018, -4.5)],
                      1, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1")
takeoff4_2 = client.moveOnPathAsync([airsim.Vector3r(-203.79189453, 39.92217773, 11.5)],
                       1, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2")
takeoff4_1.join()
takeoff4_2.join()

time.sleep(2)


############ Perform Halt Test ############
print('Press "c" to start the Halt Test')
while True:
    if keyboard.is_pressed('c'):
        break
time.sleep(0.5)
print('Performing Halt Test...')

pose1 = client.simGetVehiclePose(vehicle_name="Drone1")
x_coordinate1 = pose1.position.x_val
y_coordinate1 = pose1.position.y_val
z_coordinate1 = pose1.position.z_val

pose2 = client.simGetVehiclePose(vehicle_name="Drone2")
x_coordinate2 = pose2.position.x_val
y_coordinate2 = pose2.position.y_val
z_coordinate2 = pose2.position.z_val - 15

droneSeparation = np.sqrt( (x_coordinate1 - x_coordinate2)**2 + (y_coordinate1 - y_coordinate2)**2 + (z_coordinate1 - z_coordinate2)**2 )

client.moveByVelocityAsync(0, 1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1").join()
client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2").join()

direction_code1 = 0
direction_code2 = 1
checkpointBuffer = 20

checkpointReached1 = False
checkpointReached2 = False
closeDrones = False

front_distance_sensor_data1 = client.getDistanceSensorData(distance_sensor_name="DistanceFront", vehicle_name="Drone1")
distance_from_front1 = front_distance_sensor_data1.distance

bottom_distance_sensor_data1 = client.getDistanceSensorData(distance_sensor_name="DistanceBottom", vehicle_name="Drone1")
distance_from_bottom1 = bottom_distance_sensor_data1.distance
    
left_distance_sensor_data1 = client.getDistanceSensorData(distance_sensor_name="DistanceLeft", vehicle_name="Drone1")
distance_from_left1 = left_distance_sensor_data1.distance

right_distance_sensor_data1 = client.getDistanceSensorData(distance_sensor_name="DistanceRight", vehicle_name="Drone1")
distance_from_right1 = right_distance_sensor_data1.distance

###

front_distance_sensor_data2 = client.getDistanceSensorData(distance_sensor_name="DistanceFront", vehicle_name="Drone2")
distance_from_front2 = front_distance_sensor_data2.distance

bottom_distance_sensor_data2 = client.getDistanceSensorData(distance_sensor_name="DistanceBottom", vehicle_name="Drone2")
distance_from_bottom2 = bottom_distance_sensor_data2.distance
    
left_distance_sensor_data2 = client.getDistanceSensorData(distance_sensor_name="DistanceLeft", vehicle_name="Drone2")
distance_from_left2 = left_distance_sensor_data2.distance

right_distance_sensor_data2 = client.getDistanceSensorData(distance_sensor_name="DistanceRight", vehicle_name="Drone2")
distance_from_right2 = right_distance_sensor_data2.distance


# Direction Codes:
#
#       0: left
#       1: right

while (y_coordinate1 < 136.92217773):
    
    # Move
    
    if ((checkpointReached1 == False) and (closeDrones == False)):
        
        if (direction_code1 == 0):
            m1 = client.moveByVelocityAsync(0, 1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        
        elif (direction_code1 == 1):
            m1 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
            
    elif (checkpointReached1 == True):
        
        m1 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
    
    ###
    
    if (checkpointReached2 == False):
        
        if (direction_code2 == 0):
            m2 = client.moveByVelocityAsync(0, 1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
        elif (direction_code2 == 1):
            m2 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
            
    elif (checkpointReached2 == True):
        
        m1 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")

    ###
    
    if ((checkpointReached1 == True) and (checkpointReached2 == True)):
        
        checkpointBuffer = 0
        checkpointReached1 = False
        checkpointReached2 = False
        print('Both drones have reached a checkpoint! Resuming movement...')

    ###
        
    m1.join()
    m2.join()
    
    # Get distance sensor data
            
    front_distance_sensor_data1 = client.getDistanceSensorData(distance_sensor_name="DistanceFront", vehicle_name="Drone1")
    distance_from_front1 = front_distance_sensor_data1.distance
    
    bottom_distance_sensor_data1 = client.getDistanceSensorData(distance_sensor_name="DistanceBottom", vehicle_name="Drone1")
    distance_from_bottom1 = bottom_distance_sensor_data1.distance
    
    left_distance_sensor_data1 = client.getDistanceSensorData(distance_sensor_name="DistanceLeft", vehicle_name="Drone1")
    distance_from_left1 = left_distance_sensor_data1.distance

    right_distance_sensor_data1 = client.getDistanceSensorData(distance_sensor_name="DistanceRight", vehicle_name="Drone1")
    distance_from_right1 = right_distance_sensor_data1.distance
    
    if (checkpointBuffer > 20):
        
        if (distance_from_bottom1 < 4):
            checkpointReached1 = True

    ###
    
    front_distance_sensor_data2 = client.getDistanceSensorData(distance_sensor_name="DistanceFront", vehicle_name="Drone2")
    distance_from_front2 = front_distance_sensor_data2.distance
    
    bottom_distance_sensor_data2 = client.getDistanceSensorData(distance_sensor_name="DistanceBottom", vehicle_name="Drone2")
    distance_from_bottom2 = bottom_distance_sensor_data2.distance
    
    left_distance_sensor_data2 = client.getDistanceSensorData(distance_sensor_name="DistanceLeft", vehicle_name="Drone2")
    distance_from_left2 = left_distance_sensor_data2.distance

    right_distance_sensor_data2 = client.getDistanceSensorData(distance_sensor_name="DistanceRight", vehicle_name="Drone2")
    distance_from_right2 = right_distance_sensor_data2.distance
    
    if (checkpointBuffer > 20):
        
        if (distance_from_bottom2 < 4):
            checkpointReached2 = True

    ###
    
    checkpointBuffer = checkpointBuffer + 1

    # Alter direction
    
    if (checkpointReached1 == False):
        
        if (direction_code1 == 0):
            if (distance_from_front1 < 4.5):
            
                m1 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
                direction_code1 = 1
            
                
        elif (direction_code1 == 1):
            if (distance_from_front1 < 4.5):
            
                m1 = client.moveByVelocityAsync(0, 1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
                direction_code1 = 0
           
    ###
    
    if (checkpointReached2 == False):
        
        if (direction_code2 == 0):
            if (distance_from_front2 < 4.5):
            
                m2 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
                direction_code2 = 1
            
                
        elif (direction_code2 == 1):
            if (distance_from_front2 < 4.5):
            
                m2 = client.moveByVelocityAsync(0, 1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
                direction_code2 = 0

    ###
    
    m1.join()
    m2.join()

    # Get coordinates
    
    pose1 = client.simGetVehiclePose(vehicle_name="Drone1")
    x_coordinate1 = pose1.position.x_val
    y_coordinate1 = pose1.position.y_val
    z_coordinate1 = pose1.position.z_val
    
    ###
    
    pose2 = client.simGetVehiclePose(vehicle_name="Drone2")
    x_coordinate2 = pose2.position.x_val
    y_coordinate2 = pose2.position.y_val
    z_coordinate2 = pose2.position.z_val - 15
    
    ###
    
    droneSeparation = np.sqrt( (x_coordinate1 - x_coordinate2)**2 + (y_coordinate1 - y_coordinate2)**2 + (z_coordinate1 - z_coordinate2)**2 )
    
    if (droneSeparation < 10):
        
        closeDrones = True
        
    else:
        
        closeDrones = False
    

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
