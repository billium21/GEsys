#Python Backup script for Loan files and Discovery Data

import os
import TreeNode


def build_fromdir(searchroot):
    import subprocess
    from hashlib import md5

    def _buildnodes(startnode, fullpath, moddate=0):
        wpath = fullpath.replace(searchroot, '')
        depth = wpath.count(os.sep)
        pathhash = md5(wpath).hexdigest()
        folders = [x for x in wpath.split(os.sep) if x != '']
        for folder in folders:
            if folder in startnode.child_names:
                startnode = [x for x in startnode.lChild if x.Fname == folder][0]
            else:
                startnode = startnode.newChild(Fname=folder,
                                               modDate=moddate,
                                               depth=depth,
                                               pathhash=pathhash)

    root = TreeNode.TreeNode('root', pathhash=md5('root').hexdigest())
    proc = subprocess.Popen(['dir', searchroot, '/A:D', '/S', '/B'],
                            shell=True, stdout=subprocess.PIPE, bufsize=1)
    for line in iter(proc.stdout.readline, b''):
        line = line.strip()
        if os.path.isdir(line):
            moddate = float(os.path.getmtime(line))
            _buildnodes(root, line, moddate)
    proc.communicate()
    return root

def visit_closure(ref_table):
    '''
    Closure to generate the visit function for tree traversal.  Allows for dict passing to the
    visit func.  The dict will store the reference table.
    '''
    def add_refs(node):
        ref_table[node.pathhash] = node
    return add_refs


def gen_changelist(basetree, comparetree):
    '''
    Takes two folder trees and generates the list of added, deleted, and changed
    folders between them.
    '''
    base_ref_table = {}
    compare_ref_table = {}

    base_visit = visit_closure(base_ref_table)
    compare_visit = visit_closure(compare_ref_table)
    basetree.df_traverse(base_visit)
    comparetree.df_traverse(compare_visit)

    import pprint as pp
    pp.pprint(base_ref_table)
    print '=' * 80
    pp.pprint(base_ref_table)



if __name__ == '__main__':
    import time
    import sys
    import cPickle as pickle

    starttime = time.time()
    root = build_fromdir(sys.argv[1])
    ctime = '%d:%.1f' % divmod(time.time() - starttime, 60)
    print 'build complete', ctime

    #print len(root)
    def vf(x):
        print x.build_path(), x.depth, x.pathhash
    #root.df_traverse(vf)
    with open(sys.argv[2], 'wb') as fh:
        pickle.dump(root, fh, protocol=2)

    ctime = '%d:%.1f' % divmod(time.time() - starttime, 60)
    print 'complete', ctime