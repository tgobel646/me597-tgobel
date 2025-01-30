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
            executable='joint_topic_publisher.py', 
            name='talker',  # Alias for Publisher node
            output='screen',
        ),
        
        Node(
            package='task_2',  
            executable='service_function.py',  
            name='service',  # Alias for Service node
            output='screen',
        ),
    ])
