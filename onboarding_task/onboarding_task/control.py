import rclpy
from rclpy.node import Node
import math
from geometry_msgs.msg import Twist
from custom_interfaces.msg import Waypoint
from nav_msgs.msg import Odometry

class CommandVehicle(Node):
    """
    - cant differentiate back and front 
    - doesnt work in some places ie far away and fourth quarter
    """

    def __init__(self):
        super().__init__('command_vehicle')
        self.subscription = self.create_subscription(Waypoint, '/global_waypoint', self.waypoint_callback, 10)
        self.subscription2 = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.CAR_VELOCITY = 1.0
        self.waypoint_msg = None

    def odom_callback(self, odom_msg):
        if self.waypoint_msg is None:
            return

        current_x = odom_msg.pose.pose.position.x
        current_y = odom_msg.pose.pose.position.y

        target_angle = math.atan2(self.waypoint_msg.y - current_y, self.waypoint_msg.x - current_x)
        car_angle = self.quaternion_to_angle(odom_msg.pose.pose.orientation)

        twist_msg = Twist()

        distance_wp = math.sqrt((current_x - self.waypoint_msg.x) ** 2 + (current_y - self.waypoint_msg.y) ** 2)

        if distance_wp <= self.waypoint_msg.radius:
            print("Arrived.")
            twist_msg.linear.x = 0.0
        else:
            angle_difference = target_angle - car_angle
            if angle_difference <= 0.1:
                print("Running...")
                twist_msg.angular.z = angle_difference
                twist_msg.linear.x = self.CAR_VELOCITY
            else:
                print("Turning...")
                twist_msg.angular.z = angle_difference

        print("Target angle: {}".format(target_angle))
        print("Car angle: {}".format(car_angle))
        print("Angle moved: {}".format(twist_msg.angular.z))
        print("Current position: ({}, {})".format(current_x, current_y))
        self.publisher_.publish(twist_msg)

    def waypoint_callback(self, waypoint_msg): 
        self.waypoint_msg = waypoint_msg
    
    def quaternion_to_angle(self, quat):
        z_rotation = math.atan2(2 * ((quat.w * quat.z) + (quat.x * quat.y)), 1 - 2 * (quat.y**2 + quat.x**2))
        return abs(z_rotation)

def main(args=None):
    rclpy.init(args=args)

    command_vehicle = CommandVehicle()

    try:
        rclpy.spin(command_vehicle)
    except KeyboardInterrupt:
        pass

    command_vehicle.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
