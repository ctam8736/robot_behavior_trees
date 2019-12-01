#! /usr/bin/env python

"""
todo: navigates the campus rover to a set destination when called.
"""

import rospy
import actionlib
from action import Action
from std_msgs.msg import UInt8, String, Header, Bool
from geometry_msgs.msg import Twist, Pose, Point, \
    Quaternion, PoseStamped, Transform, Vector3, TransformStamped
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction

class ActionServer(Action):

  def __init__(self, name):
    Action.__init__(self, name)
    self.move_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    self.move_client.wait_for_server()

  def do_action(self):
    goal_pose = MoveBaseGoal()
    goal_pose.target_pose.header.frame_id = 'map'
    goal_pose.target_pose.pose.position.x = 19.0380267163
    goal_pose.target_pose.pose.position.y = 20.7569543047
    goal_pose.target_pose.pose.position.z = 0.0
    goal_pose.target_pose.pose.orientation.x = 0.0
    goal_pose.target_pose.pose.orientation.y = 0.0
    goal_pose.target_pose.pose.orientation.z = -0.211043131282
    goal_pose.target_pose.pose.orientation.w = 0.977476749973
    self.move_client.send_goal(goal_pose)
    #self.move_client.wait_for_result()
    #self.move_client.send_goal(goal, feedback_cb=self.nav_cb, done_cb=self.done_cb)
    rospy.loginfo(self.move_client.wait_for_result())
    rospy.loginfo("Goal sent to move base navigator")
    #demand_state_change('navigating')

  """
  def nav_cb(feedback):
    status = FEEDBACK_STATUS[str(move_client.get_state())]
    loc = feedback.base_position.pose.position
    rospy.logdebug("Navigation in state {}, at point ({},{})".format(status,loc.x,loc.y))

  def done_cb(goal_status, done_result):
    global goal
    demand_state_change('waiting') #change_state(States.WAITING)
    nav_status = "Navigation {}".format(FEEDBACK_STATUS[str(goal_status)])
    rospy.loginfo(nav_status)
    if goal_status == 3:
        talker(nav_status, talker_pub)
    elif goal_status == 4:
        talker("Give me a minute, I'm feeling a little tired", talker_pub)
        #NOTE: added functionality that clears costmap and re-sends goal
        costmap_clearer()
        move_client.send_goal(goal, feedback_cb=nav_cb, done_cb=done_cb)
        rospy.loginfo("Goal re-sent to move base navigator")
        demand_state_change('navigating')
  """
