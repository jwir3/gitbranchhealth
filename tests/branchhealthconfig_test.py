import unittest
import sys
import os
from gitbranchhealth.branchhealthconfig import BranchHealthConfig

class BranchHealthTestSuite(unittest.TestCase):
  def setUp(self):
    self.mConfigPath = os.path.join(os.path.dirname(__file__), "../../.git/config")

  def test_config_color(self):
      conf = BranchHealthConfig(self.mConfigPath)
      color = conf.shouldUseColor()
      self.assertTrue(color)

def allTests():
  unittest.main()

if __name__ == '__main__':
  allTests()
