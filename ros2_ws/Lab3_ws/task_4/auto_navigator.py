#!/usr/bin/env python3

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image, ImageOps

import yaml
import pandas as pd

import time

import rclpy
from copy import copy, deepcopy
from rclpy.node import Node
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped, Pose, Twist
from std_msgs.msg import Float32
from queue import Queue

class Map():
    def __init__(self, map_name):
        self.map_im, self.map_df, self.limits = self.__open_map(map_name)
        self.image_array = self.__get_obstacle_map(self.map_im, self.map_df)

    def __repr__(self):
        fig, ax = plt.subplots(dpi=150)
        ax.imshow(self.image_array,extent=self.limits, cmap=cm.gray)
        ax.plot()
        return ""

    def __open_map(self,map_name):
        # Open the YAML file which contains the map name and other configuration parameters
        f = open(map_name + '.yaml', 'r')
        map_df = pd.json_normalize(yaml.safe_load(f))
        # Open the map image
        map_name = map_df.image[0]
        im = Image.open(map_name)
        size = 200, 200
        im.thumbnail(size)
        im = ImageOps.grayscale(im)
        # Get the limits of the map. This will help to display the map
        # with the correct axis ticks.
        xmin = map_df.origin[0][0]
        xmax = map_df.origin[0][0] + im.size[0] * map_df.resolution[0]
        ymin = map_df.origin[0][1]
        ymax = map_df.origin[0][1] + im.size[1] * map_df.resolution[0]

        return im, map_df, [xmin,xmax,ymin,ymax]

    def __get_obstacle_map(self,map_im, map_df):
        img_array = np.reshape(list(self.map_im.getdata()),(self.map_im.size[1],self.map_im.size[0]))
        up_thresh = self.map_df.occupied_thresh[0]*255
        low_thresh = self.map_df.free_thresh[0]*255

        for j in range(self.map_im.size[0]):
            for i in range(self.map_im.size[1]):
                if img_array[i,j] > up_thresh:
                    img_array[i,j] = 255
                else:
                    img_array[i,j] = 0
        return img_array
print(Map('classroom_map'))

class Queue():
    def __init__(self, init_queue = []):
        self.queue = copy(init_queue)
        self.start = 0
        self.end = len(self.queue)-1

    def __len__(self):
        numel = len(self.queue)
        return numel

    def __repr__(self):
        q = self.queue
        tmpstr = ""
        for i in range(len(self.queue)):
            flag = False
            if(i == self.start):
                tmpstr += "<"
                flag = True
            if(i == self.end):
                tmpstr += ">"
                flag = True

            if(flag):
                tmpstr += '| ' + str(q[i]) + '|\n'
            else:
                tmpstr += ' | ' + str(q[i]) + '|\n'

        return tmpstr

    def __call__(self):
        return self.queue

    def initialize_queue(self,init_queue = []):
        self.queue = copy(init_queue)

    def sort(self,key=str.lower):
        self.queue = sorted(self.queue,key=key)

    def push(self,data):
        self.queue.append(data)
        self.end += 1

    def pop(self):
        p = self.queue.pop(self.start)
        self.end = len(self.queue)-1
        return p
    
class Node():
    def __init__(self,name):
        self.name = name
        self.children = []
        self.weight = []

    def __repr__(self):
        return self.name

    def add_children(self,node,w=None):
        if w == None:
            w = [1]*len(node)
        self.children.extend(node)
        self.weight.extend(w)
class Tree():
    def __init__(self,name):
        self.name = name
        self.root = 0
        self.end = 0
        self.g = {}
        self.g_visual = Graph('G')

    def __call__(self):
        for name,node in self.g.items():
            if(self.root == name):
                self.g_visual.node(name,name,color='red')
            elif(self.end == name):
                self.g_visual.node(name,name,color='blue')
            else:
                self.g_visual.node(name,name)
            for i in range(len(node.children)):
                c = node.children[i]
                w = node.weight[i]
                #print('%s -> %s'%(name,c.name))
                if w == 0:
                    self.g_visual.edge(name,c.name)
                else:
                    self.g_visual.edge(name,c.name,label=str(w))
        return self.g_visual

    def add_node(self, node, start = False, end = False):
        self.g[node.name] = node
        if(start):
            self.root = node.name
        elif(end):
            self.end = node.name

    def set_as_root(self,node):
        # These are exclusive conditions
        self.root = True
        self.end = False

    def set_as_end(self,node):
        # These are exclusive conditions
        self.root = False
        self.end = True
class AStar():
    def __init__(self,in_tree):
        self.in_tree = in_tree
        self.q = Queue()
        self.dist = {name:np.Inf for name,node in in_tree.g.items()}
        self.h = {name:0 for name,node in in_tree.g.items()}

        for name,node in in_tree.g.items():
            start = tuple(map(int, name.split(',')))
            end = tuple(map(int, self.in_tree.end.split(',')))
            self.h[name] = np.sqrt((end[0]-start[0])**2 + (end[1]-start[1])**2)

        self.via = {name:0 for name,node in in_tree.g.items()}
        for __,node in in_tree.g.items():
            self.q.push(node)

    def __get_f_score(self,node):
        return self.dist[node.name] + self.h[node.name]

    def solve(self, sn, en):
        self.dist[sn.name] = 0
        for name,node in self.in_tree.g.items():
            start = tuple(map(int, name.split(',')))
            end = tuple(map(int, self.in_tree.end.split(',')))
            self.h[name] = np.sqrt((end[0]-start[0])**2 + (end[1]-start[1])**2)
        #self.q.push((self.__get_f_score(sn), sn))
        while len(self.q) > 0:
            self.q.sort(key=self.__get_f_score)
            u = self.q.pop()
            #print(u.name,self.q.queue)
            if u.name == en.name:
                break
            for i in range(len(u.children)):
                c = u.children[i]
                w = u.weight[i]
                new_dist = self.dist[u.name] + w
                if new_dist < self.dist[c.name]:
                    self.dist[c.name] = new_dist
                    self.via[c.name] = u.name
                    #self.q.push((self.__get_f_score(c), c))

    def reconstruct_path(self,sn,en):
        start_key = sn.name
        end_key = en.name
        dist = self.dist[end_key]
        u = end_key
        path = [u]
        while u != start_key:
            u = self.via[u]
            path.append(u)
        path.reverse()
        return path,dist

class Navigation(Node):
    """! Navigation node class.
    This class should serve as a template to implement the path planning and
    path follower components to move the turtlebot from position A to B.
    """

    def __init__(self, node_name='Navigation'):
        """! Class constructor.
        @param  None.
        @return An instance of the Navigation class.
        """
        super().__init__(node_name)
        # Path planner/follower related variables
        self.path = Path()
        self.goal_pose = PoseStamped()
        self.ttbot_pose = PoseStamped()
        self.start_time = 0.0

        # Subscribers
        self.create_subscription(PoseStamped, '/move_base_simple/goal', self.__goal_pose_cbk, 10)
        self.create_subscription(PoseWithCovarianceStamped, '/amcl_pose', self.__ttbot_pose_cbk, 10)

        # Publishers
        self.path_pub = self.create_publisher(Path, 'global_plan', 10)
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.calc_time_pub = self.create_publisher(Float32, 'astar_time',10) #DO NOT MODIFY

        # Node rate
        self.rate = self.create_rate(10)

    def __goal_pose_cbk(self, data):
        """! Callback to catch the goal pose.
        @param  data    PoseStamped object from RVIZ.
        @return None.
        """
        self.goal_pose = data
        self.get_logger().info(
            'goal_pose: {:.4f}, {:.4f}'.format(self.goal_pose.pose.position.x, self.goal_pose.pose.position.y))

    def __ttbot_pose_cbk(self, data):
        """! Callback to catch the position of the vehicle.
        @param  data    PoseWithCovarianceStamped object from amcl.
        @return None.
        """
        self.ttbot_pose = data.pose
        self.get_logger().info(
            'ttbot_pose: {:.4f}, {:.4f}'.format(self.ttbot_pose.pose.position.x, self.ttbot_pose.pose.position.y))

    def a_star_path_planner(self, start_pose, end_pose):
        """! A Start path planner.
        @param  start_pose    PoseStamped object containing the start of the path to be created.
        @param  end_pose      PoseStamped object containing the end of the path to be created.
        @return path          Path object containing the sequence of waypoints of the created path.
        """
        path = Path()
        self.get_logger().info(
            'A* planner.\n> start: {},\n> end: {}'.format(start_pose.pose.position, end_pose.pose.position))
        self.start_time = self.get_clock().now().nanoseconds*1e-9 #Do not edit this line (required for autograder)
        # TODO: IMPLEMENTATION OF THE A* ALGORITHM
        path.poses.append(start_pose)
        path.poses.append(end_pose)

        # Do not edit below (required for autograder)
        self.calc_time_pub.publish(self.get_clock().now().nanoseconds*1e-9-self.start_time)
        
        return path
        print(f"Path is: {path}")

    def get_path_idx(self, path, vehicle_pose):
        """! Path follower.
        @param  path                  Path object containing the sequence of waypoints of the created path.
        @param  current_goal_pose     PoseStamped object containing the current vehicle position.
        @return idx                   Position in the path pointing to the next goal pose to follow.
        """

        idx = 0
        vehicle_x = vehicle_pose.pose.position.x
        vehicle_y = vehicle_pose.pose.position.y

        # TODO: IMPLEMENT A MECHANISM TO DECIDE WHICH POINT IN THE PATH TO FOLLOW idx <= len(path)
        min_dist = 5

        while idx <= len(path):

            point_x = path[idx][0]
            point_y = path[idx][1]
            dist = np.sqrt((vehicle_x - point_x) ** 2 + (vehicle_y - point_y) ** 2)
            
            if dist < min_dist:
                idx += 1
            else:
                return idx

    def path_follower(self, vehicle_pose, current_goal_pose):
        """! Path follower.
        @param  vehicle_pose           PoseStamped object containing the current vehicle pose.
        @param  current_goal_pose      PoseStamped object containing the current target from the created path. This is different from the global target.
        @return path                   Path object containing the sequence of waypoints of the created path.
        """
        speed = 0.0
        heading = 0.0
        # TODO: IMPLEMENT PATH FOLLOWER
        # Extract vehicle position and orientation from vehicle_pose
        vehicle_x = vehicle_pose.position.x
        vehicle_y = vehicle_pose.position.y
        vehicle_theta = vehicle_pose.orientation.z # Assuming 2D and theta represents yaw angle

        # Extract goal position from current_goal_pose
        goal_x = current_goal_pose[0][0]
        goal_y = current_goal_pose[0][1]

        # Calculate the distance to the goal
        distance_to_goal = np.sqrt((goal_x - vehicle_x) ** 2 + (goal_y - vehicle_y) ** 2)

        # Calculate the desired heading (angle to goal)
        desired_heading = np.atan2(goal_y - vehicle_y, goal_x - vehicle_x)

        # Calculate the heading error
        heading_error = desired_heading - vehicle_theta

        # Normalize the heading error to the range [-pi, pi]
        heading_error = (heading_error + np.pi) % (2 * np.pi) - np.pi

        # Proportional controller gains (can be tuned)
        k_speed = 1.0  # Proportional gain for speed
        k_heading = 1.5  # Proportional gain for heading

        # Calculate speed (reduce speed as the vehicle gets closer to the goal)
        speed = k_speed * distance_to_goal

        # Calculate the desired change in heading
        heading = k_heading * heading_error

        # Clip the speed and heading to avoid unrealistic values
        max_speed = 1.0  # Maximum speed (m/s)
        max_steering_angle = np.radians(45)  # Max steering angle (in radians)

        speed = max(0.0, min(speed, max_speed))
        heading = max(-max_steering_angle, min(heading, max_steering_angle))

        return speed, heading

    def move_ttbot(self, speed, heading):
        """! Function to move turtlebot passing directly a heading angle and the speed.
        @param  speed     Desired speed.
        @param  heading   Desired yaw angle.
        @return path      object containing the sequence of waypoints of the created path.
        """
        cmd_vel = Twist()
        # TODO: IMPLEMENT YOUR LOW-LEVEL CONTROLLER
        cmd_vel.linear.x = speed
        cmd_vel.angular.z = heading

        self.cmd_vel_pub.publish(cmd_vel)

    def run(self):
        """! Main loop of the node. You need to wait until a new pose is published, create a path and then
        drive the vehicle towards the final pose.
        @param none
        @return none
        """
        while rclpy.ok():
            # Call the spin_once to handle callbacks
            rclpy.spin_once(self, timeout_sec=0.1)  # Process callbacks without blocking

            # 1. Create the path to follow
            path = self.a_star_path_planner(self.ttbot_pose, self.goal_pose)
            # 2. Loop through the path and move the robot
            idx = self.get_path_idx(path, self.ttbot_pose)
            current_goal = path.poses[idx]
            speed, heading = self.path_follower(self.ttbot_pose, current_goal)
            self.move_ttbot(speed, heading)

            self.rate.sleep()
            # Sleep for the rate to control loop timing


def main(args=None):
    rclpy.init(args=args)
    nav = Navigation(node_name='Navigation')

    try:
        nav.run()
    except KeyboardInterrupt:
        pass
    finally:
        nav.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()