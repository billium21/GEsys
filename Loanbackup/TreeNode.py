# TreeNode Class
import os


class TreeNode:

    """
    modDate will be used to compare the files in the backup to the files in the
    original locations. It will be a floating point number representing the number
    of seconds since the new epoch, because that's how os.path.getmtime does it.
    """

    def __init__(self, Fname, modDate=0):
        self.Parent = None
        self.Fname = Fname
        self.modDate = modDate
        self.leafNode = True
        self.lChild = []

    def newChild(self, Fname, modDate=0):
        newChild = TreeNode(Fname, modDate)
        self.lChild.append(newChild)
        self.leafNode = False
        newChild.Parent = self
        return newChild

    def list_Chldrn(self):
        for chld in self.lChild:
            print chld.Fname

    #I think this is redundant of the leafnode attribute. Remove?
    def has_Chldrn(self):
        if len(self.lChild) > 0:
            return True
        else:
            return False

    def get_leaves(self):
        #result = []
        #for child in self.lChild:
            #if child.leafNode:
                #result.append(child.Fname)
        #return result
        return [child.Fname for child in self.lChild if child.leafNode]

    def __getattr__(self, name):
        if name is 'leaf_names':
            return [child.Fname for child in self.lChild if child.leafNode]
        elif name is 'child_name_date':
            return [(child.Fname, child.modDate) for child in self.lChild]
        elif name is 'name_date':
            return (self.Fname, self.modDate)
        else:
            raise AttributeError('%s not a valid attribute' % name)

    def build_path(self):
        if self.Parent:
            return self.Parent.build_path() + self.Fname + os.sep
        else:
            return self.Fname + os.sep


#Depth-first traverse the tree and call visit function on each node.
def df_traverse(root, visit_func):
    pass


if __name__ == '__main__':

    testNode = TreeNode("Test")
    testNode2 = testNode.newChild("Test2")
    testNode3 = testNode.newChild("Test3")
    testNode4 = testNode3.newChild("Test4")
    #print testNode.lChild
    ##testNode.newChild("tChild1")
    ##testNode.newChild("tChild2")
    ##testNode.newChild("tChild3")
    ##
    ##testNode.list_Chldrn()
    ##print testNode3.build_path()
    #print testNode.get_leaves()
    #print testNode4.build_path()

    print testNode.leaf_names
    print testNode.child_name_date
    print testNode.name_date
    #print testNode.blah

