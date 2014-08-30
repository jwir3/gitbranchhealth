from datetime import timedelta
from datetime import datetime
from babel.dates import format_timedelta
import dateutil.parser

class Branch:
  """
  A Branch object consists of three components - the branch path, the last
  active date, and the relative last active date (used for when the branch
  is displayed).
  """

  def __init__(self, aBranchPath, aLastActivity):
    self.__mLastActivityRelative = None
    self.__mLastActivity = self.__parseDateFromString(aLastActivity)
    self.__mBranchPath = aBranchPath

  def __str__(self):
    return self.__mBranchPath + ", Last Activity: " + str(self.__mLastActivity) + "(" + self.__mLastActivityRelative +  ")"

  def getPath(self):
    return self.__mBranchPath

  def getLastActivity(self):
    return self.__mLastActivity

  def getLastActivityRelativeToNow(self):
    if not self.__mLastActivityRelative:
      self.__computeRelativeLastActivity()
    return str(self.__mLastActivityRelative)

  ## Private API ##

  def __parseDateFromString(self, aDateString):
    return dateutil.parser.parse(aDateString)

  def __computeRelativeLastActivity(self):
    curDateTime = datetime.now()
    difference = curDateTime - self.__mLastActivity
    self.__mLastActivityRelative = format_timedelta(difference) + " ago"
