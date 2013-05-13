#Python Backup script for Loan files and Discovery Data

import os

def infoCollect():
    modTimes = {}
    print "Start getting Directory Mod times..."
    for root, dirs, files in os.walk("C:\\"):
        for name in dirs:
             modTimes[name] = float((os.path.getmtime(os.path.join(root, name))))
             print str(modTimes) + "\n"
    print str(len(modTimes)) + " Directories found"
    return modTimes

def infoCheck(modTimes):
    for root, dirs, files in os.walk("Path"):
        pass

infoCollect()
