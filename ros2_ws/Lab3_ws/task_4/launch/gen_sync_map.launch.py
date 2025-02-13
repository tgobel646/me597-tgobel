import launch
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
import os
import sys
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Paths to the launch files from other packages
    turtlebot4_navigation_share = FindPackageShare("turtlebot4_navigation").find("turtlebot4_navigation")
    turtlebot4_viz_share = FindPackageShare("turtlebot4_viz").find("turtlebot4_viz")
    
    # Return the LaunchDescription
    return LaunchDescription([
        # Include the slam.launch.py from turtlebot4_navigation
        IncludeLaunchDescription(
            os.path.join(turtlebot4_navigation_share, 'launch', 'slam.launch.py'),
            launch_arguments={}.items()
        ),
        
        # Include the view_robot.launch.py from turtlebot4_viz
        IncludeLaunchDescription(
            os.path.join(turtlebot4_viz_share, 'launch', 'view_robot.launch.py'),
            launch_arguments={}.items()
        ),
    ])
