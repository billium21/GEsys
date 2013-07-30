#Python Backup script for Loan files and Discovery Data

import os
import TreeNode
import time
import sys
import cPickle as pickle


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

    root = TreeNode.TreeNode('root')
    proc = subprocess.Popen(['dir', searchroot, '/A:D', '/S', '/B'],
                            shell=True, stdout=subprocess.PIPE, bufsize=1)
    for line in iter(proc.stdout.readline, b''):
        line = line.strip()
        if os.path.isdir(line):
            moddate = float(os.path.getmtime(line))
            _buildnodes(root, line, moddate)
    proc.communicate()

    return root


if __name__ == '__main__':
    starttime = time.time()
    root = build_fromdir(sys.argv[1])
    ctime = '%d:%.1f' % divmod(time.time() - starttime, 60)
    print 'build complete', ctime

    print len(root)
    def vf(x):
        print x.build_path(), x.depth, x.pathhash
    #root.df_traverse(vf)
    with open('treepickleBin', 'wb') as fh:
        pickle.dump(root, fh, protocol=2)
    ctime = '%d:%.1f' % divmod(time.time() - starttime, 60)
    print 'pickle complete', ctime