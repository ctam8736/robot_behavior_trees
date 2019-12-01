#! /usr/bin/env python

"""
Example tree usage involving manual edge setup.
"""

import rospy

from control_nodes import SequenceNode, SelectorNode, ParallelNode, RootNode, ClientNode
from action_nodes import twist_right, move_forward
from condition_nodes import wall_check

rospy.init_node('tree')
m_f = move_forward.ActionServer('move_forward')
t_r = twist_right.ActionServer('twist_right')

#if wall in front, twist right, else move forward
root = RootNode('root')
action1 = ClientNode('move_forward')
action2 = ClientNode('twist_right')
sequence1 = SequenceNode('turn_at_wall')
selector1 = SelectorNode('dumb_roomba')
condition1 = wall_check.WallCheckNode('wall_check')

sequence1.add_child(condition1)
sequence1.add_child(action2)

selector1.add_child(sequence1)
selector1.add_child(action1)

root.add_child(selector1)

#repeatedly tick root
rate = rospy.Rate(10)
while not rospy.is_shutdown():
    status = root.tick()
    #print(root.name + " is " + status)
    if status is "success":
        print(root.name + " is " + status + " and resetting.")
        root.reset()
    rate.sleep()