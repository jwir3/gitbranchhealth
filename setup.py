from setuptools import setup
import os

progName = ''
progVersion = 'gitbranchhealth'
progDescription='A tool for determining the health of branches in a git repository',
progAuthor = 'Scott Johnson'
progEmail = 'jaywir3@gmail.com'
progUrl = 'http://github.com/jwir3/gitbranchhealth'
entry_points = { 'console_scripts': [
  'git-branchhealth = gitbranchhealth.BranchHealth:runMain',
]}

setup(name=progName,
      version=progVersion,
      description=progDescription,
      author=progAuthor,
      author_email=progEmail,
      url=progUrl,
      packages=['gitbranchhealth'],
      entry_points=entry_points,
      requires=['argparse', 'ansicolors']
)
