#! /usr/bin/env python


import rospy
import actionlib
import math
import time

from geometry_msgs.msg import Twist
from campus_rover_behavior_tree.msg import BTAction, BTGoal, BTFeedback, BTResult



class MFActionServer(object):
  # create messages that are used to publish feedback/result
  _feedback = BTFeedback()
  _result   = BTResult()

  def __init__(self, name):
    self.name = name
    self._as = actionlib.SimpleActionServer(self.name, BTAction, execute_cb=self.execute_cb, auto_start = False)
    self._as.start()
    self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    
  def execute_cb(self, goal):
    rate = rospy.Rate(10)
    success = True
    self.move_forward()
      
    if success:
      self.set_status('SUCCESS')

  def set_status(self,status):
      if status == 'SUCCESS':
        self._feedback.status = 1
        self._result.status = self._feedback.status
        self._as.set_succeeded(self._result)
      elif status == 'FAILURE':
        self._feedback.status = 2
        self._result.status = self._feedback.status
        self._as.set_succeeded(self._result)
      else:
        pass

  def move_forward(self):

    rate = rospy.Rate(10)

    move_twist = Twist()
    move_twist.linear.x = .2
    self.cmd_vel_pub.publish(move_twist)

    """
    start_time = time.time()

    #keep moving while within threshold
    while(time.time() - start_time < 2):
      self.cmd_vel_pub.publish(move_twist)
      rate.sleep()
      #print(time.time() - start_time)

    while(time.time() - start_time < 3):
      self.cmd_vel_pub.publish(Twist())
      rate.sleep()

    #print(time.time() - start_time)
    """

if __name__ == '__main__':
  rospy.init_node('move_forward')
  server = BTActionServer(rospy.get_name())
  rospy.spin()
