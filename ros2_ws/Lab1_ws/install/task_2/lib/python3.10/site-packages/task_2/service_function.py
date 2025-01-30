from task_2_interfaces.srv import JointState

import rclpy
from rclpy.node import Node


class MinimalService(Node):

    def __init__(self):
        super().__init__('service_function')
        self.srv = self.create_service(JointState, 'joint_service', self.joint_service_callback)

    def joint_service_callback(self, request, response):
        sum_value = request.x + request.y + request.z

        if sum_value >= 0:
            response.valid = True
        else:
            response.valid = False

        self.get_logger().info('Incoming request\na: %d b: %d c: %d Response: %d' 
                               % (request.x, request.y, request.z, response.valid))

        return response


def main():
    rclpy.init()

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()