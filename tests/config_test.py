import unittest
import sys
import os
from gitbranchhealth.config import BranchHealthConfig
from gitbranchhealth import branchhealth
from git import Repo

class BranchHealthTestSuite(unittest.TestCase):
  def setUp(self):
    self.__mContext = branchhealth.BranchHealthApplication()

  def test_config_color(self):
    color = self.__mContext.getConfig().shouldUseColor()
    self.assertTrue(color)

  def test_log_created(self):
    self.assertTrue(self.__mContext.getLog())
    
def allTests():
  unittest.main()

if __name__ == '__main__':
  allTests()
