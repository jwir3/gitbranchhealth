import unittest
from os.path import abspath
from os.path import join
import tempfile
import os
import zipfile

from gitbranchhealth.manager import BranchManager
from gitbranchhealth.branchhealth import BranchHealthOptions


class ManagerTestSuite(unittest.TestCase):
  def setUp(self):
    self.__mTempDir = tempfile.mkdtemp(prefix='gitRiskTest')
    self.assertTrue(os.path.exists(self.__mTempDir))

    testRepoZipPath = join(self.findTestDir(), 'testrepo.zip')
    zipFh = open(testRepoZipPath, 'rb')
    testRepoZip = zipfile.ZipFile(zipFh)
    for name in testRepoZip.namelist():
      testRepoZip.extract(name, self.__mTempDir)
    zipFh.close()
    self.__mGitRepoPath = os.path.join(self.__mTempDir, 'testrepo')
    self.__mOptions = BranchHealthOptions(self.__mGitRepoPath, 'origin', 1, False, False, False)

  def test_manager_construction(self):
    manager = BranchManager(self.__mOptions)
    localBranches = manager.getLocalBranches()

    expectedBranches = ['bug-14', 'bug-143', 'bug-27', 'bug-44', 'master']
    self.assertEquals(expectedBranches, localBranches)

  def test_get_branch_map(self):
    manager = BranchManager(self.__mOptions)
    repo = self.__mOptions.getRepo()
    branchMap = manager.getBranchMap(repo.refs)
    branchNames = []
    for (branchName, lastActivity) in branchMap:
      branchNames.append(branchName)

    expectedBranches = ['refs/heads/bug-14', 'refs/heads/bug-143', 'refs/heads/bug-27', 'refs/heads/bug-44']
    self.assertEquals(expectedBranches, branchNames)

  def findTestDir(self):
    # Find the file called 'testrepo.zip', starting at the current dir
    for (root, dirs, files) in os.walk('.'):
      if 'testrepo.zip' in files:
        return root

def allTests():
  unittest.main()

if __name__ == '__main__':
  allTests()
