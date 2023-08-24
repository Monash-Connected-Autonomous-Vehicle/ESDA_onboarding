import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid


class LaserSenser(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.laser_callback,
            10)
        self.publisher = self.create_publisher(OccupancyGrid, 'grid_out', 10)

    def laser_callback(self, msg):
        grid = OccupancyGrid()
        grid.header = msg.header
        
        self.get_logger().info('I heard: "%s"' % grid)

        self.publisher.publish(grid)


def main(args=None):
    rclpy.init(args=args)

    laser_senser = LaserSenser()

    rclpy.spin(laser_senser)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    laser_senser.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()