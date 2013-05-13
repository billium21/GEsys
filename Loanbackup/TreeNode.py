# TreeNode Class

class TreeNode:
    
    def __init__(self, Fname):
        self.Parent = None
        self.Fname = Fname
        self.modDate = 0
        self.lChild = []

    def newChild(self, Fname):
        newChild = TreeNode(Fname)
        self.lChild.append(newChild)
        newChild.Parent = self.Fname
        return newChild

    def set_modDate(self, modDate):
        self.modDate = modDate

testNode = TreeNode("Test")
TestChild = testNode.newChild("tChild")
TestChild.set_modDate(1023)

print TestChild.Parent
