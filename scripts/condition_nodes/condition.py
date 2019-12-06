#! /usr/bin/env python

"""
A general condition node class with default resetting.
"""

class Condition:

    def __init__(self, name):
        self.name = name

    def tick(self):
        if self.check():
            return "success"
        return "failure"
    
    def check(self):
        return True

    def reset(self):
        pass