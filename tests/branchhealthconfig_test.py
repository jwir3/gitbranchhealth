import unittest
import sys
import os
from gitbranchhealth.branchhealthconfig import BranchHealthConfig
from git import Repo

class BranchHealthTestSuite(unittest.TestCase):
  def test_config_color(self):
      repo = Repo(".")
      conf = BranchHealthConfig(repo)
      color = conf.shouldUseColor()
      self.assertTrue(color)

def allTests():
  unittest.main()

if __name__ == '__main__':
  allTests()
