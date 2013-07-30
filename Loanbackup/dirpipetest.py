# -*- coding: utf-8 -*-
import sys
import os.path
from hashlib import md5
import cStringIO
import subprocess

searchroot = sys.argv[1]
mode = sys.argv[2]


def build_fromdir(searchroot, mode):
    results = {}

    def procline(resdic, line):
        line = line.strip()
        if os.path.isdir(line):
            moddate = float(os.path.getmtime(line))
            resdic[md5(line).hexdigest()] = moddate

    if mode == 1:
        dirlist = cStringIO.StringIO()
        dirlist.write(subprocess.check_output(['dir', searchroot, '/A:D', '/S', '/B'], shell=True))
        dirlist.seek(0)

        def diriter():
            """helper function to generate a lazy iterator for the StringIO object"""
            return dirlist.readline()

        for line in iter(diriter, ''):
                line = line.strip()
                if os.path.isdir(line):
                    moddate = float(os.path.getmtime(line))
                    results[md5(line).hexdigest()] = moddate

    elif mode == 2:
        proc = subprocess.Popen(['dir', searchroot, '/A:D', '/S', '/B'],
                                shell=True, stdout=subprocess.PIPE)
        while proc.poll() is None:
            procline(results, proc.stdout.readline())
        procline(results, proc.communicate()[0])

    elif mode == 3:
        proc = subprocess.Popen(['dir', searchroot, '/A:D', '/S', '/B'],
                                shell=True, stdout=subprocess.PIPE, bufsize=1)
        for line in iter(proc.stdout.readline, b''):
            procline(results, line)
        proc.communicate()

    return results

if __name__ == '__main__':
    import sys
    import time

    starttime = time.time()
    res = build_fromdir(sys.argv[1], int(sys.argv[2]))
    ctime = '%d:%.1f' % divmod(time.time() - starttime, 60)
    print len(res)
    print ctime

