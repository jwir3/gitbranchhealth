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

  def tearDown(self):
    self.__mParent.tearDown()

  def test_manager_construction(self):
    manager = BranchManager(self.__mConfig)
    localBranches = manager.getLocalBranchNames()

    expectedBranches = ['bug-14', 'bug-143', 'bug-27', 'bug-44', 'master']
    self.assertEquals(expectedBranches, localBranches)

  def test_get_prefix(self):
    conf = self.__mConfig
    manager = BranchManager(conf)
    pref1 = manager.getPrefix(conf.getRepo().heads)
    pref2 = manager.getPrefix(conf.getRepo().remotes.origin.refs[0])
    self.assertEquals('refs/heads/', pref1)
    self.assertEquals('refs/remotes/', pref2)


  def test_get_branch_map(self):
    # Set 'days' to 1 so that all branches should be old
    # Initially test local branches
    conf = self.__mConfig
    config = BranchHealthConfig(conf.getRepoPath(),
                                conf.getRemoteName(),
                                1,
                                aLogLevel=logging.ERROR)
    manager = BranchManager(config)
    branchMap = manager.getBranchMap()
    expectedBranches = ['bug-14', 'bug-44', 'bug-27', 'bug-143']
    actualBranches = []
    for someBranch in branchMap:
      self.assertEquals(Branch.OLD, someBranch.getHealth())
      actualBranches.append(someBranch.getName())

    self.assertEquals(expectedBranches, actualBranches)

    # Now perform the same stuff, but on origin as a remote
    config = BranchHealthConfig(conf.getRepoPath(),
                                'origin',
                                1,
                                aLogLevel=logging.ERROR)
    manager = BranchManager(config)
    actualBranches = []
    for someBranch in branchMap:
      self.assertEquals(Branch.OLD, someBranch.getHealth())
      actualBranches.append(someBranch.getName())

    self.assertEquals(expectedBranches, actualBranches)

    # Finally, check the same thing, but using "all" option:
    config = BranchHealthConfig(conf.getRepoPath(),
                                'all',
                                1,
                                aLogLevel=logging.ERROR)
    manager = BranchManager(config)
    branchMap = manager.getBranchMap()
    expectedBranches = ['bug-14', 'bug-14', 'bug-44', 'bug-44', 'bug-27', 'bug-27', 'bug-143', 'bug-143']
    actualBranches = []
    for someBranch in branchMap:
      self.assertEquals(Branch.OLD, someBranch.getHealth())
      actualBranches.append(someBranch.getName())

    self.assertEquals(expectedBranches, actualBranches)

  def test_get_local_branches(self):
    manager = BranchManager(self.__mConfig)
    branches = manager.getLocalBranches()
    branchNames = manager.getLocalBranchNames()
    names = []
    for branch in branches:
      names.append(branch.getName())

    self.assertEquals(branchNames, names)

  def test_delete_all_old_branches(self):
    # TODO: A test needs to be written for deleteAllOldBranches(), as soon as it
    #       is rewritten to conform to the new branch-object style (it's currently
    #       using the old tuple style). See issue #
    pass

def allTests():
  unittest.main()

if __name__ == '__main__':
  allTests()
