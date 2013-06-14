import os
import shutil
import re

indir = "C:\\Python27\\WikiExports\\test" #raw_input("Enter Input Directory: ")
Bates = raw_input("Starting bates number? ")
outFile = open(indir + "_export.dat", "a")
dst = "C:\Python27\WikiExports\dataDumps"
header = '"BEGBATES"|"ENDBATES"|"BEGATTACH"|"ENDATTACH"|\
"REVIEWTOOL_ID"|"TO"|"FROM"|"CC"|"BCC"|"TITLE"|"AUTHOR"|\
"DATE"|"DOCEXT"|"Path"|"Offensive Comments"|\
"Update Offensive Comments"|"Defensive Comments"|\
"Update Defensive Comments"|"PRODUCEDBY"|"CUSTODIAN"|"COC"|"Docs_PATH"\n'


def batesSplit(Bates):
    result = ""
    letters = ""
    setaB = list(Bates)
    setaB.reverse()
    print setaB
    for c in setaB:
        try: int(c)
        except ValueError:
            num = setaB.index(c)
            digits = setaB[:num]
            Bates = setaB[num:]
            digits.reverse()
            Bates.reverse()
            for i in digits:
                result += i
            for c in Bates:
                letters += c
            break
    return (letters, result)
            
print Bates
outFile.write(header)
for root, dirs, files in os.walk(indir):
    for File in files:
        dataList = []
        shutil.copy(os.path.join(root, File), dst)
        for i in range(0,4):
            dataList.append(Bates)
        Bates = batesSplit(Bates)[0] + str(int(batesSplit(Bates)[1]) +1).zfill(len(batesSplit(Bates)[1]))
        line = ''
        print dataList
        for data in dataList:
            line += str(data) + '|'
        #For now, this loop and the one after it just fill in placeholders
        #for the other data in the export. All we can get is the file path
        for i in range(0, 5):
            line += '""|'
        line += File.split(".")[0] + '|""|""|""|'
        line += os.path.join(root, File) #file path
        for i in range(0,10):
            line += '""|'
        print line.rstrip("|")
        outFile.write(line.rstrip("|") + "\n")

outFile.close()

