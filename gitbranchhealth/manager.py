# manager.py
#
# Copyright (C) 2014 Scott Johnson <jaywir3@gmail.com>, and contributors
#
# Module for managing branches within git-branchhealth.

from git.refs.head import Head
from git.util import join_path
from git.refs.remote import RemoteReference
from git.refs.reference import Reference

from branch import Branch
from config import BranchHealthConfig
from util import branchDateComparator

class BranchManager:
  """
  Object used to manage Branch objects. This is the primary workhorse of the
  branch health processing algorithm. Each branch is associated with a given
  healthiness state, and this object does that association.
  """
  def __init__(self, aConfig):
    """
    Create a new BranchManager instance.

    :param aConfig: The :class:`config.BranchHealthConfig` object containing the
                    configuration options for the new instance.
    """
    self.__mConfig = aConfig
    self.__mBranchMap = []

  def getPrefix(self, aRef):
    """
    Retrieve the prefix of the git path for a given Reference object. If this is
    a remote reference, this will be 'refs/remotes/', otherwise this will be
    'refs/heads/'.

    :param aRef: The Reference object for which the prefix should be retrieved.

    :return: A string for the prefix of the git path to the reference.
    """
    if type(aRef) == RemoteReference:
      return 'refs/remotes/'
    return 'refs/heads/'

  def getBranchMap(self, aRefList):
    """
    Retrieve the branch map for this manager for all local branches. The branch
    map is a list of Branch objects, each mapping a ref path to a
    healthy/aged/old status.

    :param aRefList: A list of Reference objects that should be processed and
                     mapped to healthy statuses.

    :return: A list of Branch objects, each of which maps one Reference in aRefList
             to a health status.
    """
    log = self.__mConfig.getLog()
    branchMap = []

    for branch in aRefList:
      branchPath = branch.path
      branchName = branchPath.split('/')[-1]

      # Don't include branches that should be ignored.
      shouldIgnore = False
      for ignoredBranch in self.__getOptions().getIgnoredBranches():
        if branchName == ignoredBranch:
          shouldIgnore = True
          break
      if shouldIgnore:
        continue

      newBranch = Branch(branchPath, self.__getOptions())
      branchMap.append(newBranch)
    return branchMap

  def getBranchMapFromRemote(self, aRemoteName):
    """
    Retrieve the branch map for this manager for all branches on a given remote.
    The branch map is a list of Branch objects, each mapping a ref path to a
    healthy/aged/old status.

    :param aRemoteName: The name of a remote for the repository being processed.

    :return: A list of Branch objects, each of which maps one Reference in aRefList
             to a health status.
    """

    log = self.__getOptions()
    if not aRemoteName:
      log.warn("Cannot get branches from nameless remote")
      return []

    repo = self.__getOptions().getRepo()
    assert(repo.bare == False)
    gitCmd = repo.git

    remoteToUse = None
    for someRemote in repo.remotes:
      if aRemoteName == someRemote.name:
        remoteToUse = someRemote

    remotePrefix = 'remotes/' + aRemoteName + '/'
    return self.getBranchMap(remoteToUse.refs)

  def getLocalBranches(self):
    """
    Retrieve all local branches for the repository currently being processed, as
    Branch objects.

    :return: A list of Branch objects, each a mapping of a local HEAD in the
             repository being processed.
    """
    branches = []
    branchNames = self.getLocalBranchNames()
    for branchName in branchNames:
      branchPath = 'refs/heads/' + branchName
      branch = Branch(branchPath, self.__getOptions())
      branches.append(branch)
    return branches

  def getLocalBranchNames(self):
    """
    Retrieve the names of all of the branches in the local git repository.

    :return: A list of the names of all the branches in the local git repository
             currently being processed, as strings.
    """
    repo = self.__mConfig.getRepo()
    heads = [x.name for x in repo.branches]
    return heads

def getBranchMapSortedByDate(self, aBranchMap, aHealthyDays):
  """
  Sort a list of Branch objects by the date the last activity occurred on them.

  :param aBranchMap: A list of Branch objects that map Reference objects to
                     a "healthy" status.
  :param aHealthyDays: The number of days that a branch can be untouched and
                       still be considered 'healthy'.

  :return: A list of Branch objects, guaranteed to be sorted in non-
           ascending order, by the iso-standardized date of last activity.
  """
  sortedBranchMap = sorted(aBranchMap, cmp=branchDateComparator)

  finalBranchList = []
  for someBranch in sortedBranchMap:
    someBranch.markHealth(aHealthyDays)
    branchPath = someBranch.getPath()
    humanDate = someBranch.getLastActivityRelativeToNow()
    branchHealth = someBranch.getHealth()
    finalBranchList.append(someBranch)

  return finalBranchList

  def deleteAllOldBranches(self, aBranchesToDelete):
    """
    Remove branches specified by name from both the local repository and the
    'origin' remote repository.

    :param aBranchesToDelete: A list containing the names of branches to delete.

    :warning: Use this method with care - it's operations are irreversible, and
              you may end up losing work!
    """
    log = self.__getOptions().getLog()
    for branchToDelete in aBranchesToDelete:
      (branchName, lastActivityRel, branchHealth) = branchToDelete
      if branchName.startswith('refs/heads'):
        self.__deleteOldBranch(branchName)
      elif branchName.startswith('remotes'):
        splitName = branchName.split('/')
        remoteName = splitName[len(splitName) - 2]
        self.__deleteOldBranch(branchName, remoteName, True)

  ## Private API ##

  def __getOptions(self):
    """
    Retrieve the options object that this BranchManager was instantiated
    with.

    :return: The BranchHealthConfig object that this BranchManager was created
             with.
    """
    return self.__mConfig

  def __deleteOldBranch(self, aBranch, aRemote='local', aShouldDeleteLocal=True):
    """
    Delete a given branch from a remote, the local repository, or both.

    :param aBranch: The path of the branch to remove.
    :param aRemote: The name of the remote repository on which to work (default:
                    'local', representing the local repository).
    :param aShouldDeleteLocal: If True and aRemote != 'local', then local branches
           will be removed as well as the remote ones; otherwise, only the remote
           branches will be removed.
    """
    log = self.__getOptions().getLog()
    repo = self.__getOptions().getRepo()

    # Cowardly refuse to remove the special 'master' branch
    if aBranch.split('/')[-1] == 'master':
      log.warn("Cowardly refusing to delete master branch")
      return

    if aRemote == 'local':
      log.debug("Going to delete LOCAL branch: " + aBranch)
      if aBranch.split('/')[-1] in repo.heads:
        Head.delete(aBranch.split('/')[-1])
    else:
      log.debug("Going to delete REMOTE branch: " + aBranch)
      branchRef = RemoteReference(repo, join_path('refs', aBranch))
      log.debug("Ready to delete: " + str(branchRef))
      RemoteReference.delete(repo, branchRef)

      # Now, delete the corresponding local branch, if it exists
      if aShouldDeleteLocal:
        self.deleteOldBranch(branchRef.remote_head)
