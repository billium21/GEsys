# -*- coding: utf-8 -*-
import TreeNode
import LoanBackup

if __name__ == '__main__':
    import sys
    import time
    import cPickle as pickle

    starttime = time.time()
    with open(sys.argv[1], 'rb') as fh:
        base = pickle.load(fh)

    with open(sys.argv[2], 'rb') as fh2:
        compare = pickle.load(fh2)

    LoanBackup.gen_changelist(base, compare)

    ctime = '%d:%.1f' % divmod(time.time() - starttime, 60)
    print 'complete', ctime
