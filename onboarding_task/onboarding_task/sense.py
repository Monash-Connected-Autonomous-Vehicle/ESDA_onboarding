import math
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
            self.map_to_grid,
            10)
        self.publisher = self.create_publisher(OccupancyGrid, 'grid_out', 10)
        self.GRID_DIMENSION = 100 # 100 x 100 grid size
        self.GRID_RES = 0.1 # 10 cm/cell

    def map_to_grid(self, msg):
        laser_points = msg.ranges
        scan_distances = msg.angle_increment 
        xy_points = self.polar_to_cartesian(laser_points, scan_distances)

        grid = OccupancyGrid()
        grid.header = msg.header
        grid.info.width = self.GRID_DIMENSION
        grid.info.height = self.GRID_DIMENSION
        grid.info.resolution = self.GRID_RES
        # translate the grid by half it's width & height so it's centre is the robot
        # otherwise the top left corner of the grid i.e. cell (0, 0) is where the robot is
        grid.info.origin.position.x = -self.GRID_RES * self.GRID_DIMENSION/2 
        grid.info.origin.position.y = -self.GRID_RES * self.GRID_DIMENSION/2
        grid.data = [0] * self.GRID_DIMENSION * self.GRID_DIMENSION

        # map point coordinates to the occupancy grid data array
        # this is a 1D array where every GRID_DIMENSION index is a new row
        for p in xy_points:
            # idk y we flip in x & y
            # idk y we translate by half of resolution
            x = -p[1] + int(self.GRID_DIMENSION/2)
            y = -p[0] + int(self.GRID_DIMENSION/2)    
            idx = self.GRID_DIMENSION*x + y
            grid.data[idx] = 100 

        # why is it jsut 0 and 100 s 
        # what do they mean
        self.get_logger().info('I heard: "%s"' % grid.data) 

        self.publisher.publish(grid)

    def polar_to_cartesian(self, laser_points: list[float], scan_distances: float) -> list[tuple[int, int]]: 
        """
        # convert laser points form polar coordinates to cartesian coordinates
        :param laser_points: 
        :param scan_distances: 
        returns: a list of integers representing the cartesian coordinates ? 
        """
        xy_points = []

        for p in range(len(laser_points)): 
            if laser_points[p] != float('inf'): 
                r = 10 * laser_points[p]
                ang = p * scan_distances
                x = int(r * math.cos(ang))
                y = int(r * math.sin(ang))
                xy_points.append([x, y])

        return xy_points



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