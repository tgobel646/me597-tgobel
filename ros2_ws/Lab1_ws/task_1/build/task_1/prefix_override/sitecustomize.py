import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/me597/me597-tgobel/ros2_ws/Lab1_ws/task_1/install/task_1'
