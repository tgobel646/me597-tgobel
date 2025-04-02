import numpy as np
import os
import cv2 as cv
import rclpy
import cv2
from sensor_msgs.msg import Image
from rclpy.node import Node
from cv_bridge import CvBridge    # Convert ROS2 <--> cv2 image type

class ImagePublisher(Node):
    def __init__(self, node_name = 'image_publisher'):
        self.bridge = CvBridge()
        super().__init__(node_name)
        self.show_video = True
        # rest of init code:
        self.image_pub = self.create_publisher(Image, '/video_data', 10)

    cap = cv.VideoCapture('home/me597-tgobel/me597-tgobel/ros2_ws/Lab4_ws/task_5/resource/lab3_video.avi')
    frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter('output.avi', fourcc, 20.0, (frame_width, frame_height), True)

    def some_looping_or_callback_function(self, cap, gray):
        ret, frame = cap.read()
 
        # if frame is read correctly ret is True
        while cap.isOpened():
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            if self.show_video:                         # Custom flag to enable or disable video display below
                cv2.imshow('Window Name', gray)        # Display frame image in 'Window name'
                if cv2.waitKey(1) & 0xFF == ord('q'):   # Refresh window and check for keypress of `q` 
                    self.show_video = False             # Set custom flag to False to disable video display 
                    cv2.destroyAllWindows()             # Close all cv2.imshow windows

def main(args=None):
    rclpy.init(args=args)
    img = ImagePublisher()

    try:
        img.run()
    except KeyboardInterrupt:
        pass
    finally:
        img.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()