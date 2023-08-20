# ESDA_onboarding
A repository to host ESDA recruit on-boarding project code. Follow the steps below to run:

Install the following
```
sudo apt install ros-humble-xacro ros-humble-joint-state-publisher-gui ros-humble-gazebo-ros-pkgs
```
Assuming you have cloned this repo into a new workspace and are in the workspace root:
```
colcon build; source install/setup.bash
ros2 launch articubot_one launch_sim.launch.py
```
Open a new tab in your terminal
```
source install/setup.bash
ros2 run waypoint_pub waypoint_pub
```
