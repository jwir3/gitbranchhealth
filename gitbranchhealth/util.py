import os
from os import path

def isoDateComparator(aTupleList1, aTupleList2):
  """
  Comparison function to compare two branch tuples.

  @param aTupleList1 A branch tuple containing the following:
         1) The branch name and 2) A date tuple, with each tuple continaing the
         following: 2a) A human-readable date (e.g. '2 days ago'), and 2b) an
         iso-standardized date for comparison with other dates. Note that 2a and
         2b should be equivalent, with 2a being less accurate, but more easily
         interpretable by humans.
  @param aTupleList2 A second branch tuple, with the same specification as
         aTupleList1 which should be compared to aTupleList1.

  @returns -1, If the branch represented by aTupleList1 is older than the branch
           represented by aTupleList2; 1 if the branch represented by
           aTupleList2 is older than the branch represented by aTupleList1;
           0, otherwise.
  """
  (branchName1, valueTuple1) = aTupleList1
  (branchName2, valueTuple2) = aTupleList2

  (humanDate1, isoDate1) = valueTuple1
  (humanDate2, isoDate2) = valueTuple2

  if isoDate1 < isoDate2:
    return -1
  elif isoDate1 == isoDate2:
    return 0

  return 1

def isGitRepo(aPathStr):
  """
  Determine if a string path is a git repository. That is, determine if there
  is a directory within the given path called '.git'.

  @param aPathStr The string representation of a path to check for the existence
         of a '.git' subdirectory.

  @return True, if aPathStr contains a subdirectory called '.git'; False,
          otherwise.
  """
  try:
    names = os.listdir(aPathStr)
  except Exception as e:
    print(e)
    return False

  for name in names:
    if path.isdir(path.join(aPathStr, '.git')):
      return True
  return False

def hasGitDir(aPath):
  """
  Determine if a specified path from an iteration of walkUp has the special
  '.git' directory.

  @param aPath A tuple containing the path name as a string, a list of
         directories contained in the path, and a list of non-directories
         contained in the path.

  @return The directory path, as a string, if aPath contains a directory called
          '.git'; False, otherwise.
  """
  (bottom, dirs, nondirs) = aPath

  if '.git' in dirs:
    return bottom
  return False
