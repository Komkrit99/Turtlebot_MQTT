#!/usr/bin/env python
import rospy
import cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from numpy as np

def convert_depth_image(self, ros_image):
     bridge = CvBridge()
     # Use cv_bridge() to convert the ROS image to OpenCV format
      try:
     #Convert the depth image using the default passthrough encoding
                depth_image = cv_bridge.imgmsg_to_cv2(ros_image, deside_encoding="passthrough")

      except CvBridgeError, e:
 	          print e
     #Convert the depth image to a Numpy array
      depth_array = np.array(depth_image, dtype=np.float32)

      rospy.loginfo(depth_array)

def pixel2depth():
	rospy.init_node('pixel2depth',anonymous=True)
	rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image,callback=convert_depth_image, queue_size=1)
	rospy.spin()

if __name__ == '__main__':
	pixel2depth()