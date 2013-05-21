#Python Backup script for Loan files and Discovery Data

import os
import TreeNode
import time
import sys


def infoCollect():
    modTimes = {}
    print "Start getting Directory Mod times..."
    for root, dirs, files in os.walk("C:\\"):
        for name in dirs:
            modTimes[name] = float((os.path.getmtime(os.path.join(root, name))))
            print str(modTimes) + "\n"
    print str(len(modTimes)) + " Directories found"
    return modTimes


def infoCheck(modTimes):
    for root, dirs, files in os.walk("Path"):
        pass

#infoCollect()

#@profile
def build_tree(node, path):
    dirs = [x for x in sorted(os.listdir(path))
            if os.path.isdir(os.path.join(path, x))
            and not os.path.islink(os.path.join(path, x))]

    for dir in dirs:
        newnode = node.newChild(dir)
        newpath = os.path.join(path, dir)
        build_tree(newnode, newpath)

if __name__ == '__main__':
    starttime = time.time()
    root = TreeNode.TreeNode('root')
    #c = itertools.count()
    build_tree(root, sys.argv[1])
    ctime = '%d:%.1f' % divmod(time.time() - starttime, 60)
    print 'build complete', ctime

    #print len(root)
    #root.df_traverse(vf)
    ctime = '%d:%.1f' % divmod(time.time() - starttime, 60)
    print 'trav complete', ctime