# -*- coding: utf-8 -*-
import TreeNode
import folderops

if __name__ == '__main__':
    import sys
    import time
    import cPickle as pickle
    import pprint as pp

    starttime = time.time()
    with open(sys.argv[1], 'rb') as fh:
        base = pickle.load(fh)

    with open(sys.argv[2], 'rb') as fh2:
        compare = pickle.load(fh2)

    uptime = '%d:%.1f' % divmod(time.time() - starttime, 60)

    new, dell, diff = folderops.gen_changelist(base, compare)

    ctime = '%d:%.1f' % divmod(time.time() - starttime, 60)

    pp.pprint(new)
    print '=' * 50
    pp.pprint(dell)
    print '=' * 50
    pp.pprint(diff)
    print '=' * 50
    print '=' * 50
    print 'unpickle', uptime
    print 'complete', ctime
