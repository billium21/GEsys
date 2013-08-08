# -*- coding: utf-8 -*-
import TreeNode
import cPickle as pickle

with open('pickle2.bin', 'rb') as fh:
    root = pickle.load(fh)

print len(root)
def vf(x):
        print x.build_path(), x.depth, x.pathhash
root.df_traverse(vf)