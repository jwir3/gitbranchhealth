import unittest
import sys
import gitbranchhealth.util
import os.path

class UtilTestSuite(unittest.TestCase):
  def setUp(self):
    pass

  def test_is_git_dir(self):
    path = os.path.join(os.path.dirname(__file__))
    self.assertFalse(gitbranchhealth.util.isGitRepo(path))
    repoPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    self.assertTrue(gitbranchhealth.util.isGitRepo(repoPath))

def allTests():
  unittest.main()

if __name__ == '__main__':
  allTests()
