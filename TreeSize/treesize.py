# -*- coding: utf-8 -*-
import os
import TreeNode
from collections import deque


def build_tree_bf(node, searchpath):
    #from itertools import count
    #cnt = count()
    dirs = None
    queue = deque()
    depth = 1

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
                #if next(cnt) % 1000 == 0:
                    #print cnt, newpath
                queue.appendleft((newnode, newpath))


#@profile
def rollup_sizes(node):
    import heapq
    leaflist = []
    tracking = {}
    heap = []

    def collectleaves(visitnode):
        if visitnode.leafNode:
            leaflist.append(visitnode)

    node.df_traverse(collectleaves)
    leaflist = sorted(leaflist, key=lambda x: x.depth)
    #print '; '.join([str((x.Fname, x.depth)) for x in leaflist])
    queue = deque(leaflist)

    while len(queue) > 0:
        currnode = queue.pop()
        if currnode.Parent is not None:
            currnode.Parent.datasize += currnode.datasize
            #if currnode.Parent not in queue:
            if currnode.Parent not in tracking:
                tracking[currnode.Parent] = None
                #queue.appendleft(currnode.Parent)
                heapq.heappush(heap, (10000 - currnode.Parent.depth, currnode.Parent))

    while len(heap) > 0:
        dp, currnode = heapq.heappop(heap)
        if currnode.Parent is not None:
            currnode.Parent.datasize += currnode.datasize
            if currnode.Parent not in tracking:
                tracking[currnode.Parent] = None
                heapq.heappush(heap, (10000 - currnode.Parent.depth, currnode.Parent))

    #for treenode in leaves:
        #while treenode.Parent is not None:
            #treenode.Parent.datasize += treenode.datasize
            #treenode = treenode.Parent


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
    print root.datasize

    def vf(x):
        print x.build_path(), x.datasize, x.depth

    #root.df_traverse(vf)

    ctime = '%d:%.1f' % divmod(time.time() - starttime, 60)
    print 'all complete', ctime