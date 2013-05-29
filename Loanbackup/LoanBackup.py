#Python Backup script for Loan files and Discovery Data

import os
import TreeNode
import time
import sys
import cPickle as pickle
from collections import deque


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
    dirs = None
    try:
        dirs = [x for x in sorted(os.listdir(path))
                if os.path.isdir(os.path.join(path, x))
                and not os.path.islink(os.path.join(path, x))]
    except:
        e = sys.exc_info()[0]
        print e

    if dirs:
        for dirx in dirs:
            newpath = os.path.join(path, dirx)
            modTime = float(os.path.getmtime(newpath))
            newnode = node.newChild(dirx, modTime, newpath)
            build_tree(newnode, newpath)


def build_tree_bf(node, path):
    dirs = None
    queue = deque()

    queue.appendleft((node, path))

    while len(queue) > 0:
        qnode, qpath = queue.pop()
        dirs = None
        try:
            dirs = [x for x in sorted(os.listdir(qpath))
                    if os.path.isdir(os.path.join(qpath, x))
                    and not os.path.islink(os.path.join(qpath, x))]
        except:
            e = sys.exc_info()
            print e[1].message

        if dirs:
            for dirx in dirs:
                newpath = os.path.join(qpath, dirx)
                print newpath, newpath.count('/')
                modTime = float(os.path.getmtime(newpath))
                newnode = qnode.newChild(dirx, modTime, newpath)
                queue.appendleft((newnode, newpath))


if __name__ == '__main__':
    starttime = time.time()
    root = TreeNode.TreeNode('root')
    #c = itertools.count()
    build_tree_bf(root, sys.argv[1])
    ctime = '%d:%.1f' % divmod(time.time() - starttime, 60)
    print 'build complete', ctime

    #print len(root)
    def vf(x):
        print x.Fname, x.build_path()
    #root.df_traverse(vf)
    with open('treepickleBin', 'wb') as fh:
        pickle.dump(root, fh, protocol=2)
    ctime = '%d:%.1f' % divmod(time.time() - starttime, 60)
    print 'pickle complete', ctime