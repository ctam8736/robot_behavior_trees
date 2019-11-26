#! /usr/bin/env python

"""
todo: navigates the campus rover to a set destination when called.
"""

import rospy
from action import Action

class ActionServer(Action):

  def __init__(self, name):
    Action.__init__(self, name)
    destination_pub = rospy.Publisher('destination', PoseStamped, queue_size=1)

  def do_action(self):
    pass

"""
def web_destination_cb(msg): # input json
    # clean input
    destination = json.loads(msg.data.replace("u\'","\"").replace("\'","\""))
    rospy.loginfo("New destination received from web server: {}".format(destination["name"]))

    goal_point = Point(destination["location"]["x"], destination["location"]["y"], destination["location"]["z"])
    goal_orientation = Quaternion(destination["orientation"]["x"], destination["orientation"]["y"], destination["orientation"]["z"], destination["orientation"]["w"])
    goal_pose_unstamped = Pose(goal_point, goal_orientation)
    goal_pose = PoseStamped(Header(),goal_pose_unstamped)
    goal_pose.header.stamp = rospy.get_rostime()
    goal_pose.header.frame_id = 'map'
"""