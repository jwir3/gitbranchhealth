from setuptools import setup
import os
from pip.req import parse_requirements

progName = 'gitbranchhealth'
progVersion = '0.2'
progDescription='A tool for determining the health of branches in a git repository',
progAuthor = 'Scott Johnson'
progEmail = 'jaywir3@gmail.com'
progUrl = 'http://github.com/jwir3/gitbranchhealth'
downloadUrl = 'https://github.com/jwir3/gitbranchhealth/archive/gitbranchhealth-v0.2.tar.gz',
entry_points = { 'console_scripts': [
  'git-branchhealth = gitbranchhealth.branchhealth:runMain',
]}
installRequirements = parse_requirements("requirements.txt")
reqs = [str(ir.req) for ir in installRequirements]

setup(name=progName,
      version=progVersion,
      description=progDescription,
      author=progAuthor,
      author_email=progEmail,
      url=progUrl,
      packages=['gitbranchhealth'],
      entry_points=entry_points,
      test_suite='tests',
      install_requires=reqs
)
