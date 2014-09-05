import git.config
from git import Repo
import ConfigParser
import os.path
import sys
from nicelog.formatters import ColorLineFormatter
import logging

from util import parseIgnoredBranchListFromString


class BranchHealthConfig:
  """
  Composition of all possible options for a given run of git branchhealth.
  """

  def __init__(self, aRepoPath, aRemoteName='', aNumDays=14, aBadOnly=False, aNoColor=False, aDeleteOldBranches=False, aIgnoredBranches=['master', 'HEAD'], aLogLevel=logging.ERROR):
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
    self.mDeleteOldBranches = aDeleteOldBranches

    self.__setupLogging(aLogLevel)

    self.__mIgnoredBranches = aIgnoredBranches
    for branch in self.__mIgnoredBranches:
      self.getLog().debug("(Command Line) Ignoring branch: " + str(branch))

    self.__setupConfigOptions()

    for branch in self.__mIgnoredBranches:
      self.getLog().debug("Ignoring branch: " + str(branch))

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
    return self.__mLog

  ## Private API ##

  def __setupLogging(self, aLogLevel=logging.DEBUG):
    log = logging.getLogger("git-branchhealth")
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(ColorLineFormatter())
    log.setLevel(aLogLevel)
    handler.setLevel(aLogLevel)

    log.addHandler(handler)

    self.__mLog = log

  def __setupParser(self):
    self.mParser = git.config.SectionConstraint(self.getRepo().config_reader(), 'branchhealth')

  def __setupIgnoreBranches(self):
    try:
      ignoredBranchString = self.mParser.get_value(option='ignoredbranches')
      self.getLog().debug("Ignored branch string is: " + str(ignoredBranchString))
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
      # Do nothing, since we just want to continue merrily.
      ignoredBranchString = ''

    branchSet = set(self.__mIgnoredBranches)

    # The default value for self.__mIgnoredBranches should be: 'HEAD' and 'master'.
    defaultBranches = set(['HEAD', 'master'])
    commandLineSpecified = defaultBranches != branchSet
    configSpecified = False
    configIgnoredBranches = []

    if len(ignoredBranchString) > 0:
      configIgnoredBranches = parseIgnoredBranchListFromString(ignoredBranchString)
      self.getLog().debug("Config ignored branches: " + str(configIgnoredBranches))
      configSpecified = len(configIgnoredBranches) != 0

    self.getLog().debug("Config specified? " + str(configSpecified))
    self.getLog().debug("Command line specified? " + str(commandLineSpecified))
    if configSpecified and commandLineSpecified:
      branchSet = branchSet.union(configIgnoredBranches)
      self.getLog().warn("Branches to be ignored specified on the command line (" + str(self.__mIgnoredBranches) + ") and those specified to be ignored in the config file (" + str(configIgnoredBranches) + ") are different. Ignoring the union of these two sets.")
    elif configSpecified:
      branchSet = set(configIgnoredBranches)
    else:
      branchSet = set(self.__mIgnoredBranches)

    branchList = list(branchSet)

    self.__mIgnoredBranches = branchList

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
