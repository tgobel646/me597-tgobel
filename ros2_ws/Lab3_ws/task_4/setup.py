from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'task_4'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
            (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
            (os.path.join('share', package_name, 'maps'), glob(os.path.join('maps', '*maps.[pxy][yma]*')))
            (os.path.join('share', package_name, 'rviz'), glob(os.path.join('rviz', '*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='me597',
    maintainer_email='talon.gobel@gmail.com',
    description='Launches mapping and drive nodes for turtlebot4',
    license='Apache 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gen_sync_map_launch = task_4.gen_sync_map_launch:main',
            'auto_navigator = task_4.auto_navigator:main'
        ],
    },
)
