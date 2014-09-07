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
    self.__mBranchMap = None

  def getBranchMap(self):
    config = self.__mConfig
    if self.__mBranchMap:
      return self.__mBranchMap

    config.getLog().debug("Remote name is: " + str(config.getRemoteName()))

    if not config.getRemoteName() or config.getRemoteName() == 'local':
      # We're operating on the local repo only.
      self.__mBranchMap = self.__getBranchMapFromRefList(config.getRepo().heads)
    elif config.getRemoteName() == 'all':
      # We're operating on ALL remotes, as well as local branches.
      self.__mBranchMap = []
      for remote in config.getRepo().remotes:
        self.__mBranchMap = self.__mBranchMap + self.__getRemoteBranchMap(remote.name)
      self.__mBranchMap = self.__mBranchMap + self.__getBranchMapFromRefList(config.getRepo().heads)
    else:
      # We're operating on a specific remote
      self.__mBranchMap = self.__getRemoteBranchMap(config.getRemoteName())

    return self.__sortBranchMapByDate()

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
      branch = Branch(branchPath, self.__getConfig())
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

  def deleteAllOldBranches(self, aBranchesToDelete):
    """
    Remove branches specified by name from both the local repository and the
    remote repository on which the branch health search was operating.

    :param aBranchesToDelete: A list containing the names of branches to delete.

    :warning: Use this method with care - it's operations are irreversible, and
              you may end up losing work!
    """
    log = self.__getConfig().getLog()
    for branchToDelete in aBranchesToDelete:
      branchPath = branchToDelete.getPath()
      lastActivityRel = branchToDelete.getLastActivityRelativeToNow()
      branchHealth = branchToDelete.getHealth()
      remoteName = 'local'
      if branchToDelete.isRemote():
        splitName = branchPath.split('/')
        remoteName = splitName[len(splitName) - 2]

      self.__deleteOldBranch(branchPath, remoteName)

  ## Private API ##

  def __sortBranchMapByDate(self):
    """
    Sort the list of Branch objects by the date the last activity occurred on them.

    :return: A list of Branch objects, guaranteed to be sorted in non-
             ascending order, by the iso-standardized date of last activity.
    """
    sortedBranchMap = sorted(self.__mBranchMap, cmp=branchDateComparator)

    finalBranchList = []
    for someBranch in sortedBranchMap:
      someBranch.markHealth()
      branchPath = someBranch.getPath()
      humanDate = someBranch.getLastActivityRelativeToNow()
      branchHealth = someBranch.getHealth()
      finalBranchList.append(someBranch)

    return finalBranchList

  def __getBranchMapFromRefList(self, aRefList):
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
      for ignoredBranch in self.__getConfig().getIgnoredBranches():
        if branchName == ignoredBranch:
          shouldIgnore = True
          break
      if shouldIgnore:
        continue

      newBranch = Branch(branchPath, self.__getConfig())
      branchMap.append(newBranch)
    return branchMap

  def __getRemoteBranchMap(self, aRemoteName):
    """
    Retrieve the branch map for this manager for all branches on a given remote.
    The branch map is a list of Branch objects, each mapping a ref path to a
    healthy/aged/old status.

    :param aRemoteName: The name of a remote for the repository being processed.

    :return: A list of Branch objects, each of which maps one Reference in aRefList
             to a health status.
    """

    log = self.__getConfig().getLog()
    if not aRemoteName:
      log.warn("Cannot get branches from nameless remote")
      return []

    repo = self.__getConfig().getRepo()
    assert(repo.bare == False)
    gitCmd = repo.git

    remoteToUse = None
    for someRemote in repo.remotes:
      if aRemoteName == someRemote.name:
        remoteToUse = someRemote

    remotePrefix = 'remotes/' + aRemoteName + '/'
    return self.__getBranchMapFromRefList(remoteToUse.refs)

  def __getConfig(self):
    """
    Retrieve the options object that this BranchManager was instantiated
    with.

    :return: The BranchHealthConfig object that this BranchManager was created
             with.
    """
    return self.__mConfig

  def __deleteOldBranch(self, aBranchPath, aRemote='local', aShouldDeleteLocal=True):
    """
    Delete a given branch from a remote, the local repository, or both.

    :param aBranchPath: The path of the branch to remove.
    :param aRemote: The name of the remote repository on which to work (default:
                    'local', representing the local repository).
    :param aShouldDeleteLocal: If True and aRemote != 'local', then local branches
           will be removed as well as the remote ones; otherwise, only the remote
           branches will be removed.
    """
    log = self.__getConfig().getLog()
    repo = self.__getConfig().getRepo()

    # Cowardly refuse to remove the special 'master' branch
    if aBranchPath.split('/')[-1] == 'master':
      log.warn("Cowardly refusing to delete master branch")
      return

    log.debug("Saw deletion request for remote named: " + str(aRemote))
    if aRemote == 'local':
      log.debug("Going to delete LOCAL branch: " + aBranchPath)
      if aBranchPath.split('/')[-1] in repo.heads:
        branchRef = Reference(repo, aBranchPath)

        # NOTE: Head.delete has a parameter in it's kwargs that allows you to
        #       specify whether to "force" this to be deleted, even if it hasn't
        #       been merged into the main development trunk.
        Head.delete(repo, branchRef)
    else:
      log.debug("Going to delete REMOTE branch: " + aBranchPath)
      branchRef = RemoteReference(repo, aBranchPath)
      log.debug("Ready to delete: " + str(branchRef))
      RemoteReference.delete(repo, branchRef)

      # Now, delete the corresponding local branch, if it exists
      if aShouldDeleteLocal:
        self.__deleteOldBranch(join_path('refs/heads', branchRef.remote_head))
