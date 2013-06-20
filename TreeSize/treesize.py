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
    def jsonnode(node, spacing=10):
        tokens = []
        tokens.append('{"label":"%s"' % (node.Fname.ljust(spacing, '-')
                                         + datasize_str(node.datasize)))
        if not node.leafNode:
            maxlen = max([len(name.Fname) for name in node.lChild])
            tokens.append(',"children":[')
            for child in sorted(node.lChild, key=lambda x: x.Fname.lower()):
                tokens.append(jsonnode(child, maxlen + 5))
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
    import bz2
    import base64

    b64template = """
        QlpoOTFBWSZTWUUWzE4AAWBfgEQwfvf//79G3CC////6UAWYMy9d27FQZl3a1tznCSQRMmjRkCm1
        PTEnoj9UPKPRHqaZlNA0ekPUEkmk2om0pPZU9IaeTTSDQ00eoBoMgAbUAk1IUnpTyNTGoABtTQAD
        QDRoAADmmRkMmCGjCYI00aMQNMmRgACCSEQBU9qZkmapkAYjQyGQGIGgGi4SWYb0ZAlTEhAEgQQG
        BAFRFCSf06utKBJSVKKpVBjTRBWKILFjVSUnFgD/IsDWx2U4IRG9TK7RRe5IWJZM4SSTELMJAcB/
        OBSZRY8OycHUuBo9giff81NwNJmNLpQ32AcdVYtQQyVmJl00W2IQqsYcYY3hX77qUZdX9ygqCvEz
        Bk2DscRbTNMLN9oNvI+DdfO76LpzY5uaUTgGobWWW8UCyoLGBmCzV0Y1G1x4+u/pdxpCqbsxU48k
        F0aiwWEWEootryTKp3NR3a5w95XPb5Y1PBGcYUUwDPTk9krAaWvtvjeotTWWlC4TJJRGrUMZt3L+
        Mx1bxK5EAXREDCwATsr5cY+XEKkXCT7efAi5ZY6tNNCMNCqueRa5JSGXqQw7ykDMG0HDlgu1ewhE
        zxLM7e1KMo3acaD9W90aMZm1uQOGe0ljTyOaUjpFuuBFXZE/gGnpZLmsZnhp5Z4Z9ksjOhUc8LjJ
        mTRRyjPxKHtC5OwVu89lHtalCwZ+PMRPpw3cjMvlHishoU6o45IwiIpZmayHiuY+j0uQTs8M4VNb
        xTSxMxceOi0ptf7Fflk4bu3OOcMVwHHg3XFwPk/hSs7b5zB9IZup0Ze0aOu2E69NppnbAsDz2BsW
        wPzs+93x+APDSG8Ktx4rip/KOj9rB/pcQZjwbRMHXAREcoJbdrt5z8HyWfMr7EW8TItEdpNC4ZDL
        lJ9iHR/vhyCKSgM1VMWGIDgovVBWOgP7AYRAlgDIZuHIN6C86Jj2MiBD1lym6hbhahmokGpUIdYY
        S0S0WBBclp+zgrWTXp63cSITJAOzMqUTUpa8Y3Spjdih3oUBuWBmRMGmdQ5KoyVQCRIRJDkGCOWa
        NqwBig7NGgocTMNaWy0qqiYbwXLY7HJmiSgToxEfXIWG02qpGpKQjZvzdSiYdQj3cOuUpZI0u8qL
        Expej7ESS5yevUCxTO1vBUoDo4AjsswRC3rovQTadiDS9ynvmi4C9B3ThrsmQ6gxlF9KdE0qHGZH
        KKyLKNSZmQJOGOUJxLqKn6UhMshWjCpaV3Oa+z2aqEphOcyMwzPRFQBY5q0hXZOnM4UAvTBsTJVl
        YI03zROtVoyuDINMw7VyzKgUDShqTNIWpgxJvMzwawCQmcfCvvy1SzBtIypsNq2YgMG7RDAwaQvA
        qECjGEG/MMALDAVXTJaUOLARGUy/BjBBcNQrUbA1GUI12ksqRYoPv7husbo55O9qbv2b1jFr3Hd8
        Mkk0at0KhSxhQFJQa+bmGC14m4VCq1oBHoYWRUNchOb6Dub94hyywIvM5jLPC8CotiuWCfZnmlNZ
        7grrHXibBDDQCOrI29vXs3N+0exLWajDlMflUvKmDoKoiI1cWvWk5S4AxkhosWUK8FNF6Z6Vaqrp
        IIuzM0iyI6U+lfpoEUkam2pIVFWt4W6kYy7iCa6oPlWUBSUbahEYla4gli0FUJyDSxcVQtWYUBSb
        0AKHDRtWu9UozIAlfa1YZpCv5jNxC60C8uDmvQgV7f8XckU4UJBFFsxO
        """

    try:
        pathroot = sys.argv[1]
        outfile = sys.argv[2]
        totalspace = int(sys.argv[3])
    except:
        print """
        Incorrect arguments.  Must be three positional args. Last must be an integer.
        """
        sys.exit(0)

    root = TreeNode.TreeNode('root')
    root.datasize = 0
    root.fileflag = False
    build_tree_bf(root, pathroot)
    rollup_sizes(root)

    sub = {}
    sub['summary'] = '{} of {} used, {}%'.format(datasize_str(root.datasize),
                                          datasize_str(totalspace),
                                          round(float(root.datasize) /
                                                float(totalspace) * 100, 1))
    sub['json'] = jsontree(root)
    sub['timestamp'] = 'Generated: %s' % time.ctime()

    template = bz2.decompress(base64.decodestring(b64template))

    with open(sys.argv[2], 'w') as fh:
        fh.write(template.format(**sub))
