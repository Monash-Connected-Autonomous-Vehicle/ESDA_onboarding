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
        self.subscription1 = self.create_subscription(Odometry,'/odom',self.position_callback,10)
        self.subscription2 = self.create_subscription(Waypoint,'/global_waypoint',self.waypoint_callback,10)
    def waypoint_callback(self,msg):
        self.final_pos = msg
        self.get_logger().info(msg)
    def	position_callback(self,pos):
    	self.car_pos_x = pos.pose.pose.position.x
    	self.car_pos_y = pos.pose.pose.position.y
    	#since rotation is just in the z axis, then qy = sin(alpha/2)
    	self.ori = asin(pos.pose.pose.orientation.y)*2
    	
    	#steps: find angle between current pos and waypoint pos
    	#align the car to the correct direction
    	#go forward innit
    	
    

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
