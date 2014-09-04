import unittest
import os

from gitbranchhealth.manager import BranchManager
from gitbranchhealth.branchhealth import BranchHealthConfig
from gitbranchhealth.branch import Branch
from gitbranchhealth.util import branchDateComparator
from testutil import GitRepoTest


class BranchTestSuite(GitRepoTest):
  def setUp(self):
    self.__mParent = super(BranchTestSuite, self)
    self.__mParent.setUp()

  def tearDown(self):
    self.__mParent.tearDown()

  # def test_relative_last_activity(self):
  #   curTime = datetime.datetime.now()
  #   fiveDaysAgo = curTime + datetime.timedelta(-5)
  #   aboutOneWeekAgo = curTime + datetime.timedelta(-8)
  #   branchOneWeek = Branch("/path/to/anotherbranch", str(aboutOneWeekAgo))
  #   branchFiveDays = Branch("/path/to/branch", str(fiveDaysAgo))
  #   self.assertEqual('5 days ago', branchFiveDays.getLastActivityRelativeToNow())
  #   self.assertEquals('1 week ago', branchOneWeek.getLastActivityRelativeToNow())

  def test_branch_sorting(self):
    options = self.__mParent.getConfig()
    manager = BranchManager(options)
    branches = [x.getName() for x in sorted(manager.getLocalBranches(), branchDateComparator)]
    expectedBranches = ['bug-14', 'bug-44', 'bug-27', 'bug-143', 'master']
    self.assertEqual(expectedBranches, branches)

  def test_mark_branch_health(self):
    options = self.__mParent.getConfig()
    manager = BranchManager(options)
    branches = manager.getLocalBranches()
    for someBranch in branches:
      someBranch.markHealth(options.getHealthyDays())
      self.assertEquals(Branch.OLD, someBranch.getHealth())

    # Now, create a new branch so we can test if it returns the value
    # Branch.HEALTHY
    repo = options.getRepo()
    repo.create_head('aNewBranch')
    repo.heads.aNewBranch.checkout()

    # Create a new file so we have a new commit
    fh = open(os.path.join(self.__mParent.getTempDir(), "testrepo/myNewFile"), "w")
    fh.write("TEST123")
    fh.close()

    index = repo.index
    index.add(['myNewFile'])
    index.commit("A new commit")

    newBranch = Branch('refs/heads/aNewBranch', options)
    newBranch.markHealth(options.getHealthyDays())
    self.assertEquals(Branch.HEALTHY, newBranch.getHealth())

def allTests():
  unittest.main()

if __name__ == '__main__':
  allTests()
