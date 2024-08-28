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

def broadcastDrone2ToDrone1():
    
    separationDistance = np.sqrt( (x_coordinate2 - x_coordinate1)**2 + (y_coordinate2 - y_coordinate1)**2 )

    if (separationDistance <= 20):
        
        print('...')
        print('Message receieved! The drones are less than 20m apart! Precisely, ' + str(separationDistance) + 'm!')
        
    elif (separationDistance <= 40):
        
        print('...')
        print('Message receieved! The drones are less than 40m apart! Precisely, ' + str(separationDistance) + 'm!')
        
    elif (separationDistance <= 60):
        
        print('...')
        print('Message receieved! The drones are less than 60m apart! Precisely, ' + str(separationDistance) + 'm!')
        
    elif (separationDistance > 60):
        
        print('...')
        print('No message detected! The drones are separated by more than the maximum detection distance of 60m!')


############ Go to the Mirror Test ############
print('Press "c" to fly to the Mirror Test')
while True:
    if keyboard.is_pressed('c'):
        break
print("Taking off...")
time.sleep(0.5)

client.takeoffAsync(vehicle_name="Drone1").join()
client.takeoffAsync(vehicle_name="Drone2").join()

takeoff1_1 = client.moveOnPathAsync([airsim.Vector3r(-336.663125, 0, -2)],
                       15, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1")
takeoff1_2 = client.moveOnPathAsync([airsim.Vector3r(-336.663125, 0, -2)],
                       15, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2")
takeoff1_1.join()
takeoff1_2.join()

takeoff2_1 = client.moveOnPathAsync([airsim.Vector3r(-336.663125, 22.68601318, -2)],
                       3.5, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1")
takeoff2_2 = client.moveOnPathAsync([airsim.Vector3r(-336.663125, 116.70591797, 13)],
                       7, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2")
takeoff2_1.join()
takeoff2_2.join()

takeoff3_1 = client.moveOnPathAsync([airsim.Vector3r(-346.663125, 22.68601318, -2)],
                       2, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1")
takeoff3_2 = client.moveOnPathAsync([airsim.Vector3r(-346.663125, 116.70591797, 13)],
                       2, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone2")
takeoff3_1.join()
takeoff3_2.join()

takeoff4_1 = client.moveOnPathAsync([airsim.Vector3r(-351.663125, 22.68601318, -2)],
                      1, 10000000, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), -1, 1, vehicle_name="Drone1")
takeoff4_2 = client.moveOnPathAsync([airsim.Vector3r(-351.663125, 116.70591797, 13)],
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
z_coordinate2 = pose2.position.z_val

############ Perform Mirror Test ############
print('Press "c" to start the Mirror Test')
while True:
    if keyboard.is_pressed('c'):
        break
time.sleep(0.5)

print('Performing Mirror Test...')

##### First segment #####
segmentFinished1 = False
segmentFinished2 = False

while True:
    
    # Move
    if ( (segmentFinished1 == False) and (segmentFinished2 == False) ):
        m1 = client.moveByVelocityAsync(-1, 0, 0, 1, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(-1, 0, 0, 1, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished1 == False):
        m1 = client.moveByVelocityAsync(-1, 0, 0, 1, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, 0, 0, 1, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished2 == False):
        m1 = client.moveByVelocityAsync(0, 0, 0, 1, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(-1, 0, 0, 1, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    else:
        print("Turning corner!")
        break
    
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
    z_coordinate2 = pose2.position.z_val
    
    if keyboard.is_pressed('q'):
        broadcastDrone2ToDrone1()

    if (x_coordinate1 < -361.250):
        segmentFinished1 = True
        
    if (x_coordinate2 < -361.250):
        segmentFinished2 = True
            
##### Second segment #####
segmentFinished1 = False
segmentFinished2 = False

while True:
    
    # Move
    if ( (segmentFinished1 == False) and (segmentFinished2 == False) ):
        m1 = client.moveByVelocityAsync(0, 1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, -1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished1 == False):
        m1 = client.moveByVelocityAsync(0, 1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished2 == False):
        m1 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, -1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    else:
        print("Turning corner!")
        break
    
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
    z_coordinate2 = pose2.position.z_val
    
    if keyboard.is_pressed('q'):
        broadcastDrone2ToDrone1()
    
    if (y_coordinate1 > 43.92148438):
        segmentFinished1 = True
        
    if (y_coordinate2 < 95.60591797):
        segmentFinished2 = True
        
##### Third segment #####
segmentFinished1 = False
segmentFinished2 = False

while True:
    
    # Move 
    if ( (segmentFinished1 == False) and (segmentFinished2 == False) ):
        m1 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished1 == False):
        m1 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished2 == False):
        m1 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    else:
        print("Turning corner!")
        break
    
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
    z_coordinate2 = pose2.position.z_val
    
    if keyboard.is_pressed('q'):
        broadcastDrone2ToDrone1()
    
    if (x_coordinate1 < -376.450):
        segmentFinished1 = True
        
    if (x_coordinate2 < -376.450):
        segmentFinished2 = True
        
##### Fourth segment #####
segmentFinished1 = False
segmentFinished2 = False

while True:
    
    # Move
    if ( (segmentFinished1 == False) and (segmentFinished2 == False) ):
        m1 = client.moveByVelocityAsync(0, 1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, -1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished1 == False):
        m1 = client.moveByVelocityAsync(0, 1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished2 == False):
        m1 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, -1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    else:
        print("Turning corner!")
        break
    
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
    z_coordinate2 = pose2.position.z_val
    
    if keyboard.is_pressed('q'):
        broadcastDrone2ToDrone1()
    
    if (y_coordinate1 > 52.41969727):
        segmentFinished1 = True
        
    if (y_coordinate2 < 87.15591797):
        segmentFinished2 = True
        
##### Fifth segment #####
segmentFinished1 = False
segmentFinished2 = False

while True:
    
    # Move
    if ( (segmentFinished1 == False) and (segmentFinished2 == False) ):
        m1 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished1 == False):
        m1 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished2 == False):
        m1 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    else:
        print("Turning corner!")
        break
    
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
    z_coordinate2 = pose2.position.z_val
    
    if keyboard.is_pressed('q'):
        broadcastDrone2ToDrone1()
    
    if (x_coordinate1 < -387.000):
        segmentFinished1 = True
        
    if (x_coordinate2 < -387.000):
        segmentFinished2 = True
        
##### Sixth segment #####
segmentFinished1 = False
segmentFinished2 = False

while True:
    
    # Move
    if ( (segmentFinished1 == False) and (segmentFinished2 == False) ):
        m1 = client.moveByVelocityAsync(0, -1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, 1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished1 == False):
        m1 = client.moveByVelocityAsync(0, -1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished2 == False):
        m1 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, 1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    else:
        print("Turning corner!")
        break
    
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
    z_coordinate2 = pose2.position.z_val
    
    if keyboard.is_pressed('q'):
        broadcastDrone2ToDrone1()
    
    if (y_coordinate1 < 31.1763501):
        segmentFinished1 = True
    
    if (y_coordinate2 > 108.35591797):
        segmentFinished2 = True
        
##### Seventh segment #####
segmentFinished1 = False
segmentFinished2 = False

while True:
    
    # Move
    if ( (segmentFinished1 == False) and (segmentFinished2 == False) ):
        m1 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished1 == False):
        m1 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished2 == False):
        m1 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    else:
        print("Turning corner!")
        break
    
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
    z_coordinate2 = pose2.position.z_val
    
    if keyboard.is_pressed('q'):
        broadcastDrone2ToDrone1()
    
    if (x_coordinate1 < -409.550):
        segmentFinished1 = True
        
    if (x_coordinate2 < -409.550):
        segmentFinished2 = True
        
##### Eight segment #####
segmentFinished1 = False
segmentFinished2 = False

while True:
    
    # Move
    if ( (segmentFinished1 == False) and (segmentFinished2 == False) ):
        m1 = client.moveByVelocityAsync(0, 1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, -1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished1 == False):
        m1 = client.moveByVelocityAsync(0, 1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished2 == False):
        m1 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, -1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    else:
        print("Turning corner!")
        break
    
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
    z_coordinate2 = pose2.position.z_val
    
    if keyboard.is_pressed('q'):
        broadcastDrone2ToDrone1()
    
    if (y_coordinate1 > 65.16469727):
        segmentFinished1 = True
    
    if (y_coordinate2 < 74.45591797):
        segmentFinished2 = True

##### Ninth segment #####
segmentFinished1 = False
segmentFinished2 = False

while True:
    
    # Move
    if ( (segmentFinished1 == False) and (segmentFinished2 == False) ):
        m1 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished1 == False):
        m1 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished2 == False):
        m1 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    else:
        print("Turning corner!")
        break
    
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
    z_coordinate2 = pose2.position.z_val
    
    if keyboard.is_pressed('q'):
        broadcastDrone2ToDrone1()
    
    if (x_coordinate1 < -424.300):
        segmentFinished1 = True
        
    if (x_coordinate2 < -424.300):
        segmentFinished2 = True
        
##### Tenth segment #####
segmentFinished1 = False
segmentFinished2 = False

while True:
    
    # Move
    if ( (segmentFinished1 == False) and (segmentFinished2 == False) ):
        m1 = client.moveByVelocityAsync(0, -1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, 1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished1 == False):
        m1 = client.moveByVelocityAsync(0, -1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished2 == False):
        m1 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, 1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    else:
        print("Turning corner!")
        break
    
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
    z_coordinate2 = pose2.position.z_val
    
    if keyboard.is_pressed('q'):
        broadcastDrone2ToDrone1()
    
    if (y_coordinate1 < 43.54320801):
        segmentFinished1 = True
    
    if (y_coordinate2 > 96.05591797):
        segmentFinished2 = True
        
##### Eleventh segment #####
segmentFinished1 = False
segmentFinished2 = False

while True:
    
    # Move
    if ( (segmentFinished1 == False) and (segmentFinished2 == False) ):
        m1 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished1 == False):
        m1 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished2 == False):
        m1 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    else:
        print("Turning corner!")
        break
    
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
    z_coordinate2 = pose2.position.z_val
    
    if keyboard.is_pressed('q'):
        broadcastDrone2ToDrone1()
    
    if (x_coordinate1 < -435.100):
        segmentFinished1 = True
        
    if (x_coordinate2 < -435.100):
        segmentFinished2 = True
        
##### Twelfth segment #####
segmentFinished1 = False
segmentFinished2 = False

while True:
    
    # Move
    if ( (segmentFinished1 == False) and (segmentFinished2 == False) ):
        m1 = client.moveByVelocityAsync(0, -1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, 1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished1 == False):
        m1 = client.moveByVelocityAsync(0, -1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished2 == False):
        m1 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, 1, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    else:
        print("Turning corner!")
        break
    
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
    z_coordinate2 = pose2.position.z_val
    
    if keyboard.is_pressed('q'):
        broadcastDrone2ToDrone1()
    
    if (y_coordinate1 < 23.71784424):
        segmentFinished1 = True
    
    if (y_coordinate2 > 115.70591797):
        segmentFinished2 = True
        
##### Thirteenth segment #####
segmentFinished1 = False
segmentFinished2 = False

while True:
    
    # Move
    if ( (segmentFinished1 == False) and (segmentFinished2 == False) ):
        m1 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished1 == False):
        m1 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    elif (segmentFinished2 == False):
        m1 = client.moveByVelocityAsync(0, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone1")
        m2 = client.moveByVelocityAsync(-1, 0, 0, 0.5, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), vehicle_name="Drone2")
        
    else:
        print("Turning corner!")
        break
    
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
    z_coordinate2 = pose2.position.z_val
    
    if keyboard.is_pressed('q'):
        broadcastDrone2ToDrone1()
    
    if (x_coordinate1 < -444.66363281):
        segmentFinished1 = True
        
    if (x_coordinate2 < -444.66363281):
        segmentFinished2 = True

print('Finished!')
time.sleep(2)
airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0)


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
