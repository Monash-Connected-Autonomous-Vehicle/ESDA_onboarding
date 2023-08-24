import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid


class LaserToGrid(Node):
    def __init__(self):
        super().__init__('laser_to_grid')
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.map_to_grid,
            1)
        self.subscription  # prevent unused variable warning
        
      	self.publisher_ = self.create_publisher(OccupancyGrid, 'grid', 1)

    def map_to_grid(self, scan_msg):
        # get scan
        
        # convert points to x, y relative to centre
        
        # translate points so that the bottom left most is the origin
        
        # create an occupancy grid with 
        # 	width, height equal to domain, range of points
        #   resolution equal to something small but fixed
        
        # map point coordinates to the occupancy grid where
        #   bottom ros is inserted first, then next row up, then next...
        
        


def main(args=None):
    rclpy.init(args=args)
    node = LaserToGrid()
    rclpy.spin(node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
