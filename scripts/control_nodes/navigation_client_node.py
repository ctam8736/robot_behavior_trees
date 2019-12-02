#! /usr/bin/env python

"""
An auxillary node used to call the navigation stack indirectly, using a given pose.
"""

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction

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