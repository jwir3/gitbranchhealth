import os
from os import path

def __do_walk_up(bottom):
  """
  Generator function for walking up a specified bottom path to the root.

  Based on the 'walk_up' function written by @zdavkeos available at:
  https://gist.github.com/zdavkeos/1098474

  @param aBottom The path at which to start walking up.

  @return A tuple containing the path name as a string, a list of directories
          contained in the path, and a list of non-directories contained in
          the path.
  """

  bottom = path.realpath(bottom)

  #get files in current dir
  try:
    names = os.listdir(bottom)
  except Exception as e:
    print e
    return

  dirs, nondirs = [], []
  for name in names:
    if path.isdir(path.join(bottom, name)):
      dirs.append(name)
    else:
      nondirs.append(name)

  yield bottom, dirs, nondirs

  new_path = path.realpath(path.join(bottom, '..'))

  # see if we are at the top
  if new_path == bottom:
    return

  for x in __do_walk_up(new_path):
    yield x

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

def walkUp(aBottom, aVisitor=hasGitDir):
  """
  Walk up a directory structure, until a specified condition is met.

  @param aBottom The starting point (a path) from which to 'walk up'.
  @param aVisitor A method that will be passed the path at each stage
         of the 'walking'. If this method returns non-False, then the execution
         will cease.

  @return The return value of aVisitor on the first path, x, such that
          aVisitor(x) is non-False.
  """
  if not aVisitor:
    raise AttributeError('Visitor does not exist')

  for i in __do_walk_up(aBottom):
    visitation = aVisitor(i)
    if visitation:
      return visitation

  return None
