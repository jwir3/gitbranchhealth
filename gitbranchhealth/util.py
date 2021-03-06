import os
from os import path
from branch import Branch

def branchDateComparator(aBranch, aOther):
  """
  Comparison function to compare two Branch objects.

  @param aBranch A Branch object that has a last activity date, along with
                 a relative last activity date.
  @param aBranch Another Branch object that has a last activity date, along
                 with a relative last activity date to compare to aBranch.

  @returns -1, If the branch represented by aBranch is older than the branch
           represented by aOther; 1 if the branch represented by
           aOther is older than the branch represented by aBranch;
           0, otherwise.
  """
  branchPath1 = aBranch.getPath()
  branchPath2 = aOther.getPath()
  humanDate1 = aBranch.getLastActivityRelativeToNow()
  humanDate2 = aOther.getLastActivityRelativeToNow()
  isoDate1 = aBranch.getLastActivity()
  isoDate2 = aOther.getLastActivity()

  if isoDate1 < isoDate2:
    return -1
  elif isoDate1 == isoDate2:
    return 0

  return 1

def parseIgnoredBranchListFromString(aIgnoredBranchString):
  # We always want to ignore HEAD, because it's going to be covered by another
  # branch if it's not detached, and if it is detached, we don't want to deal
  # with it.
  ignoredBranches = set(['HEAD'])

  if len(aIgnoredBranchString) > 0:
    aIgnoredBranchString = aIgnoredBranchString.strip()
    branchNames = aIgnoredBranchString.split(',')
    for name in branchNames:
      ignoredBranches.add(name.strip())

  return list(ignoredBranches)
