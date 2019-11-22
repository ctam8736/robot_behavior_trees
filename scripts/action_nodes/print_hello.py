#! /usr/bin/env python


import rospy
import actionlib
from campus_rover_behavior_tree.msg import BTAction, BTGoal, BTFeedback, BTResult

class PHActionServer(object):
  # create messages that are used to publish feedback/result
  _feedback = BTFeedback()
  _result   = BTResult()

  def __init__(self, name):
    self.name = name
    self._as = actionlib.SimpleActionServer(self.name, BTAction, execute_cb=self.execute_cb, auto_start = False)
    self._as.start()
    
  def execute_cb(self, goal):
    success = True
    
    self.do_prints()
      
    if success:
      self.set_status('SUCCESS')

  def set_status(self,status):
      if status == 'SUCCESS':
        self._feedback.status = 1
        self._result.status = self._feedback.status
        #rospy.loginfo('Action %s: Succeeded' % self.name)
        self._as.set_succeeded(self._result)
      elif status == 'FAILURE':
        self._feedback.status = 2
        self._result.status = self._feedback.status
        #rospy.loginfo('Action %s: Failed' % self.name)
        self._as.set_succeeded(self._result)
      else:
        #rospy.logerr('Action %s: has a wrong return status' % self.name)
        pass

  def do_prints(self):
      rate = rospy.Rate(3)
      for i in range(10):
          print("Hello!")
          rate.sleep()


if __name__ == '__main__':
  rospy.init_node('print_hello')
  server = BTActionServer('print_hello')
  rospy.spin()