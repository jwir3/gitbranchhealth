import git.config
import ConfigParser

class BranchHealthConfig:
  def __init__(self, aPathToConfigFile):
    self.mParser = git.config.SectionConstraint(git.config.GitConfigParser(aPathToConfigFile), 'branchhealth')

  def shouldUseColor(self):
    try:
      color = self.mParser.get_value(option='nocolor')
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
      return True
    return color
