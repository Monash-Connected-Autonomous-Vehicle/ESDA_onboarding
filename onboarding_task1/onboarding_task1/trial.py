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
        scan = LaserScan()
        ranges = msg.ranges
        intensities = msg.intensities

        angles = np.linspace(msg.angle_min, msg.angle_max, len(ranges))
        cartesian_points = [(r * np.cos(theta), r * np.sin(theta)) for r, theta in zip(ranges, angles)]
        resolution = 0.1  # Adjust as needed
        grid_width = int(100 / resolution)  # Compute based on your environment
        grid_height = int(100 / resolution)  # Compute based on your environment
        grid = np.zeros((grid_height, grid_width), dtype=np.int8)

        for point in cartesian_points:
            print(point)
            if point!= float('inf'):
                x_cell = int((point[0] - 0) / resolution)
                y_cell = int((point[1] - 0) / resolution)

                if 0 <= x_cell < grid_width and 0 <= y_cell < grid_height:
                    grid[y_cell, x_cell] = 100  # Occupied cell


        self.get_logger().info('I heard: "%s"' % scan)

        # defiine type of msg
        msg = OccupancyGrid()

        # Populate msg fields with meaningful data
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.info.resolution = 0.1  # Example resolution
        msg.info.width = 100  # Example width
        msg.info.height = 100  # Example height
        msg.data = np.random.randint(0, 100, size=(msg.info.width * msg.info.height)).tolist()

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