import unittest

from gitbranchhealth.manager import BranchManager
from gitbranchhealth.branchhealth import BranchHealthOptions
from testutil import GitRepoTest

class ManagerTestSuite(GitRepoTest):
  def setUp(self):
    self.__mParent = super(ManagerTestSuite, self)
    self.__mParent.setUp()
    self.__mOptions = self.__mParent.getOptions()
    self.__mTempDir = self.__mParent.getTempDir()

  def test_manager_construction(self):
    manager = BranchManager(self.__mOptions)
    localBranches = manager.getLocalBranchNames()

    expectedBranches = ['bug-14', 'bug-143', 'bug-27', 'bug-44', 'master']
    self.assertEquals(expectedBranches, localBranches)

  def test_get_branch_map(self):
    manager = BranchManager(self.__mOptions)
    repo = self.__mOptions.getRepo()
    branchMap = manager.getBranchMap(repo.refs)
    branchNames = []
    for someBranch in branchMap:
      branchNames.append(someBranch.getPath())

    expectedBranches = ['refs/heads/bug-14', 'refs/heads/bug-143', 'refs/heads/bug-27', 'refs/heads/bug-44']
    self.assertEquals(expectedBranches, branchNames)

def allTests():
  unittest.main()

if __name__ == '__main__':
  allTests()
