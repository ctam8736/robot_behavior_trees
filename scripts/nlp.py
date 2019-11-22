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


def apply_op(operators, values):
    operator = operators.pop()
    right = values.pop()
    left = values.pop()
    node = None
    if operator == "and":
        node = ParallelNode("dummy", 2, 2)
    elif operator == "or":
        node = SelectorNode("dummy", 2, 2)
    node.add_child(left)
    node.add_child(right)
    values.append(node)

#get input      
command = raw_input("Enter command: ").split()
last_phrase = []

#perform basic shunting yard
values = []
operators = []
for word in command:
    if word == "and" or word == "or":
        last_phrase = []
        operators.append(word)
    else:
        last_phrase.append(word)
        if tuple(last_phrase) in dictionary:
            values.append(ClientNode("_".join(last_phrase)))
            print("_".join(last_phrase))
            last_phrase = []

while len(operators) > 0:
    apply_op(operators, values)
if values:
    root.add_child(values.pop())

rate = rospy.Rate(10)
while not rospy.is_shutdown():
    status = root.tick()
    #print(root.name + " is " + status)
    if status is "success":
        print(root.name + " is " + status + " and resetting.")
        root.reset()
    rate.sleep()