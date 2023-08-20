import rclpy
from rclpy.node import Node

from custom_interfaces.msg import Waypoint


class WaypointPublisher(Node):

    def __init__(self):
        super().__init__('waypoint_publisher')
        self.publisher_ = self.create_publisher(Waypoint, 'global_waypoint', 1)
        
        HALF_SECOND = 0.5
        self.timer = self.create_timer(HALF_SECOND, self.waypoint_callback)

    def waypoint_callback(self):
        wp = Waypoint()
        wp.x, wp.y, wp.z, wp.radius = 25, 37, 0, 1
                
        self.publisher_.publish(wp)
        self.get_logger().info('Publishing: [x, y, radius]=["%i""%i""%i"]' % msg.x, msg.y, msg.radius)



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
