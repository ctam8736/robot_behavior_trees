#! /usr/bin/env python
import rospy

"""
TODO: node that keeps calling child after success or failure is returned
"""

class RepeaterNode():

    def __init__(self, name):
        self.child = None
        self.name = name

    def tick(self):
        if self.child:
            status = self.child.tick()
            if status == "success":
                self.reset()
                self.child.tick()
            return status

    def reset(self):
        if self.child:
            self.child.reset()

    def add_child(self, node):
        self.child = node