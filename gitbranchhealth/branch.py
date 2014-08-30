class Branch:
  """
  A Branch object consists of three components - the branch path, the last
  active date, and the relative last active date (used for when the branch
  is displayed).
  """

  def __init__(self, aBranchPath, aLastActivity, aLastActivityRelative):
    self.__mLastActivity = aLastActivity
    self.__mLastActivityRelative = aLastActivityRelative
    self.__mBranchPath = aBranchPath

  def __str__(self):
    return self.__mBranchPath + ", Last Activity: " + str(self.__mLastActivity) + "(" + self.__mLastActivityRelative +  ")"

  def getPath(self):
    return self.__mBranchPath

  def getLastActivity(self):
    return self.__mLastActivity

  def getLastActivityRelativeToNow(self):
    return self.__mLastActivityRelative
