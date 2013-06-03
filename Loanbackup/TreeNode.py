# TreeNode Class
import os
#from __future__ import print_function

class TreeNode:

    """
    modDate will be used to compare the files in the backup to the files in the
    original locations. It will be a floating point number representing the number
    of seconds since the new epoch, because that's how os.path.getmtime does it.
    """

    def __init__(self, Fname, modDate=0, fullpath=None):
        self.Parent = None
        self.Fname = Fname
        self.modDate = modDate
        self.leafNode = True
        self.lChild = []
        self.fullpath = fullpath

    def newChild(self, Fname, modDate=0, fullpath=None):
        newChild = TreeNode(Fname, modDate, fullpath)
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
        elif name is 'child_names':
            return [child.Fname for child in self.lChild]
        elif name is 'name_date':
            return (self.Fname, self.modDate)
        elif name is 'count':
            return self._count_nodes()
        else:
            raise AttributeError('%s not a valid attribute' % name)

    def __len__(self):
        return self._count_nodes()

    def build_path(self):
        if self.Parent:
            #return self.Parent.build_path() + self.Fname + os.sep
            return ''.join((self.Parent.build_path(), self.Fname, os.sep))
        else:
            return ''.join((self.Fname, os.sep))

    #Depth-first traverse the tree and call visit function on each node.
    #@profile
    def df_traverse(self, visit_func, marked=None):
        if marked is None:
            marked = {}
        marked[self] = None
        visit_func(self)
        for child in self.lChild:
            if child not in marked:
                child.df_traverse(visit_func, marked)

    #@profile
    def _count_nodes(self):
        from itertools import count
        ct = count()
        self.df_traverse(lambda x: next(ct))
        return next(ct)


if __name__ == '__main__':

    testNode = TreeNode("Test")
    testNode2 = testNode.newChild("Test2")
    testNode3 = testNode.newChild("Test3")
    testNode4 = testNode3.newChild("Test4")
    testNode5 = testNode2.newChild("Test5")

    #print testNode.lChild
    ##testNode.newChild("tChild1")
    ##testNode.newChild("tChild2")
    ##testNode.newChild("tChild3")
    ##
    ##testNode.list_Chldrn()
    ##print testNode3.build_path()
    #print testNode.get_leaves()
    print testNode4.build_path(), '\n'

    def vf(x):
        print x.build_path()
    testNode.df_traverse(vf)
