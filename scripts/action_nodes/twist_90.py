#! /usr/bin/env python


import rospy
import actionlib
import math
from campus_rover_behavior_tree.msg import BTAction, BTGoal, BTFeedback, BTResult

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion



class T90ActionServer(object):
  # create messages that are used to publish feedback/result
  _feedback = BTFeedback()
  _result   = BTResult()

  def __init__(self, name):
    self.name = name
    self._as = actionlib.SimpleActionServer(self.name, BTAction, execute_cb=self.execute_cb, auto_start = False)
    self._as.start()

    self.current_yaw = 0
    self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_cb)
    self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    self.radian_goal = math.pi/2
    
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

  def odom_cb(self, msg):
    #update curr_units or init initial_units
    q = msg.pose.pose.orientation
    q_list = [q.x, q.y, q.z, q.w]
    (roll, pitch, yaw) = euler_from_quaternion(q_list)
    self.current_yaw = yaw

  def initiate_spin(self):

    turn_twist = Twist()

    #wait for odom info
    while not self.current_yaw:
      pass

    #set target between -pi and pi
    target = self.current_yaw - self.radian_goal
    while target > math.pi:
        target -= 2 * math.pi
    while target < -math.pi:
        target += 2 * math.pi

    #keep spinning while within threshold
    while(abs((target - self.current_yaw) * (180/math.pi)) > 1):
      turn_twist = Twist()
      turn_twist.angular.z = -.2
      self.cmd_vel_pub.publish(turn_twist)

    #stop robot
    self.cmd_vel_pub.publish(Twist())

if __name__ == '__main__':
  rospy.init_node('twist_90')
  server = BTActionServer('twist_90')
  rospy.spin()