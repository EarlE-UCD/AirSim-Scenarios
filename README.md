# Welcome to the AirSim Scenario Simulator

This project uses Microsoft's AirSim to simulate different drone flight scenarios. The project consists of twelve different flight scenarios that demonstrate different drone functionalities, namely navigation, perception, and planning, as well as communication between separate drones. A custom map is used for this project, and this map consists of a different course for each of the twelve flight scenarios.  Each scenario is designed to highlight a certain drone functionality (or some combination of functionalities) or some specific aspect of a functionality (e.g. latency or maximum broadcast distance in communication demonstrations).

![image](https://github.com/user-attachments/assets/e9ab848a-aeac-4a2a-9f70-78ee61507759)


## Download the map

Download the map for this project in this Google Drive folder: https://drive.google.com/drive/folders/1_LDcNGHn1BbTyQ0k0bJot1F8ht8U57MJ?usp=sharing

## How to setup the project

(explanation here)
- Python 3.6
- Unreal Engine 4.27


## How this project works

Once the AirSim is loaded onto an Unreal Engine project with the custom map, the Python scripts for the different scenarios can be run by doing the following:

1) Run the project
2) Use the command line in a conda environment to run one of the scripts
3) Once the script is running, press the appropriate keys according to the printed prompts to proceed through the scenario


## Miscellaneous notes for the simulator

Resetting the simulator:
- If you need to cancel the performance of the task, it is recommanded that you stop the current process with ctrl+c on the command line and then run the script     
  reset_simulator.py before pausing or stopping the project from running; this is to prevent the Unreal Engine from freezing when attempting to stop the project while a task   is still running

Coordiates:
- In the AirSim APIs, the +z-direction is downward, but in the Unreal Engine editor, the +z-direction is upward
- The coordinate system used in the code 

Takeoff flight times:
- For some of the flight scenarios, it takes awhile for the drones to fly from spawn to the corresponding course and position themselves to start the course
