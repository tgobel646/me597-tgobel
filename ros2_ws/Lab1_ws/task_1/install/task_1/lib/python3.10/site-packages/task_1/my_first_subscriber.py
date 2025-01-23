import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Float64,
            'elapsed_time',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        elapsed_time = msg.data
        doubled_time = elapsed_time * 2
        self.get_logger().info(f'Elapsed time: {elapsed_time} seconds, this doubled is {doubled_time} seconds.')


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()