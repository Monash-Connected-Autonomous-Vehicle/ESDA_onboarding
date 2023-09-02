import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from custom_interfaces.msg import Waypoint
from nav_msgs.msg import Odometry
import math

class waypoint_direction(Node):

    def __init__(self):
        super().__init__('waypoint_direction')
        
        # create publisher which sends msg to '/cmd_vel' topic
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription2 = self.create_subscription(Waypoint, '/global_waypoint', self.waypoint_callback, 10)
        self.subscription1 = self.create_subscription(Odometry, '/odom', self.position_callback, 10)
        self.final_pos_x = 0.0
        self.final_pos_y = 0.0

    def waypoint_callback(self, msg):
        self.final_pos_x = msg.x
        self.final_pos_y = msg.y
        self.get_logger().info('yeet')

    def position_callback(self, pos):
        self.car_pos_x = pos.pose.pose.position.x
        self.car_pos_y = pos.pose.pose.position.y
        # since rotation is just in the z-axis, then qy = sin(alpha/2)
        self.ori = math.asin(pos.pose.pose.orientation.z) * 2

        # steps: find the angle between current pos and waypoint pos
        self.final_direction = math.atan((self.car_pos_y - self.final_pos_y) / (self.car_pos_x - self.final_pos_x))
        self.moveangle = self.final_direction - self.ori

        msg = Twist()
        if self.car_pos_x <= self.final_pos_x+2.0 and self.car_pos_x >= self.final_pos_x-2.0 and self.car_pos_y <= self.final_pos_y+2.0 and self.car_pos_y >= self.final_pos_y-2.0:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
        elif self.moveangle < 1.0 or self.moveangle >-1.0:
            msg.linear.x = 1.0
            msg.angular.z = 0.0
        elif self.moveangle > 0.0:
            msg.angular.z = 0.5
            msg.linear.x = 0.0
        else:
            msg.angular.z = -0.5
            msg.linear.x = 0.0

        self.publisher_.publish(msg)

        # prints msg in console
        # align the car to the correct direction
        # go forward innit
        self.get_logger().info('Publishing: "%s"' % self.moveangle)
        self.get_logger().info('Publishing: "%s"' % msg.angular)

def main(args=None):
    # initialize rclpy library
    rclpy.init(args=args)

    # instantiate
    waypointdirection = waypoint_direction()

    # spins the node so callbacks are called
    rclpy.spin(waypointdirection)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    waypointdirection.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

