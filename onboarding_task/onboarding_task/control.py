import rclpy
from rclpy.node import Node
import math
from geometry_msgs.msg import Twist
from custom_interfaces.msg import Waypoint
from nav_msgs.msg import Odometry

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.subscription = self.create_subscription(Waypoint, '/global_waypoint', self.waypoint_callback, 10)
        self.subscription2 = self.create_subscription(Odometry, '/odom', self.lets_go, 10)
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.pos_x = 0.0 
        self.pos_y = 0.0
        self.pos_radius = 0.0

    def lets_go(self, odom_msg):
        # destination = x, y, z, radius
        #Note that the destination is 2D, where z = 0
        cur_pos_x = odom_msg.pose.pose.position.x
        cur_pos_y = odom_msg.pose.pose.position.y

        twist_msg = Twist()

        # when we are at the target waypoint
        distance_wp = math.sqrt(cur_pos_x**2 + cur_pos_y**2)
        distance_car = math.sqrt(self.pos_x**2 + self.pos_y)

        if abs(distance_car - distance_wp) <= self.pos_radius:
            twist_msg.linear.x = 0.0
        else:
            # this is the angle between the current cord and target cord
            target_angle = round(math.atan2(self.pos_y - cur_pos_y, self.pos_x - cur_pos_x), 2)
            # this is the angle of the car currently is facing
            car_angle = round(self.quaternion_to_angle(odom_msg.pose.pose.orientation), 2)
            if (target_angle - car_angle) <= 0.1: 
                print("runing...")
                twist_msg.linear.x = 1.0
            else: 
                print("turning...")
                twist_msg.angular.z = target_angle - car_angle

        # print(odom_msg.pose.pose.position)
        # print(odom_msg.pose.pose.orientation)
        print(twist_msg.angular.z)
        print(target_angle)
        print(car_angle)
        print(cur_pos_x, cur_pos_y)
        # print(twist_msg)
        self.publisher_.publish(twist_msg)

    def waypoint_callback(self, waypoint_msg): 
        self.pos_x = waypoint_msg.x 
        self.pos_y = waypoint_msg.y
        self.pos_radius = waypoint_msg.radius

    
    def quaternion_to_angle(self, quat):
        # Extract the z-axis rotation component from the quaternion
        # z_rotation = 2 * math.atan2(quat.z, quat.w)
        z_rotation = math.atan2(2*((quat.w*quat.z) + (quat.x*quat.y)), 1 - 2*(quat.y**2 + quat.x**2))
        # Convert the rotation to the range [0, 2π)
        # if z_rotation < 0:
        #     z_rotation += 2 * math.pi
        return abs(z_rotation)
    


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()