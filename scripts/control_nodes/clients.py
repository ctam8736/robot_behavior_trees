#! /usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction
from campus_rover_behavior_tree.msg import BTAction, BTGoal, BTFeedback, BTResult

"""
An auxillary node used to call action nodes indirectly.
"""

class ClientNode():

    def __init__(self, name, param = None):
        self.name = name
        self.client = actionlib.SimpleActionClient(self.name, BTAction)
        self.client.wait_for_server()
        self.status = "idle"
        self.param = param

    def tick(self):
        if self.status is "idle":
            self.status = "running"
            goal = BTGoal()
            if self.param:
                goal.parameter = self.param
            self.client.send_goal(goal)
            return "running"
        elif self.status is "running":
            if self.client.get_result():
                return "success"
            return "running"

    def reset(self):
        self.status = "idle"

"""
An auxillary node used to call the navigation stack indirectly, using a given pose.
"""

class NavigationClientNode():

    def __init__(self, name, pose):
        self.name = name
        self.move_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.move_client.wait_for_server()
        self.status = "idle"
        self.pose = pose

    def tick(self):
        if self.status is "idle":
            self.status = "running"
            goal_pose = MoveBaseGoal()
            goal_pose.target_pose = self.pose
            goal_pose.target_pose.header.frame_id = 'map'
            self.move_client.send_goal(goal_pose)
            return "running"
        elif self.status is "running":
            if self.move_client.get_result():
                return "success"
            return "running"

    def reset(self):
        self.status = "idle"

