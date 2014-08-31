import git.config
from git import Repo
import ConfigParser
import os.path

class BranchHealthConfig:
  """
  Composition of all possible options for a given run of git branchhealth.
  """

  def __init__(self, aRepoPath, aRemoteName='', aNumDays=14, aBadOnly=False, aNoColor=False, aDeleteOldBranches=False, aIgnoredBranches=['master', 'HEAD'], aLog=None):
    """
    Initialize a new BranchHealthConfig object with parameters that were given
    from the command line.
    """
    self.mRepoPath = aRepoPath
    self.mRemoteName = aRemoteName
    self.mNumDays = aNumDays
    self.mBadOnly = aBadOnly
    self.mNoColor = aNoColor
    self.mRepo = Repo(self.mRepoPath)
    self.mLog = aLog
    self.mDeleteOldBranches = aDeleteOldBranches

    self.__mIgnoredBranches = aIgnoredBranches
    self.__setupConfigOptions()

  def shouldDeleteOldBranches(self):
    return self.mDeleteOldBranches

  def getIgnoredBranches(self):
    return self.__mIgnoredBranches

  def getRepo(self):
    return self.mRepo

  def getRepoPath(self):
    return self.mRepoPath

  def getRemoteName(self):
    return self.mRemoteName

  def getHealthyDays(self):
    return int(self.mNumDays)

  def getBadOnly(self):
    return self.mBadOnly

  def shouldUseColor(self):
    return not self.mNoColor

  def getLog(self):
    return self.mLog

  def setLog(self, aLog):
    self.mLog = aLog

  ## Private API ##

  def __setupParser(self):
    self.mParser = git.config.SectionConstraint(self.getRepo().config_reader(), 'branchhealth')

  def __setupIgnoreBranches(self):
    try:
      ignoreBranches = not self.mParser.get_value(option='noignore')
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
      ignoreBranches = True

    if not ignoreBranches:
      self.__mIgnoredBranches = []

  def __setupColor(self):
    try:
      color = not self.mParser.get_value(option='nocolor')
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
      color = True

    self.mNoColor = not color or self.mNoColor

  def __setupConfigOptions(self):
    self.__setupParser()
    log = self.getLog()
    self.__setupColor()
    self.__setupIgnoreBranches()
