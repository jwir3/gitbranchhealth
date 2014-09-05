import unittest
import tempfile
import os
from os.path import join
import zipfile
from git import *
from shutil import rmtree

from gitbranchhealth.branchhealth import BranchHealthConfig

class GitRepoTest(unittest.TestCase):
  def setUp(self):
    self.__mOriginTempDir = tempfile.mkdtemp(prefix='gitBranchHealthTest')
    self.assertTrue(os.path.exists(self.__mOriginTempDir))

    # Create our origin first
    testRepoZipPath = join(self.__findTestDir(), 'testrepo.zip')
    zipFh = open(testRepoZipPath, 'rb')
    testRepoZip = zipfile.ZipFile(zipFh)
    for name in testRepoZip.namelist():
      testRepoZip.extract(name, self.__mOriginTempDir)
    zipFh.close()
    self.__mOriginGitRepoPath = os.path.join(self.__mOriginTempDir, 'testrepo')

    originRepo = Repo(self.__mOriginGitRepoPath)

    self.__mTempDir = tempfile.mkdtemp(prefix='gitBranchHealthTest')
    os.mkdir(os.path.join(self.__mTempDir, 'testrepo'))
    self.assertTrue(os.path.exists(self.__mTempDir))

    # Now create the local repo
    self.__mGitRepoPath = os.path.join(self.__mTempDir, 'testrepo')
    originRepo.clone(self.__mGitRepoPath)
    self.assertTrue(os.path.exists(self.__mGitRepoPath))
    self.__mConfig = BranchHealthConfig(self.__mGitRepoPath)
    self.__trackAllRemoteBranches()

  def tearDown(self):
    pass
    # rmtree(self.__mTempDir)
    # rmtree(self.__mOriginTempDir)

  def getConfig(self):
    return self.__mConfig

  def getTempDir(self):
    return self.__mTempDir

  ## Private API ###

  def __trackAllRemoteBranches(self):
    repo = Repo(self.__mGitRepoPath)
    for remote in repo.remotes:
      for branch in remote.refs:
        localBranchName = branch.name.split('/')[-1]
        if localBranchName != 'master' and localBranchName != 'HEAD':
          repo.git.checkout(branch.name, b=localBranchName)

    repo.heads.master.checkout()

  def __findTestDir(self):
    # Find the file called 'testrepo.zip', starting at the current dir
    for (root, dirs, files) in os.walk('.'):
      if 'testrepo.zip' in files:
        return root
