import unittest
import sys
import os.path
from os.path import join

import datetime
import time
import tempfile
import os
import zipfile

from gitbranchhealth.branch import Branch
from gitbranchhealth.branchhealth import BranchHealthOptions
from gitbranchhealth.manager import BranchManager

class BranchTestSuite(unittest.TestCase):
  def setUp(self):
    self.__mTempDir = tempfile.mkdtemp(prefix='gitBranchHealthTest')
    self.assertTrue(os.path.exists(self.__mTempDir))

    testRepoZipPath = join(self.findTestDir(), 'testrepo.zip')
    zipFh = open(testRepoZipPath, 'rb')
    testRepoZip = zipfile.ZipFile(zipFh)
    for name in testRepoZip.namelist():
      testRepoZip.extract(name, self.__mTempDir)
    zipFh.close()
    self.__mGitRepoPath = os.path.join(self.__mTempDir, 'testrepo')
    self.__mOptions = BranchHealthOptions(self.__mGitRepoPath, 'origin', 1, False, False, False)

  # def test_relative_last_activity(self):
  #   curTime = datetime.datetime.now()
  #   fiveDaysAgo = curTime + datetime.timedelta(-5)
  #   aboutOneWeekAgo = curTime + datetime.timedelta(-8)
  #   branchOneWeek = Branch("/path/to/anotherbranch", str(aboutOneWeekAgo))
  #   branchFiveDays = Branch("/path/to/branch", str(fiveDaysAgo))
  #   self.assertEqual('5 days ago', branchFiveDays.getLastActivityRelativeToNow())
  #   self.assertEquals('1 week ago', branchOneWeek.getLastActivityRelativeToNow())

  def test_mark_branch_health(self):
    manager = BranchManager(self.__mOptions)
    branches = manager.getLocalBranches()
    for someBranch in branches:
      someBranch.markHealth(self.__mOptions.getHealthyDays())
      self.assertEquals(Branch.OLD, someBranch.getHealth())

    # Now, create a new branch so we can test if it returns the value
    # Branch.HEALTHY
    repo = self.__mOptions.getRepo()
    repo.create_head('aNewBranch')
    repo.heads.aNewBranch.checkout()

    # Create a new file so we have a new commit
    fh = open(os.path.join(self.__mTempDir, "testrepo/myNewFile"), "w")
    fh.write("TEST123")
    fh.close()

    index = repo.index
    index.add(['myNewFile'])
    index.commit("A new commit")
    
    newBranch = Branch('refs/heads/aNewBranch', self.__mOptions)
    newBranch.markHealth(self.__mOptions.getHealthyDays())
    self.assertEquals(Branch.HEALTHY, newBranch.getHealth())

  def findTestDir(self):
    # Find the file called 'testrepo.zip', starting at the current dir
    for (root, dirs, files) in os.walk('.'):
      if 'testrepo.zip' in files:
        return root

def allTests():
  unittest.main()

if __name__ == '__main__':
  allTests()
