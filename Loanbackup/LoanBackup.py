#Python Backup script for Loan files and Discovery Data

import os
import os.path
import TreeNode
import subprocess


def build_fromdir(searchroot):
    from hashlib import md5

    def _buildnodes(startnode, fullpath, moddate=0):
        wpath = fullpath.replace(searchroot, '').lstrip(os.sep)
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


def remove_children(folderlist, ref_table):
    '''removes folders from the set if their parents are also in the set'''
    def _check_parents(f):
        node = ref_table[f].Parent
        if node is None:
            return None  # bail if given the root node
        while node.Parent is not None:
            if node.pathhash in folderlist:
                return None
            node = node.Parent
        return f

    res = []
    for folder in folderlist:
        ret = _check_parents(folder)
        if ret is not None:
            res.append(ret)
    return res


def gen_changelist(basetree, comparetree):
    '''
    Takes two folder trees and generates the list of added, deleted, and changed
    folder paths between them.
    '''
    #store the map between the path hash and a ref to the tree node for later lookup
    base_ref_table = {}
    compare_ref_table = {}
    diffdate_folders = []

    base_visit = visit_closure(base_ref_table)
    compare_visit = visit_closure(compare_ref_table)
    basetree.df_traverse(base_visit)
    comparetree.df_traverse(compare_visit)

    base_folders = set(base_ref_table.iterkeys())
    compare_folders = set(compare_ref_table.iterkeys())
    new_folders = base_folders - compare_folders
    remove_folders = compare_folders - base_folders
    same_folders = base_folders & compare_folders

    new_folders = remove_children(new_folders, base_ref_table)
    remove_folders = remove_children(remove_folders, compare_ref_table)

    for folder in same_folders:
        datediff = abs(base_ref_table[folder].modDate - compare_ref_table[folder].modDate)
        if datediff > 5:
            diffdate_folders.append(folder)

    return [[base_ref_table[folder].build_path() for folder in new_folders],
            [compare_ref_table[folder].build_path() for folder in remove_folders],
            [base_ref_table[folder].build_path() for folder in diffdate_folders]]

def copy_newfolder(treepath, sourceroot, destroot):
    '''
    Performs the shell robocopy command to copy a new directory to the destination.
    treepath: path generated from the TreeNode operations. Starts with root
    sourceroot: Actual path on the local os to start from.
    destroot: Actual path on the local os to copy too.
    '''
    copy_from = os.path.join(sourceroot.strip(os.sep),
                             treepath.replace('root', '').strip(os.sep))
    copy_to = os.path.join(destroot.strip(os.sep),
                             treepath.replace('root', '').strip(os.sep))
    roboargs = [copy_from, copy_to, '/COPY:DAT', '/E', '/MT:8',
                '/W:1', '/R:5', '/NFL', 'NDL', '/NJH']
    proc = subprocess.Popen(roboargs, stdout=subprocess.PIPE, shell=True)
    out = proc.communicate()[0]
    return (out, proc.returncode)


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
