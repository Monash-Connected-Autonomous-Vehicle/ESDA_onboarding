import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from custom_interfaces.msg import Waypoint


class WaypointFollow(Node):
    def __init__(self):
        super().__init__('waypoint_follow')
        # subscribe to odom topic
        self.odom_sub = self.create_subscription(Odometry, 'odom', self.follow_waypoint_callback, 1)
        # subscribe to waypoint topic
        self.waypoint_sub = self.create_subscription(Waypoint, 'global_waypoint', self.set_waypoint_callback, 1)
        self.waypoint = None
        self.cmd_vel_pub_ = self.create_publisher(Twist, 'cmd_vel', 1)
        self.count = 0
        self.drive = True
        self.distance = None
        self.theta = None
        self.orientation_z = None
        
        
    def follow_waypoint_callback(self, odom_msg=None):
        if odom_msg is not None and self.waypoint is not None:
            orientation = odom_msg.pose.pose.orientation
            position = odom_msg.pose.pose.position
            (x, y, z) = self.euler_from_quaternion(orientation.x, orientation.y, orientation.z, orientation.w)
            self.orientation_z = z
            # calculate z-angle between current position and waypoint position
            self.theta = math.atan2(self.waypoint.y - position.y, self.waypoint.x - position.x)
            self.distance = math.sqrt((self.waypoint.x - position.x)**2 + (self.waypoint.y - position.y)**2)


        if self.distance is not None and self.theta is not None and self.orientation_z is not None:
            msg = Twist()

            if self.distance < self.waypoint.radius:
                msg.angular.z = 0.0
                msg.linear.x = 0.0
                self.get_logger().info('Reached waypoint: "%s"' % self.waypoint)
                self.destroy_subscription(self.odom_sub)

            elif abs(self.orientation_z - self.theta) > 0.1:
                
                msg.linear.x = 0.0

                if self.orientation_z > self.theta:
                    msg.angular.z = -0.5
                else:
                    msg.angular.z = 0.5
            else:
                msg.angular.z = 0.0
                msg.linear.x = 1.0


            self.cmd_vel_pub_.publish(msg)


    def set_waypoint_callback(self, msg):
        if self.waypoint is None and msg is not None:
            self.waypoint = msg
            self.get_logger().info('Received waypoint: "%s"' % self.waypoint)
            # unsubscribe from waypoint topic since we only need to receive it once
            self.destroy_subscription(self.waypoint_sub)


 
    def euler_from_quaternion(self, x, y, z, w):
            """
            Source: https://automaticaddison.com/how-to-convert-a-quaternion-into-euler-angles-in-python/
            Convert a quaternion into euler angles (roll, pitch, yaw)
            roll is rotation around x in radians (counterclockwise)
            pitch is rotation around y in radians (counterclockwise)
            yaw is rotation around z in radians (counterclockwise)
            """
            t0 = +2.0 * (w * x + y * z)
            t1 = +1.0 - 2.0 * (x * x + y * y)
            roll_x = math.atan2(t0, t1)
        
            t2 = +2.0 * (w * y - z * x)
            t2 = +1.0 if t2 > +1.0 else t2
            t2 = -1.0 if t2 < -1.0 else t2
            pitch_y = math.asin(t2)
        
            t3 = +2.0 * (w * z + x * y)
            t4 = +1.0 - 2.0 * (y * y + z * z)
            yaw_z = math.atan2(t3, t4)
        
            return roll_x, pitch_y, yaw_z # in radians



        
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
