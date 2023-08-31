import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class WaypointFollow(Node):
    def __init__(self):
        super().__init__('waypoint_follow')
        # subscribe to odom topic
        self.odom_sub = self.create_subscription(Odometry, 'odom', self.follow_waypoint_callback, 1)
        self.cmd_vel_pub_ = self.create_publisher(Twist, 'cmd_vel', 1)
        self.count = 0
        
        
    def follow_waypoint_callback(self, odom_msg=None):
        msg = Twist()
        msg.linear.x = -5.0
        msg.angular.x = 5.0
        self.cmd_vel_pub_.publish(msg)
        print(odom_msg)
        if odom_msg is None:
            return
        
        if self.count % 500 == 0:
            self.count += 1
            return


        
        # self.get_logger().info('Publishing: "%s"' % msg.linear.x)
        # self.get_logger().info('Publishing: "%s"' % msg.angular.z)


def main(args=None):
    rclpy.init(args=args)
    node = WaypointFollow()
    rclpy.spin(node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
