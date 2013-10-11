import hashlib
import subprocess
import os


#This assumes that the two directories supplied are supposed
#to be copies of each other
#source = raw_input("Source Directory: ")
#backup = raw_input("Backup Directory: ")

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

def DirCompare(source, backup):
    
    #Build Dictionaries of MD5 hashes
    sourcetag = hashtag(source)
    backuptag = hashtag(backup)


    #look for matching MD5's.
    mismatch = []
    matchlog = open("MatchLog.txt", "w")
    for key in sourcetag.keys():
        if key not in backuptag.keys():
            mismatch.append(sourcetag[key])
        else:
            matchlog.write(sourcetag[key] + " MATCH")

    if len(mismatch) > 0:
        print str(len(mismatch)) + " mismatches!"
        for x in mismatch:
            print x
    else:
        print source + " equals " + backup

    print "DONE! Match Log created in program directory. Move it out as the next compare will overwrite it!"
