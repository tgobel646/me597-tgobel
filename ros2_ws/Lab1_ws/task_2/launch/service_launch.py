import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Log information when launching
        LogInfo(msg="Launching Service and Publisher nodes..."),
        
        # Declare nodes
        Node(
            package='task_2', 
            executable='service', 
        ),
        
        Node(
            package='task_2', 
            executable='talker',  
        ),
    ])
