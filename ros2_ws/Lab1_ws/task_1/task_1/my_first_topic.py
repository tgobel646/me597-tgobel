import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import time


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('time_publisher')
        self.publisher_ = self.create_publisher(Float64, 'my_first_topic', 10)
        self.start_time = time.time() 
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        my_first_topic = time.time() - self.start_time
        self.get_logger().info(f'Elapsed time: {my_first_topic} seconds')
        msg = Float64()
        msg.data = my_first_topic
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()