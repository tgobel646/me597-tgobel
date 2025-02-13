# pid_controller.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32
import time
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy

class PIDController(Node):
    def __init__(self):
        super().__init__('pid_speed_controller')

        # Declare parameters for the PID controller
        self.declare_parameter('kp', 0.6)
        self.declare_parameter('ki', 0.0001)
        self.declare_parameter('kd', 0.008)
        self.declare_parameter('target_distance', 0.35)
        self.declare_parameter('integral_min', -1)
        self.declare_parameter('integral_max', 1)

        self.kp = self.get_parameter('kp').get_parameter_value().double_value
        self.ki = self.get_parameter('ki').get_parameter_value().double_value
        self.kd = self.get_parameter('kd').get_parameter_value().double_value
        self.target_distance = self.get_parameter('target_distance').get_parameter_value().double_value
        self.integral_min = self.get_parameter('integral_min').get_parameter_value().double_value
        self.integral_max = self.get_parameter('integral_max').get_parameter_value().double_value
        
        self.get_logger().info(f'PID Controller Initialized with Kp: {self.kp}, Ki: {self.ki}, Kd: {self.kd}')

        # Create PID values
        self.prev_error = 1.0
        self.integral = 0
        self.last_time = self.get_clock().now()

        # Create a subscriber
        self.subscription = self.create_subscription(
            LaserScan,
            '/robot/scan',  # Topic name
            self.scan_callback,  # Callback function
            10  # QoS (quality of service) set to 10Hz
        )
        
        # Create a publisher to output the forward-facing velocity
        self.velocity_publisher = self.create_publisher(Twist, '/robot/cmd_vel', 10)
    
    def scan_callback(self, data: LaserScan):

        self.get_logger().info("scan_callback triggered")

        # Extract the forward-facing distance from the lidar data (ranges)
        forward_distance = data.ranges[270]  # Make sure this is correct for your LIDAR sensor

        # Debug the first few distance values
        self.get_logger().info(f"First 5 range values: {data.ranges[:5]}")

        if forward_distance != float('inf') and forward_distance > 0:
            # Calculate the error between the target distance and the measured distance
            error = forward_distance - self.target_distance

            # Get the current time to calculate delta time for derivative term
            current_time = self.get_clock().now()
            delta_time = (current_time - self.last_time).nanoseconds / 1e9  # Convert to seconds
            self.last_time = current_time

            # Compute the integral term
            self.integral += error * delta_time
            self.integral = max(min(self.integral, self.integral_max), self.integral_min)

            # Compute the derivative term
            derivative = (error - self.prev_error) / delta_time if delta_time > 0 else 0

            # PID output
            pid_output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)

            # Set bounds for linear.x
            linear_velocity = max(min(pid_output, 0.15), -0.015)

            # Control the robot's velocity based on the PID output
            velocity_msg = Twist()
            velocity_msg.linear.x = linear_velocity  # Adjust the linear velocity based on PID output

            # Publish the velocity command
            self.velocity_publisher.publish(velocity_msg)

            # Log the forward distance, PID output, and velocities
            self.get_logger().info(f'Forward-facing distance: {forward_distance:.2f} meters, PID Output: {pid_output:.2f}')
            self.get_logger().info(f'Error: {error:.2f}, Integral: {self.integral:.2f}, Derivative: {derivative:.2f}')
            self.get_logger().info(f"Publishing velocity: {linear_velocity:.3f}")

            # Update the previous error for the next iteration
            self.prev_error = error
        else:
            self.get_logger().warn('Invalid forward-facing distance (NaN or infinity)')

def main(args=None):
    rclpy.init(args=args)

    node = PIDController()
    while rclpy.ok():
        rclpy.spin_once(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
