import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from vision_msgs.msg import BoundingBox2D
import cv2
import numpy as np
from cv_bridge import CvBridge
from std_msgs.msg import Header

class ObjectDetector(Node):

    def __init__(self):
        super().__init__('object_detector')

        # Initialize CvBridge to convert ROS images to OpenCV format
        self.bridge = CvBridge()

        # Create a subscriber to the /video_data topic (sensor_msgs/Image)
        self.subscription = self.create_subscription(
            Image,
            '/video_data',
            self.listener_callback,
            10
        )

        # Create a publisher to publish BoundingBox2D messages
        self.publisher = self.create_publisher(BoundingBox2D, '/bbox', 10)

    def listener_callback(self, msg):
        # Convert ROS Image message to OpenCV image
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # Convert image to grayscale for easier processing
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Threshold the image to create a binary mask
        _, thresholded = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # Find contours in the binary image
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.get_logger().info(f"Contours is: {contours}")

        if contours:
            # Find the largest contour (assumed to be the object of interest)
            largest_contour = max(contours, key=cv2.contourArea)

            # Get the bounding box of the largest contour
            x, y, w, h = cv2.boundingRect(largest_contour)

            # Calculate the centroid of the bounding box
            centroid_x = x + w // 2
            centroid_y = y + h // 2

            # Print the centroid position and bounding box size
            self.get_logger().info(f"Centroid position: ({centroid_x}, {centroid_y})")
            self.get_logger().info(f"Bounding box size: ({w}, {h})")

            # Create a BoundingBox2D message
            bbox_msg = BoundingBox2D()
            bbox_msg.header = Header()
            bbox_msg.header.stamp = self.get_clock().now().to_msg()
            bbox_msg.x = x
            bbox_msg.y = y
            bbox_msg.size_x = w
            bbox_msg.size_y = h

            # Publish the bounding box
            self.publisher.publish(bbox_msg)

            # Draw a rectangle (bounding box) around the detected object
            cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Display the image with the bounding box
            cv2.imshow("Object Detection", cv_image)
            cv2.waitKey(10)

def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetector()
    rclpy.spin(node)

    # Destroy the node after the spin
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
