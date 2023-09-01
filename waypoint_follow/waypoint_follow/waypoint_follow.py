import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from custom_interfaces.msg import Waypoint
from nav_msgs.msg import OccupancyGrid


class WaypointFollow(Node):
    """
    Class for following a waypoint. Works for with basic worlds.
    Uses a temporary waypoint if the robot is blocked infront.
    """
    DEFAULT_Z_ANGLE_VEL = 0.5
    DEFAULT_X_LINEAR_VEL = 1.0
    ZERO_VEL = 0.0
    MANEUVER_ANGLE = math.pi/3

    def __init__(self):
        super().__init__('waypoint_follow')
        self.odom_sub = self.create_subscription(Odometry, 'odom', self.follow_waypoint_callback, 1)
        self.waypoint_sub = self.create_subscription(Waypoint, 'global_waypoint', self.set_waypoint_callback, 1)
        self.grid_sub = self.create_subscription(OccupancyGrid, 'grid', self.set_grid_callback, 1)
        self.cmd_vel_pub_ = self.create_publisher(Twist, 'cmd_vel', 1)

        self.waypoint = None
        self.grid = None
        self.temp_waypoint = None
        self.angle_z = None
        self.pos = None
        self.is_maneuvering = False
        
        
    def follow_waypoint_callback(self, odom_msg):
        """Follows the waypoint until it is reached."""
        if self.waypoint is None:
            return
        
        # Update current position and angle
        self.pos = odom_msg.pose.pose.position
        self.angle_z = self.euler_from_quaternion(odom_msg.pose.pose.orientation)

        if self.is_blocked_infront():
            new_temp_waypoint = self.calculate_temp_waypoint()
            if new_temp_waypoint != self.temp_waypoint:
                print("object in front, maneuvering")
                self.temp_waypoint = new_temp_waypoint
                print(f"New temp waypoint: {self.temp_waypoint}")
                self.is_maneuvering = True

        current_wp = self.temp_waypoint if self.is_maneuvering else self.waypoint

        distance = self.calculate_distance(current_wp.x, current_wp.y, self.pos.x, self.pos.y)
        theta = math.atan2(current_wp.y - self.pos.y, current_wp.x - self.pos.x)

        msg = Twist()
        
        if distance < current_wp.radius: # Waypoint reached
            msg.angular.z = self.ZERO_VEL
            msg.linear.x = self.ZERO_VEL

            if self.is_maneuvering:
                self.is_maneuvering = False
                print(f"Reached temp waypoint: {current_wp}")
            else:
                print(f"Reached waypoint: {current_wp}")
                self.destroy_subscription(self.odom_sub)
                self.destroy_subscription(self.grid_sub)

        # Turning in place
        elif abs(self.angle_z - theta) > 0.1:
            msg.linear.x = self.ZERO_VEL

            if self.angle_z > theta:
                msg.angular.z = -1 * self.DEFAULT_Z_ANGLE_VEL
            else:
                msg.angular.z = self.DEFAULT_Z_ANGLE_VEL

        # Moving forward
        else:
            msg.angular.z = self.ZERO_VEL
            msg.linear.x = self.DEFAULT_X_LINEAR_VEL

        self.cmd_vel_pub_.publish(msg)


    def set_waypoint_callback(self, msg):
        """Sets the waypoint to follow."""
        if self.waypoint is None and msg is not None:
            self.waypoint = msg
            print(f"Received waypoint: {self.waypoint}") 
            self.destroy_subscription(self.waypoint_sub)


    def set_grid_callback(self, msg):
        """Sets the occupancy grid."""
        self.grid = msg.data
 

    def euler_from_quaternion(self, orientation):
        """Source: https://automaticaddison.com/how-to-convert-a-quaternion-into-euler-angles-in-python/"""
        t3 = +2.0 * (orientation.w * orientation.z + orientation.x * orientation.y)
        t4 = +1.0 - 2.0 * (orientation.y * orientation.y + orientation.z * orientation.z)
        return  math.atan2(t3, t4) # in radians
    

    def is_blocked_infront(self):
        """Check if the robot is blocked infront of it."""
        # Check cells infront of robot
        if self.grid is None:
            return True
        else:
            # Hard coding for now :( Not entirely sure how to read occupancy grid data
            return (100 in self.grid[4554:4558] or 
                    100 in self.grid[4654:4658] or
                    100 in self.grid[4754:4758] or
                    100 in self.grid[4854:4858] or
                    100 in self.grid[4954:4958] or
                    100 in self.grid[5054:5058] or
                    100 in self.grid[5154:5158])
        

    def calculate_temp_waypoint(self):
        """Computes a new temp way point approximately 2 blocks to the right of the current position.
        New waypoint is 60 degrees from the current angle."""
        temp_waypoint = Waypoint()
        x_right = int(self.pos.x + 2 * math.cos(self.angle_z - self.MANEUVER_ANGLE))
        y_right = int(self.pos.y + 2 * math.sin(self.angle_z - self.MANEUVER_ANGLE))

        temp_waypoint.x = x_right
        temp_waypoint.y = y_right
        temp_waypoint.z = 0
        temp_waypoint.radius = 1
        return temp_waypoint
    
    
    def calculate_distance(self, x1, y1, x2, y2):
        """Calculates the distance between two points."""
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def main(args=None):
    rclpy.init(args=args)
    node = WaypointFollow()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
