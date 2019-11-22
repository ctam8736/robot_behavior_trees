#! /usr/bin/env python
import rospy

from control_nodes.sequence_node import SequenceNode
from control_nodes.selector_node import SelectorNode
from control_nodes.parallel_node import ParallelNode
from control_nodes.root_node import RootNode
from action_nodes.twist_right import TRActionServer
from action_nodes.move_forward import MFActionServer
from action_nodes.client_node import ClientNode
from condition_nodes.wall_check import WallCheckNode

rospy.init_node('tree')
m_f = MFActionServer('move_forward')
t_r = TRActionServer('twist_right')

root = RootNode('root')
action1 = ClientNode('move_forward')
action2 = ClientNode('twist_right')
sequence1 = SequenceNode('turn_at_wall')
selector1 = SelectorNode('dumb_roomba')
condition1 = WallCheckNode('wall_check')

sequence1.add_child(condition1)
sequence1.add_child(action2)

selector1.add_child(sequence1)
selector1.add_child(action1)

root.add_child(selector1)

rate = rospy.Rate(50)
while not rospy.is_shutdown():
    status = root.tick()
    #print(root.name + " is " + status)
    if status is "success":
        print(root.name + " is " + status + " and resetting.")
        root.reset()
    rate.sleep()