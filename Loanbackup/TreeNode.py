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
        self.lChild = []

    def newChild(self, Fname, pNode):
        newChild = TreeNode(Fname)
        self.lChild.append(newChild)
        newChild.Parent = pNode
        return newChild

    def set_modDate(self, modDate):
        self.modDate = modDate

    def list_Chldrn(self):
        for chld in self.lChild:
            print chld.Fname

    def has_Chldrn(self):
        if len(self.lChild) > 0:
            return True
        else:
            return False

    def build_path(self):
        if self.Parent == None:
            return self.Fname + "/"
        else:
            return self.Parent.build_path() + self.Fname + "/"
        
##testNode = TreeNode("Test")
##testNode2 = testNode.newChild("Test2", testNode)
##testNode3 = testNode.newChild("Test3", testNode2)
##testNode.newChild("tChild1")
##testNode.newChild("tChild2")
##testNode.newChild("tChild3")
##
##testNode.list_Chldrn()
##print testNode3.build_path()
