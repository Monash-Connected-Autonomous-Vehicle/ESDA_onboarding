import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from geographic_msgs.msg import WayPoint


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.subscription = self.create_subscription(Waypoint, '/global_waypoint', self.lets_go, 10)
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

    def lets_go(self):
        msg = Twist()
        msg.linear.x = 24.0
        msg.angular.z = 0.0
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)


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