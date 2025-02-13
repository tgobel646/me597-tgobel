import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('listener')
        self.subscription = self.create_subscription(
            Float64,
            'my_first_topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        my_first_topic = msg.data
        doubled_time = my_first_topic * 2
        self.get_logger().info(f'Elapsed time: {my_first_topic} seconds, this doubled is {doubled_time} seconds.')


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