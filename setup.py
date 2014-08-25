from setuptools import setup
import os

progName = 'gitbranchhealth'
progVersion = '0.1'
progDescription='A tool for determining the health of branches in a git repository',
progAuthor = 'Scott Johnson'
progEmail = 'jaywir3@gmail.com'
progUrl = 'http://github.com/jwir3/gitbranchhealth'
downloadUrl = 'https://github.com/jwir3/gitbranchhealth/archive/v0.1.tar.gz',
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
      test_suite='tests',
      requires=['argparse', 'ansicolors', 'nicelog']
)
