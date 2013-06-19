# -*- coding: utf-8 -*-
import os
import TreeNode
from collections import deque

#@profile
def build_tree_bf(node, searchpath):
    queue = deque()
    queue.appendleft((node, searchpath))

    while len(queue) > 0:
        qnode, qpath = queue.pop()
        dirs = None
        try:
            dirlisting = sorted(os.listdir(qpath))
            dirs = [x for x in dirlisting
                    if os.path.isdir(os.path.join(qpath, x))
                    and not os.path.islink(os.path.join(qpath, x))]
            files = [x for x in dirlisting
                    if os.path.isfile(os.path.join(qpath, x))
                    and not os.path.islink(os.path.join(qpath, x))]

            for filex in files:
                newpath = os.path.join(qpath, filex)
                depth = newpath.replace(searchpath, '').count(os.sep)
                fsize = os.path.getsize(newpath)
                newnode = qnode.newChild(filex, depth=depth)
                newnode.datasize = fsize
                newnode.fileflag = True
        except:
            e = sys.exc_info()
            print e[1].message

        if dirs:
            for dirx in dirs:
                newpath = os.path.join(qpath, dirx)
                depth = newpath.replace(searchpath, '').count(os.sep)
                newnode = qnode.newChild(dirx, depth=depth)
                newnode.datasize = 0
                newnode.fileflag = False
                queue.appendleft((newnode, newpath))


#@profile
def rollup_sizes(node):
    leaflist = []

    def collectleaves(visitnode):
        if visitnode.leafNode:
            leaflist.append(visitnode)

    node.df_traverse(collectleaves)

    for treenode in leaflist:
        ds = treenode.datasize
        while treenode.Parent is not None:
            treenode.Parent.datasize += ds
            treenode = treenode.Parent

def jsontree(rootnode):
    def jsonnode(node):
        tokens = []
        tokens.append('{"label":"%s"' % node.Fname)
        if not node.leafNode:
            tokens.append(',"children":[')
            for child in sorted(node.lChild, key=lambda x: x.Fname.lower()):
                tokens.append(jsonnode(child))
                tokens.append(',')
            tokens.pop()  # remove the trailing comma
            tokens.append(']')
        tokens.append('}')
        return ''.join(tokens)

    return '[%s]' % jsonnode(rootnode)


def datasize_str(datasize):
    ln = len(str(datasize))
    if ln > 9:
        return '%s GB' % round(datasize / (1024.0**3), 2)
    elif ln <= 9 and ln > 6:
        return '%s MB' % round(datasize / (1024.0**2), 2)
    else:
        return '%s KB' % round(datasize / 1024.0, 2)

if __name__ == '__main__':
    import sys
    import time
    starttime = time.time()
    root = TreeNode.TreeNode('root')
    root.datasize = 0
    root.fileflag = False
    build_tree_bf(root, sys.argv[1])
    ctime = '%d:%.1f' % divmod(time.time() - starttime, 60)
    print 'build complete', ctime
    rollup_sizes(root)
    ctime = '%d:%.1f' % divmod(time.time() - starttime, 60)
    print 'rollup complete', ctime

    print len(root)
    #print datasize_str(root.datasize)
    xx = jsontree(root)

    def vf(x):
        print x.build_path(), x.datasize, x.depth

    #root.df_traverse(vf)

    ctime = '%d:%.1f' % divmod(time.time() - starttime, 60)
    print 'all complete', ctime