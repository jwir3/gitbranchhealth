from gitbranchhealth.branchhealth import BranchHealthApplication

from testutil import GitRepoTest

class BranchHealthTestSuite(GitRepoTest):
  def setUp(self):
    self.__mParent = super(BranchHealthTestSuite, self)
    self.__mParent.setUp()

  def tearDown(self):
    self.__mParent.tearDown()

  def test_arguments(self):
    context = BranchHealthApplication(['-t', 'mainline'])
    trunkName = context.getConfig().getTrunkBranchName()
    self.assertEquals('mainline', trunkName)

def allTests():
  unittest.main()

if __name__ == '__main__':
  allTests()
