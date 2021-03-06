# Git Branch-Health Tool
#
# A tool for showing, with colors, the health of branches, both locally and
# on remotes, of a specified git repository. The health of a branch is
# computed using the time since last activity was recorded on the branch. This
# can be specified on the command line.
#
# Inspired by Felipe Kiss' "Show Last Activity On Branch" script, available at:
# https://coderwall.com/p/g-1n9w
#

import logging
import sys
import os

from git import *

import argparse
import sys
from datetime import *
import dateutil.parser
from colors import red, yellow, green

from branch import Branch
from config import BranchHealthConfig
from manager import BranchManager
from util import parseIgnoredBranchListFromString

class BranchHealthApplication:
  """
  Application context that contains configuration and display data related to
  the overall application. Can be instantiated as a standalone application, or
  as a harness for testing.
  """

  def __init__(self, aArguments=None):
    """
    Create a new BranchHealthApplication context.

    @param aConfig Configuration information to initialize the application.
    @param aArguments Command line arguments to initialize the application with
           if no arguments are given, default values will be assigned.
    """
    self.__mArgParser = self.__createParser()

    if aArguments:
      self.__mConfig = self.__parseArguments(aArguments)
    else:
      self.__mConfig = BranchHealthConfig('.', aLogLevel=0)

  def showBranchHealth(self, aStream=sys.stdout):
    """
    Output the health of all branches from the branch map given in the BranchManager.
    This displays the branches in descending order of last activity age.

    :param aStream: An output stream to send the output to.
    """
    branchMap = []

    config = self.getConfig()
    log = config.getLog()
    remoteName = config.getRemoteName()
    repoPath = config.getRepoPath()

    if log:
      log.debug('Operating on repository in: ' + repoPath)
      log.debug('Operating on remote named: ' + str(remoteName))

    repo = config.getRepo()
    manager = BranchManager(config)

    branchMap = manager.getBranchMap()
    self.__printBranchHealthChart(branchMap, aStream)

  def getConfig(self):
    """
    Retrieve the BranchHealthConfig object that determines the settings for this
    context. These are a combination of command line arguments (if given) and git
    configuration file options.

    @returns A BranchHealthConfig object representing the settings for this
             application context.
    """
    return self.__mConfig

  def getLog(self):
    """
    Retrieve the logging object for this application context.

    @returns A logging object which can be written to for this application
             instance.
    """
    return self.getConfig().getLog()

  def printHelp(self):
    """
    Print out the help (usage notes) for this application.
    """
    self.__mArgParser.print_help()

  def __createParser(self):
    """
    Construct an argparse parser for use with this context to parse command
    line arguments.

    @returns An argparse parser object which can be used to parse command line
             arguments, specific to git-branchhealth.
    """

    parser = argparse.ArgumentParser(description='''
       Show health (time since creation) of git branches, in order.
    ''', add_help=True)
    parser.add_argument('-v', action='count', dest='logLevel',
                        help='Specify how verbose the output should be (-v to -vvv)')
    parser.add_argument('-b', '--bad-only', action='store_true',
                        help='Only show branches that are ready for pruning (i.e. older than numDays * 2)',
                        dest='badOnly')
    parser.add_argument('-d', '--days', action='store', dest='numDays',
                        help='Specify number of days old where a branch is considered to no longer be \'healthy\'',
                        default=14)
    parser.add_argument('-n', '--nocolor', action='store_true', help="Don't use ANSI colors to display branch health",
                        dest='noColor')
    parser.add_argument('-R', '--repository', action='store',  metavar=('repository'), help='Path to git repository where branches should be listed', nargs='?', default='.', dest='repo')
    parser.add_argument('-D', '--delete', action='store_true', help='Delete old branches that are considered "unhealthy"', dest='deleteOld')
    parser.add_argument('-i-', '--ignore-branches', action='store', help='Ignore a set of branches specified by a comma-separated list of branch names', dest='ignoredBranches', default='master')
    parser.add_argument('-t', '--trunk', action='store', help='Specify the trunk branch name for the given repository', metavar=('trunkBranch'), dest='trunkBranch', default='master')

    # Make sure that only one of -r and --all-remotes is specified
    remoteGroup = parser.add_mutually_exclusive_group()
    remoteGroup.add_argument('-r', '--remote', metavar=('<remote name>'), action='store',
                             help='Operate on specified remote', default=None,
                             dest='remote')
    remoteGroup.add_argument('--all-remotes', action='store_true', dest='allRemotes',
                             help='Run a branch health check for all remotes, including local branches')


    return parser

  def __parseArguments(self, aArguments):
    """
    Parse command line arguments given to this application.

    :returns: A BranchHealthConfig object populated with the values from the command
              line arguments, as well as the values from the git configuration file
              for a given repository (if it exists).
    """
    parsed = self.__mArgParser.parse_args(aArguments)

    # Retrieve the git repository, if one wasn't given on the command line
    repo = parsed.repo

    ignoredBranches = parseIgnoredBranchListFromString(parsed.ignoredBranches)

    logLevel = parsed.logLevel
    if not logLevel:
      logLevel = 0

    if logLevel > 3:
      logLevel = 3

    possibleLogLevels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]

    remote = 'local'
    if parsed.remote:
      remote = parsed.remote
    elif parsed.allRemotes:
      remote = 'all'

    return BranchHealthConfig(repo, remote, parsed.numDays, parsed.badOnly, parsed.noColor, parsed.deleteOld, parsed.trunkBranch, ignoredBranches, possibleLogLevels[logLevel])

  def __printBranchHealthChart(self, aBranchMap, aStream):
    """
    Print out a 'health chart' of different branches and when they were last
    changed. The health chart will color the given branches such that:
        - Branches with last activity longer than double the number of 'healthy
          days' ago will be colored in RED.
        - Branches with last activity longer than the number of 'healthy days'
          ago will be colored in YELLOW.
        - All other branches will be colored in GREEN

    :param aBranchMap: A list of Branch objects. Note that this list is assumed to
                       be pre-sorted in the order in which they should be output.
    :param aStream: An output stream to print the data to.
    """

    config = self.getConfig()
    badOnly = config.getBadOnly()
    noColor = not config.shouldUseColor()

    log = config.getLog()

    deleteBucket = []
    for someBranch in aBranchMap:
      branchPath = someBranch.getPath()
      branchHealth = someBranch.getHealth()
      lastActivityRel = someBranch.getLastActivityRelativeToNow()

      # If this is an unhealthy branch, then let's put it in the "delete"
      # bucket.
      if branchHealth == Branch.OLD:
        deleteBucket.append(someBranch)

      # Skip healthy and aged branches if we're only looking for bad ones
      if badOnly and not branchHealth == Branch.OLD:
        continue

      if not noColor:
        if branchHealth == Branch.HEALTHY:
          coloredDate = green(lastActivityRel)
        elif branchHealth == Branch.AGED:
          coloredDate = yellow(lastActivityRel)
        else:
          coloredDate = red(lastActivityRel)
      else:
          coloredDate = lastActivityRel

      alignedPrintout = '{0:40} {1}\n'.format(branchPath + ":", coloredDate)
      aStream.write(alignedPrintout)

    if config.shouldDeleteOldBranches():
      manager = BranchManager(config)
      manager.deleteAllOldBranches(deleteBucket)

# Main entry point
def runMain(aInOldMode=False):
  if aInOldMode:
    print("WARNING: 'git branchhealth' has been replaced with 'git branch-health'. The older command variant will be removed in the 1.0 release.")

  context = BranchHealthApplication(sys.argv[1:])

  if context.getConfig().getRepoPath() == None:
    context.printHelp()
    return

  context.showBranchHealth()

# Entry point for 'git branchhealth', the old version of the command. This is
# provided only for backwards compatibility. Notify the user that this will be
# going away as of version 1.0.
def runMainOld():
  runMain(True)

if __name__ == '__main__':
  runMain()
