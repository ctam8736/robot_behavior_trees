#! /usr/bin/env python

"""
A control node that ticks children in parallel/synchronously.
"""

import rospy

class ParallelNode():

    def __init__(self, name, ns, nf):
        self.children = []
        self.ns = ns
        self.nf = nf

    def tick(self):
        s = 0
        f = 0
        for i, node in enumerate(self.children):
            child_status = node.tick()
            if child_status == "success":
                s = s + 1
            elif child_status == "failure":
                f = f + 1
        if s >= self.ns:
            return "success"
        if f >= self.nf:
            return "failure"
        return "running"

    def reset(self):
        for node in self.children:
            node.reset()

    def add_child(self, node):
        self.children.append(node)
            