#! /usr/bin/env python

"""
Sends cmd_vel messages until the robot has turned 90 degrees when called.
"""

import rospy
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion

from action import Action

class ActionServer(Action):

  def __init__(self, name):
    Action.__init__(self, name)
    self.current_yaw = 0
    self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_cb)
    self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    self.radian_goal = math.pi/2

  def do_action(self):
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
    while(abs((target - self.current_yaw) * (180/math.pi)) > 2):
      turn_twist = Twist()
      turn_twist.angular.z = -.3
      self.cmd_vel_pub.publish(turn_twist)

    #stop robot
    self.cmd_vel_pub.publish(Twist())

  def odom_cb(self, msg):
    #update curr_units or init initial_units
    q = msg.pose.pose.orientation
    q_list = [q.x, q.y, q.z, q.w]
    (roll, pitch, yaw) = euler_from_quaternion(q_list)
    self.current_yaw = yaw