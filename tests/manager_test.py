import unittest
import logging

from gitbranchhealth.manager import BranchManager
from gitbranchhealth.branchhealth import BranchHealthConfig
from gitbranchhealth.branch import Branch
from testutil import GitRepoTest

class ManagerTestSuite(GitRepoTest):
  def setUp(self):
    self.__mParent = super(ManagerTestSuite, self)
    self.__mParent.setUp()
    self.__mConfig = self.__mParent.getConfig()
    self.__mTempDir = self.__mParent.getTempDir()

  def test_manager_construction(self):
    manager = BranchManager(self.__mConfig)
    localBranches = manager.getLocalBranchNames()

    expectedBranches = ['bug-14', 'bug-143', 'bug-27', 'bug-44', 'master']
    self.assertEquals(expectedBranches, localBranches)

  def test_get_branch_map(self):
    # Set 'days' to 1 so that all branches should be old
    conf = self.__mConfig
    config = BranchHealthConfig(conf.getRepoPath(),
                                conf.getRemoteName(),
                                1,
                                aLogLevel=logging.DEBUG)
    manager = BranchManager(config)
    branchMap = manager.getBranchMap()
    expectedBranches = ['bug-14', 'bug-143', 'bug-27', 'bug-44']

    for someBranch in branchMap:
#      self.assertEquals(Branch.OLD, someBranch.getHealth())
      self.assertTrue(someBranch.getName() in expectedBranches)

def allTests():
  unittest.main()

if __name__ == '__main__':
  allTests()
