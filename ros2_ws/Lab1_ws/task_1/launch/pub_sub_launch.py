import launch
from launch_ros.actions import Node

def generate_launch_description():
    return launch.LaunchDescription([
        Node(
            package='task_1',
            executable='talker',
            name='talker'),
        Node(
            package='task_1',
            executable='listener',
            name='listener')
  ])