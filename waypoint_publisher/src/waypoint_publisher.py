import rclpy
from rclpy.node import Node

from waypoint_publisher.msg import Waypoint


class WaypointPublisher(Node):

    def __init__(self):
        super().__init__('waypoint_publisher')
        self.publisher_ = self.create_publisher(Waypoint, '/goal_waypoint', 10)
        
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.waypoint_callback)

    def waypoint_callback(self):
        """ Publishes a fixed global waypoint consisting of an x, y, z co-ordinate and radius
        
        
        """
        msg = Waypoint()
        print(Waypoint)
        
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
