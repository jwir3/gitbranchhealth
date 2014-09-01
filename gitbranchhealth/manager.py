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

class BranchManager:
  """
  Object used to manage Branch objects. This is the primary workhorse of the
  branch health processing algorithm. Each branch is associated with a given
  healthiness state, and this object does that association.
  """
  def __init__(self, aConfig):
    self.__mConfig = aConfig
    self.__mBranchMap = []

  def getPrefix(self, aRef):
    """
    Retrieve the prefix of the git path for a given Reference object. If this is
    a remote reference, this will be 'refs/remotes/', otherwise this will be
    'refs/heads/'.

    @param aRef The Reference object for which the prefix should be retrieved.

    @returns A string for the prefix of the git path to the reference.
    """
    if type(aRef) == RemoteReference:
      return 'refs/remotes/'
    return 'refs/heads/'

  def getBranchMap(self, aRefList):
    """
    Retrieve the branch map for this manager. The branch map is a list of Branch
    objects, each mapping a ref path to a healthy/aged/old status.

    @param aRefList A list of Reference objects that should be processed and
           mapped to healthy statuses.

    @returns A list of Branch objects, each of which maps one Reference in aRefList
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
    branches = []
    branchNames = self.getLocalBranchNames()
    for branchName in branchNames:
      branchPath = 'refs/heads/' + branchName
      branch = Branch(branchPath, self.__getOptions())
      branches.append(branch)
    return branches

  def getLocalBranchNames(self):
    repo = self.__mConfig.getRepo()
    heads = [x.name for x in repo.branches]
    return heads

  def deleteAllOldBranches(self, aBranchesToDelete):
    log = self.__getOptions().getLog()
    for branchToDelete in aBranchesToDelete:
      (branchName, lastActivityRel, branchHealth) = branchToDelete
      if branchName.startswith('refs/heads'):
        self.__deleteOldBranch(branchName)
      elif branchName.startswith('remotes'):
        splitName = branchName.split('/')
        remoteName = splitName[len(splitName) - 2]
        self.__deleteOldBranch(branchName, remoteName, True)

  # Private API
  def __getOptions(self):
    """
    Retrieve the options object that this BranchManager was instantiated
    with.

    @return The BranchHealthConfig object that this BranchManager was created
            with.
    """
    return self.__mConfig

  def __deleteOldBranch(self, aBranch, aRemote='local', aShouldDeleteLocal=True):
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
