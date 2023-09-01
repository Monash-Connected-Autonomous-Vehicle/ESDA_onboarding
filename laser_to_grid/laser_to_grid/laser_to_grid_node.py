import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid


class LaserToGrid(Node):
    def __init__(self):
        super().__init__('laser_to_grid')
        self.scan_sub = self.create_subscription(LaserScan, 'scan', self.map_to_grid, 1)
        self.scan_sub  # prevent unused variable warning
        self.grid_pub_ = self.create_publisher(OccupancyGrid, 'grid', 1)
        self.GRID_WIDTH = 100 # grid is 100 cells wide
        self.GRID_RES = 0.1 # 10 cm/cell

    def map_to_grid(self, scan_msg):
        # laser points are a series of lengths from origin to point
        # each point is inc radians apart from each other
        laser_points = scan_msg.ranges
        inc = scan_msg.angle_increment
        xy_points = []
        
        # get scan points and convert points from polar coords to to cartesian relative to centre
        # grid resolution will be 10cm so also round points to nearest 10cm and scale up from m to dm
        for p in range(len(laser_points)):
            if laser_points[p] != float('inf'):
                r = 10 * laser_points[p] # scale up from metres to decimetres
                ang = p*inc
                x = int(r * math.cos(ang)) # round x & y
                y = int(r * math.sin(ang))
                xy_points.append([x, y])
                
        # create an occupancy grid with 0 occupancy in all cells by default
        grid = OccupancyGrid()
        grid.header = scan_msg.header
        grid.info.resolution = self.GRID_RES
        grid.info.width = self.GRID_WIDTH
        grid.info.height = self.GRID_WIDTH
        # translate the grid by half it's width & height so it's centre is the robot
        # otherwise the top left corner of the grid i.e. cell (0, 0) is where the robot is
        grid.info.origin.position.x = -self.GRID_RES * self.GRID_WIDTH/2 
        grid.info.origin.position.y = -self.GRID_RES * self.GRID_WIDTH/2
        grid.data = [0] * self.GRID_WIDTH * self.GRID_WIDTH

        # map point coordinates to the occupancy grid data array
        # this is a 1D array where every GRID_WIDTH index is a new row
        for p in xy_points:
            # idk y we flip in x & y
            # idk y we translate by half of resolution
            x = -p[1] + int(self.GRID_WIDTH/2)
            y = -p[0] + int(self.GRID_WIDTH/2)    
            idx = self.GRID_WIDTH*x + y
            if idx < len(grid.data):
                grid.data[idx] = 100 
        
        self.grid_pub_.publish(grid)


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
