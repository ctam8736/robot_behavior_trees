#! /usr/bin/env python


import rospy
import actionlib
import math
from campus_rover_behavior_tree.msg import BTAction, BTGoal, BTFeedback, BTResult

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion



class TRActionServer(object):
  # create messages that are used to publish feedback/result
  _feedback = BTFeedback()
  _result   = BTResult()

  def __init__(self, name):
    self.name = name
    self._as = actionlib.SimpleActionServer(self.name, BTAction, execute_cb=self.execute_cb, auto_start = False)
    self._as.start()
    self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    
  def execute_cb(self, goal):
    success = True
    
    self.initiate_spin()
      
    if success:
      self.set_status('SUCCESS')

  def set_status(self,status):
      if status == 'SUCCESS':
        self._feedback.status = 1
        self._result.status = self._feedback.status
        #rospy.loginfo('Action %s: Succeeded' % self.name)
        self._as.set_succeeded(self._result)
      elif status == 'FAILURE':
        self._feedback.status = 2
        self._result.status = self._feedback.status
        #rospy.loginfo('Action %s: Failed' % self.name)
        self._as.set_succeeded(self._result)
      else:
        #rospy.logerr('Action %s: has a wrong return status' % self.name)
        pass

  def initiate_spin(self):

    turn_twist = Twist()
    turn_twist.angular.z = -.2
    self.cmd_vel_pub.publish(turn_twist)

    """
    #wait for odom info
    while not self.current_yaw:
      pass

    #set target between -pi and pi
    target = self.current_yaw - self.radian_goal
    while target > math.pi:
        target -= 2 * math.pi
    while target < -math.pi:
        target += 2 * math.pi

    #init publisher
    cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

    #keep spinning while within threshold
    while(abs((target - self.current_yaw) * (180/math.pi)) > .5):
      turn_twist = Twist()
      turn_twist.angular.z = -.2
      cmd_vel_pub.publish(turn_twist)

    #stop robot
    cmd_vel_pub.publish(Twist())
    """

if __name__ == '__main__':
  rospy.init_node('twist_right')
  server = BTActionServer('twist_right')
  rospy.spin()