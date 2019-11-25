#! /usr/bin/env python
import rospy

"""
A node to be designated as the root of a behavior tree, with only one child.
"""

class RootNode():

    def __init__(self, name):
        self.child = None
        self.name = name

    def tick(self):
        if self.child:
            return self.child.tick()

    def reset(self):
        if self.child:
            self.child.reset()

    def add_child(self, node):
        self.child = node