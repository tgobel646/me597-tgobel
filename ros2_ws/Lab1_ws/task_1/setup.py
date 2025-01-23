from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'task_1'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Talon Gobel',
    maintainer_email='talon.gobel@gmail.com',
    description='Task 1 package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = task_1.my_first_topic:main',
            'listener = task_1.my_first_subscriber:main',
        ],
    },
)
