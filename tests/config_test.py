import unittest
import sys
import os
from git import Repo

from gitbranchhealth.config import BranchHealthConfig
from gitbranchhealth import branchhealth
from gitbranchhealth.util import parseIgnoredBranchListFromString

from testutil import GitRepoTest

class ConfigTestSuite(GitRepoTest):
  def setUp(self):
    self.__mParent = super(ConfigTestSuite, self)
    self.__mParent.setUp()

    self.__mConfig = self.__mParent.getConfig()
    self.__mTempDir = self.__mParent.getTempDir()
    self.__mContext = branchhealth.BranchHealthApplication()

  def test_config_color(self):
    color = self.__mContext.getConfig().shouldUseColor()
    self.assertTrue(color)

  def test_log_created(self):
    self.assertTrue(self.__mContext.getLog())

  def test_default_ignored_branches(self):
    expectedIgnoredBranches = set(['master', 'HEAD'])
    ignoredBranches = self.__mContext.getConfig().getIgnoredBranches()
    self.assertEquals(expectedIgnoredBranches, set(ignoredBranches))

  def test_command_line_ignored_branches(self):
    ignoredBranches = 'bug-143'
    expectedIgnoredBranches = set(['bug-143', 'HEAD'])
    self.__mContext = branchhealth.BranchHealthApplication(['-i', 'bug-143'])
    conf = self.__mContext.getConfig()
    self.assertEquals(expectedIgnoredBranches, set(conf.getIgnoredBranches()))

  def test_config_file_ignored_branches(self):
    configFileHandle = open(os.path.join(self.__mTempDir, 'testrepo/.git/config'), "w")
    configFileHandle.write("[branchhealth]\n")
    configFileHandle.write("\tignoredbranches=bug-27")
    configFileHandle.close()
    repoDir = os.path.join(self.__mTempDir, "testrepo")
    self.__mContext = branchhealth.BranchHealthApplication(['-R', repoDir])
    expectedIgnoredBranches = set(['bug-27', 'HEAD'])
    conf = self.__mContext.getConfig()

    self.assertEquals(expectedIgnoredBranches, set(conf.getIgnoredBranches()))

  def test_both_ignored_branches(self):
    configFileHandle = open(os.path.join(self.__mTempDir, 'testrepo/.git/config'), "w")
    configFileHandle.write("[branchhealth]\n")
    configFileHandle.write("\tignoredbranches=bug-27")
    configFileHandle.close()
    repoDir = os.path.join(self.__mTempDir, "testrepo")
    self.__mContext = branchhealth.BranchHealthApplication(['-R', repoDir, '-i', 'bug-143'])
    expectedIgnoredBranches = set(['bug-27', 'HEAD', 'bug-143'])
    conf = self.__mContext.getConfig()

    self.assertEquals(expectedIgnoredBranches, set(conf.getIgnoredBranches()))

  def test_default_trunk_name(self):
    expectedTrunkName = 'master'
    trunkName = self.__mContext.getConfig().getTrunkBranchName()
    self.assertEquals(expectedTrunkName, trunkName)

  def test_command_line_trunk_name(self):
    expectedTrunkName = 'bug-143'
    self.__mContext = branchhealth.BranchHealthApplication(['-t', expectedTrunkName])
    conf = self.__mContext.getConfig()
    self.assertEquals(expectedTrunkName, conf.getTrunkBranchName())

  def test_config_file_trunk_name(self):
    expectedTrunkName = 'bug-27'
    configFileHandle = open(os.path.join(self.__mTempDir, 'testrepo/.git/config'), "w")
    configFileHandle.write("[branchhealth]\n")
    configFileHandle.write("\ttrunk=" + expectedTrunkName)
    configFileHandle.close()
    repoDir = os.path.join(self.__mTempDir, "testrepo")
    self.__mContext = branchhealth.BranchHealthApplication(['-R', repoDir])
    conf = self.__mContext.getConfig()

    self.assertEquals(expectedTrunkName, conf.getTrunkBranchName())

  def test_both_trunk_name(self):
    expectedBranchName = 'bug-143'
    configFileHandle = open(os.path.join(self.__mTempDir, 'testrepo/.git/config'), "w")
    configFileHandle.write("[branchhealth]\n")
    configFileHandle.write("\tignoredbranches=bug-27")
    configFileHandle.close()
    repoDir = os.path.join(self.__mTempDir, "testrepo")
    self.__mContext = branchhealth.BranchHealthApplication(['-R', repoDir, '-t', expectedBranchName])
    conf = self.__mContext.getConfig()

    self.assertEquals(expectedBranchName, conf.getTrunkBranchName())

def allTests():
  unittest.main()

if __name__ == '__main__':
  allTests()
