import unittest
import sys
import os.path

import datetime
import time

from gitbranchhealth.branch import Branch

class BranchTestSuite(unittest.TestCase):
  def setUp(self):
    pass

  def test_relative_last_activity(self):
    curTime = datetime.datetime.now()
    fiveDaysAgo = curTime + datetime.timedelta(-5)
    aboutOneWeekAgo = curTime + datetime.timedelta(-8)
    branchOneWeek = Branch("/path/to/anotherbranch", str(aboutOneWeekAgo))
    branchFiveDays = Branch("/path/to/branch", str(fiveDaysAgo))
    self.assertEqual('5 days ago', branchFiveDays.getLastActivityRelativeToNow())
    self.assertEquals('1 week ago', branchOneWeek.getLastActivityRelativeToNow())

def allTests():
  unittest.main()

if __name__ == '__main__':
  allTests()
