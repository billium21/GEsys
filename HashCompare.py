import hashlib
import subprocess
import os

source = raw_input("Source Directory: ")
backup = raw_input("Backup Directory: ")

def hashtag(filename):
    result = {}
    proc = subprocess.Popen(['dir', filename, '/S', '/B', '/a:-d'],
                            shell=True, stdout=subprocess.PIPE, bufsize=1)
    for line in iter(proc.stdout.readline, b''): # do stuff to the file path line.  Process it or store it in a list.
        f = open(line.strip('\r\n'), 'rb')
        m = hashlib.md5()
        buf = f.read(65536)
        if len(buf) > 0:
            while len(buf) > 0:
                    m.update(buf)
                    buf = f.read(65536)
            result[m.hexdigest()] = line.strip('\r\n')
        else:
            result['NO DATA'] = line.strip('\r\n')
    proc.communicate()
    return result

sourcetag = hashtag(source)
backuptag = hashtag(backup)

mismatch = []
for key in source.keys():
    if key not in backup.keys():
        mismatch.append(source[key])
    else:
        print source[key] + " MATCH"

if len(mismatch) > 0:
    print len(mismatch) + " mismatches!"
    for x in mismatches:
        print x + "\n"
