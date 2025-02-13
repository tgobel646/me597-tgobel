import launch
from launch_ros.actions import Node

def generate_launch_description():
    return launch.LaunchDescription([
        Node(
            package='task_3',
            executable='pid_speed_controller',
            name='pid_speed_controller'),
  ])