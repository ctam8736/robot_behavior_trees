#! /usr/bin/env python

"Some basic movement action servers."

import rospy
from action import Action

from geometry_msgs.msg import Twist

class MoveForwardServer(Action):

  def __init__(self, name):
    Action.__init__(self, name)
    self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

  def do_action(self):
    rate = rospy.Rate(.5)
    move_twist = Twist()
    move_twist.linear.x = .2
    self.cmd_vel_pub.publish(move_twist)
    rate.sleep()
    self.cmd_vel_pub.publish(Twist())

class MoveBackwardServer(Action):

  def __init__(self, name):
    Action.__init__(self, name)
    self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

  def do_action(self):
    rate = rospy.Rate(.5)
    move_twist = Twist()
    move_twist.linear.x = -.2
    self.cmd_vel_pub.publish(move_twist)
    rate.sleep()
    self.cmd_vel_pub.publish(Twist())

class TurnRightServer(Action):

  def __init__(self, name):
    Action.__init__(self, name)
    self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

  def do_action(self):
    rate = rospy.Rate(.5)
    move_twist = Twist()
    move_twist.angualar.x = -.5
    self.cmd_vel_pub.publish(move_twist)
    rate.sleep()
    self.cmd_vel_pub.publish(Twist())

class TurnLeftServer(Action):

  def __init__(self, name):
    Action.__init__(self, name)
    self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

  def do_action(self):
    rate = rospy.Rate(.5)
    move_twist = Twist()
    move_twist.angualar.x = .5
    self.cmd_vel_pub.publish(move_twist)
    rate.sleep()
    self.cmd_vel_pub.publish(Twist())