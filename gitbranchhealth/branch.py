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

  def __init__(self, aBranchPath, aConfig):
    self.__mLastActivityRelative = None
    self.__mBranchPath = aBranchPath
    self.__mConfig = aConfig
    self.__computeLastActivity()

  def __str__(self):
    return self.__mBranchPath + ", Last Activity: " + str(self.__mLastActivity) + "(" + self.__mLastActivityRelative +  ")"

  def isRemote(self):
    if self.getPath().startswith('refs/remotes'):
      return True
    return False

  def getPath(self):
    return self.__mBranchPath

  def getLastActivity(self):
    return self.__mLastActivity

  def getLastActivityRelativeToNow(self):
    if not self.__mLastActivityRelative:
      self.__computeRelativeLastActivity()
    return str(self.__mLastActivityRelative)

  def getHealth(self):
    self.markHealth()
    return self.__mHealth

  def getName(self):
    return self.getPath().split('/')[-1]

  def markHealth(self):
    """
    Determine whether this branch is healthy, based on the date of last activity.
    """

    healthyDays = self.__mConfig.getHealthyDays()
    branchPath = self.getPath()
    isoDate = self.getLastActivity()
    humanDate = self.getLastActivityRelativeToNow()

    branchLife = date.today() - isoDate.date()
    if branchLife > timedelta(healthyDays * 2):
      self.__mHealth = Branch.OLD
    elif branchLife > timedelta(healthyDays):
      self.__mHealth = Branch.AGED
    else:
      self.__mHealth = Branch.HEALTHY

  ## Private API ##

  def __computeLastActivity(self):
    repo = self.__mConfig.getRepo()
    assert(repo.bare == False)
    gitCmd = repo.git

    hasActivityNonRel = gitCmd.log('--abbrev-commit', '--date=iso', '-1', self.getPath())
    hasActivityNonRelLines = hasActivityNonRel.split('\n')
    i = 0
    for line in hasActivityNonRelLines:
      if 'Date:' in line:
        lastActivity = line.replace('Date: ', '').strip()
        lastActivityNonRel = hasActivityNonRelLines[i].replace('Date: ', '').strip()
        self.__mLastActivity = self.__parseDateFromString(lastActivityNonRel).astimezone(pytz.timezone("UTC")).replace(tzinfo=None)
        break
      i = i + 1

  def __parseDateFromString(self, aDateString):
    return dateutil.parser.parse(aDateString)

  def __computeRelativeLastActivity(self):
    curDateTime = datetime.utcnow()
    difference = curDateTime - self.__mLastActivity
    self.__mLastActivityRelative = format_timedelta(difference) + " ago"
