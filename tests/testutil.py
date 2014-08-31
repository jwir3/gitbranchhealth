import unittest
import tempfile
import os
from os.path import join
import zipfile

from gitbranchhealth.branchhealth import BranchHealthOptions

class GitRepoTest(unittest.TestCase):
  def setUp(self):
    self.__mTempDir = tempfile.mkdtemp(prefix='gitBranchHealthTest')
    self.assertTrue(os.path.exists(self.__mTempDir))

    testRepoZipPath = join(self.__findTestDir(), 'testrepo.zip')
    zipFh = open(testRepoZipPath, 'rb')
    testRepoZip = zipfile.ZipFile(zipFh)
    for name in testRepoZip.namelist():
      testRepoZip.extract(name, self.__mTempDir)
    zipFh.close()
    self.__mGitRepoPath = os.path.join(self.__mTempDir, 'testrepo')
    self.__mOptions = BranchHealthOptions(self.__mGitRepoPath, 'origin', 1, False, False, False)

  def getOptions(self):
    return self.__mOptions

  def getTempDir(self):
    return self.__mTempDir
    
  def __findTestDir(self):
    # Find the file called 'testrepo.zip', starting at the current dir
    for (root, dirs, files) in os.walk('.'):
      if 'testrepo.zip' in files:
        return root
