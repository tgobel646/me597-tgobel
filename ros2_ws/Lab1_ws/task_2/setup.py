from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'task_2'

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
    maintainer='me597',
    maintainer_email='talon.gobel@gmail.com',
    description='pub/sub combo for interface',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = task_2.joint_topic_publisher:main',
            'listener = task_2.joint_topic_subscriber:main',
            'service = task_2.service_function:main',
            'client = task_2.client_function:main',
        ],
    },
)
