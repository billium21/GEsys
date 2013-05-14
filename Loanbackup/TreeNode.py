# TreeNode Class

class TreeNode:

    """
    modDate will be used to compare the files in the backup to the files in the
    original locations. It will be a floating point number representing the number
    of seconds since the new epoch, because that's how os.path.getmtime does it.
    """

    def __init__(self, Fname):
        self.Parent = None
        self.Fname = Fname
        self.modDate = 0
        self.leafNode = True
        self.lChild = []

    def newChild(self, Fname):
        newChild = TreeNode(Fname)
        self.lChild.append(newChild)
        self.leafNode = False
        newChild.Parent = self
        return newChild

    def list_Chldrn(self):
        for chld in self.lChild:
            print chld.Fname

    def has_Chldrn(self):
        if len(self.lChild) > 0:
            return True
        else:
            return False

    def get_leaves(self):
        result = []
        for child in self.lChild:
            if child.leafNode == True:
                result.append(child.Fname)
        return result

    def build_path(self):
        if self.Parent == None:
            return self.Fname + "/"
        else:
            return self.Parent.build_path() + self.Fname + "/"
        
testNode = TreeNode("Test")
testNode2 = testNode.newChild("Test2")
testNode3 = testNode.newChild("Test3")
print testNode.lChild
##testNode.newChild("tChild1")
##testNode.newChild("tChild2")
##testNode.newChild("tChild3")
##
##testNode.list_Chldrn()
##print testNode3.build_path()
print testNode.get_leaves()
print testNode.build_path()
