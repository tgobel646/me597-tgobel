import launch
from launch_ros.actions import Node

def generate_launch_description():
    return launch.LaunchDescription([
        Node(
            package='turtlebot4_navigation',
            executable='slam.launch.py',),
        Node(
            package='turtlebot4_rviz',
            executable='view_robot_launch',)
  ])