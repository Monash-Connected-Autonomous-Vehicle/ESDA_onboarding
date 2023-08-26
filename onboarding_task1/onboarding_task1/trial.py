# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from nav_msgs.msg import OccupancyGrid
import numpy as np


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.publisher = self.create_publisher(OccupancyGrid,'/yeet',10)
        

    def listener_callback(self, msg):

        # convert polar coordinates into Cartesian coordinates (x, y) relative to the robot's position
        ranges = msg.ranges

        #return evenly spaced numbers over a specified interval
        angles = np.linspace(msg.angle_min, msg.angle_max, len(ranges))
        for r, theta in zip(ranges, angles)
            if r != float('inf') and theta != float('inf'):
                cartesian_points = [(r * np.cos(theta), r * np.sin(theta))]
        
        # map cartesian points to grid
        resolution = 0.1  
        grid_width = int(100 / resolution) 
        grid_height = int(100 / resolution) 
        grid = np.zeros((grid_height, grid_width), dtype=np.int8)

        for point in cartesian_points:
            if point[0] != float('inf') and point[1] != float('inf'):
                x_cell = int((point[0] - 0) / resolution)
                y_cell = int((point[1] - 0) / resolution)

                if 0 <= x_cell < grid_width and 0 <= y_cell < grid_height:
                    grid[y_cell, x_cell] = 100  # Occupied cell
        

        # defiine type of msg
        msg = OccupancyGrid()

        # Populate msg fields with meaningful data
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.info.resolution = 0.1  # Example resolution
        msg.info.width = 100  # Example width
        msg.info.height = 100  # Example height
        msg.info.origin.position.x = -0.1* 100/2
        msg.info.origin.position.y = -0.1* 100/2
        msg.data = [0]*100*100
        for p in cartesian_points:
            x = -p[1]+int(self.msg.info.width/2)
            y = -p[0] + int(self.msg.info.width/2)
            idx = self.msg.info.width*x+y
            msg.data[idx] =100

        # publishes 'msg' message
        self.publisher_.publish(msg)

        # prints msg in console
        self.get_logger().info('Publishing OccupancyGrid: "%s"' % msg.header)
        self.i += 1


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
