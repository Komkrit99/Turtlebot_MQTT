import rospy
from geometry_msgs.msg import Twist
rospy.init_node('turtlebot3_teleop')
pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

turtlebot3_model = rospy.get_param("model", "burger")

def move(x,r):
    while(True):
        twist = Twist()
        twist.linear.x = x; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = r
        pub.publish(twist)