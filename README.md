# Welcome to the AirSim Scenario Simulator

This project uses Microsoft's AirSim to simulate different drone flight scenarios. The project consists of twelve different flight scenarios that demonstrate different drone functionalities, namely navigation, perception, and planning, as well as communication between separate drones. A custom map is used for this project, and this map consists of a different course for each of the twelve flight scenarios.  Each scenario is designed to highlight a certain drone functionality.

![image](https://github.com/user-attachments/assets/e9ab848a-aeac-4a2a-9f70-78ee61507759)


## Demonstrations

**Video**

(insert video here)


**Gifs**

*Rings Test*: Demonstrates **planning** by moving through a series of rings based on predetermined coordinates

![ringsTestGif](https://github.com/user-attachments/assets/7a0076b5-2833-4a1e-9617-a71eb15f520e)


*Tube Test*: Demonstrates **navigation** by moving through a tube with turns and **perception** by using distance sensors to detect corners in the tube

![tubeTestGif](https://github.com/user-attachments/assets/2853a550-6b56-48fc-8e31-3c8b1ef5e97a)


*Corner Test*: Demonstrates **planning** by moving in a telegraphed straight path and **communication** by having drones move on diverging paths when they detect that they are close to each other; this also demonstrates communication being used for collision avoidance when two drones are not in each others' line of sight

![cornerTestGif](https://github.com/user-attachments/assets/34860802-8536-4e6b-8867-2692cdf09a4a)


*Up-down Test*: Demonstrates **planning** by having the bottom drone move in a predictable straight path, **perception** b having the bottom drone detect indicators, and **communication** by having the bottom drone communicate the detection of these indicators to the top drone to influence the top drone's movement; this also demonstrates communication being used in a way in which the signal from one drone affects the movement of another drone

![updownTestGif](https://github.com/user-attachments/assets/de873ddb-d682-43f6-8d83-0cf40c1cc728)


## How to setup the project

**Required Software**
- Conda environment with Python 3.6
- Unreal Engine 4.27

**Steps**
1) Download the Unreal Project file for this project in the following Google Drive folder: https://drive.google.com/drive/folders/1_LDcNGHn1BbTyQ0k0bJot1F8ht8U57MJ?usp=sharing
2) Create an Unreal Project containing AirSim by following AirSim's documentation (https://microsoft.github.io/AirSim/unreal_custenv/) or the following video: https://www.youtube.com/watch?v=BVkN3CCMg4A
3) In project folder, replace the created Unreal Project file with the custom Unreal Project file downloaded earlier
4) Update the settings.json file (found in the "AirSim" folder) to match the settings.json folder uploaded to this repository
5) Create a Conda environment using Python 3.6


## How this project works

Once the AirSim is loaded onto an Unreal Engine project with the custom map, the Python scripts for the different scenarios can be run by doing the following:

1) Run the project
2) Activate the Conda environment created for this project
3) Navigate to the folder containing the Python scripts
4) Use the command line in the conda environment to run one of the scripts
5) Once the script is running, press the appropriate keys according to the printed prompts to proceed through the scenario


## Miscellaneous notes for the simulator

**Resetting the simulator**
- If you need to cancel the performance of the task, it is recommanded that you stop the current process with ctrl+c on the command line and then run the script reset_simulator.py before pausing or stopping the project from running; this is to prevent the Unreal Engine from freezing when attempting to stop the project while a task is still running

**Coordiates**
- In the AirSim APIs, the +z-direction is downward, but in the Unreal Engine editor, the +z-direction is upward
- The "coordinate" (e.g. x_coordinate, y_coordinate, z_coordinate) variables used in the Python scripts use a coordinate system that has its origin located at the spawn position of Drone1 and has the +z-direction pointing upward to be consistent with the convention used by the Unreal Editor
- The spawn position of Drone1 is located slightly above the origin in the Unreal Environment, located at (0m, 0m, 2.02868713m)
- The "coordinates" variables in the Python scripts are determined by the "pose" of each drone, which is its position and orientation relative to its spawn point (https://microsoft.github.io/AirSim/api_docs/html/#airsim.types.Pose)
    - The spawn point of Drone2 is 15m above the spawn point of Drone1, meaning that in order to determine the "coordinate" variables for Drone2, 15m is subtracted from its pose

**Takeoff flight times**
- For some of the flight scenarios, it takes awhile for the drones to fly from spawn to the corresponding course and position themselves to start the course

**Lighting**
- It is recommended to use "medium" lighting quality in the Unreal Project
- Make sure to build the lighting before running the project to avoid awkward shadows
