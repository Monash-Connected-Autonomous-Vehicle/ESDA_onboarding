import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')

        # create publisher which sends mesg to '/simulated_vehicle/cmd_vel' topic
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        # defiine type of msg
        msg = Twist()

        # defines that it moves forward by 5.0
        msg.linear.x = 5.0
        #msg.angular.z = 10.0

        # publishes 'msg' message
        self.publisher_.publish(msg)

        # prints msg in console
        self.get_logger().info('Publishing: "%s"' % msg.linear)
        self.i += 1

def main(args=None):
    # initialise rclpy library
    rclpy.init(args=args)

    # instantiate 
    minimal_publisher = MinimalPublisher()

    # spins the node so callbacks are called
    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()

    rclpy.shutdown()

    
if __name__ == '__main__':
    main()