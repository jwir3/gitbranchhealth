from datetime import timedelta
from datetime import datetime
from babel.dates import format_timedelta
import dateutil.parser
from datetime import *
import pytz

class Branch:
  """
  A Branch object consists of three components - the branch path, the last
  active date, and the relative last active date (used for when the branch
  is displayed).
  """

  # Constants specifying branch health
  HEALTHY = 0
  AGED = 1
  OLD = 2

  def __init__(self, aBranchPath, aOptions):
    self.__mLastActivityRelative = None
    self.__mBranchPath = aBranchPath
    self.__mOptions = aOptions
    self.__computeLastActivity()

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

  def getHealth(self):
    return self.__mHealth

  ## Private API ##

  def __computeLastActivity(self):
    repo = self.__mOptions.getRepo()
    assert(repo.bare == False)
    gitCmd = repo.git

    hasActivityNonRel = gitCmd.log('--abbrev-commit', '--date=iso', '-1', self.getPath())
    hasActivityNonRelLines = hasActivityNonRel.split('\n')
    i = 0
    for line in hasActivityNonRelLines:
      if 'Date:' in line:
        lastActivity = line.replace('Date: ', '').strip()
        lastActivityNonRel = hasActivityNonRelLines[i].replace('Date: ', '').strip()
        print("Last activity: " + str(lastActivity))
        self.__mLastActivity = self.__parseDateFromString(lastActivityNonRel).astimezone(pytz.timezone("UTC")).replace(tzinfo=None)
        break
      i = i + 1

  def markHealth(self, aHealthyDays):
    """
    Determine whether this branch is healthy, based on the date of last activity.

    @param aHealthyDays The number of days that a branch can be untouched and
           still be considered 'healthy'.
    """

    branchPath = self.getPath()
    isoDate = self.getLastActivity()
    humanDate = self.getLastActivityRelativeToNow()

    branchLife = date.today() - isoDate.date()
    if branchLife > timedelta(aHealthyDays * 2):
      self.__mHealth = Branch.OLD
    elif branchLife > timedelta(aHealthyDays):
      self.__mHealth = Branch.AGED
    else:
      self.__mHealth = Branch.HEALTHY

  def __parseDateFromString(self, aDateString):
    return dateutil.parser.parse(aDateString)

  def __computeRelativeLastActivity(self):
    curDateTime = datetime.utcnow()
    difference = curDateTime - self.__mLastActivity
    self.__mLastActivityRelative = format_timedelta(difference) + " ago"
