#!/usr/bin/env python
import rospy
from control_nodes.sequence_node import SequenceNode
from control_nodes.selector_node import SelectorNode
from control_nodes.parallel_node import ParallelNode
from control_nodes.root_node import RootNode
from action_nodes.twist_right import TRActionServer
from action_nodes.twist_90 import T90ActionServer
from action_nodes.print_hello import PHActionServer
from action_nodes.move_forward import MFActionServer
from action_nodes.client_node import ClientNode
from condition_nodes.wall_check import WallCheckNode

rospy.init_node('tree')
root = RootNode('root')

dictionary = {("print", "hello"): PHActionServer('print_hello'),
              ("twist", "90"): T90ActionServer('twist_90')}

command = raw_input("Enter command: ").split()
last_phrase = []
stack = []
for word in command:
    last_phrase.append(word)
    if tuple(last_phrase) in dictionary:
        stack.append(ClientNode("_".join(last_phrase)))
        print("_".join(last_phrase))
        last_phrase = []
while len(stack) > 0:
    root.add_child(stack.pop())




#if (command == "turn"):

"""
t_90 = T90ActionServer('twist_90')
p_h = PHActionServer('print_hello')
action1 = ClientNode('print_hello')
action2 = ClientNode('twist_90')
parallel1 = ParallelNode('talker', 2, 2)
parallel1.add_child(action1)
parallel1.add_child(action2)
root.add_child(parallel1)
"""

rate = rospy.Rate(10)
while not rospy.is_shutdown():
    status = root.tick()
    #print(root.name + " is " + status)
    if status is "success":
        print(root.name + " is " + status + " and resetting.")
        root.reset()
    rate.sleep()