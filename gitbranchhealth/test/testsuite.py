import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import branchhealthconfig

class BranchHealthTestSuite(unittest.TestCase):
  def setUp(self):
    self.mConfigPath = os.path.join(os.path.dirname(__file__), "../../.git/config")

  def test_config_color(self):
      conf = branchhealthconfig.BranchHealthConfig(self.mConfigPath)
      color = conf.shouldUseColor()
      self.assertTrue(color)

if __name__ == '__main__':
  unittest.main()
