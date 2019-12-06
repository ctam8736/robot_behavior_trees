#! /usr/bin/env python

from condition import Condition

"""
Sanity check conditions.
"""

class TrueCondition(Condition):

    def __init__(self, name):
        Condition.__init__(self, name)

class FalseCondition(Condition):

    def __init__(self, name):
        Condition.__init__(self, name)

    def check(self):
        return False