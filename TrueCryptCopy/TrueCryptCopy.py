import xlwt
import xlrd
import subprocess
import os

pwdfile = xlrd.open_workbook("RS Copy of NYDOCS04-#557736-v1-MDL_Reproduction_Password_Log.xls")
pwdList = pwdfile.sheet_by_name("Password Log")
dismount = '"C:\Program Files\TrueCrypt\TrueCrypt.exe" /dx /q /s'
argList = []

for row in range(1, pwdList.nrows):
    for value in pwdList.row_values(row, 0,5):
        argList.append(value.strip("u'"))
    #print argList
    for root, dirs, files in os.walk("F:\\"):
        if argList[2] + ".tc" in files or argList[2] + ".TC" in files:
            robocopy = 'robocopy X: "G:\%s\%s" /s /e /copy:dat /nfl /ndl /r:0 /w:0' % (argList[1], argList[4])
            truecrypt = '"C:\Program Files\TrueCrypt\TrueCrypt.exe" /q /v "' + os.path.join(root, argList[2]+".tc") + '" /lx /p %s /s"' % (argList[3])
            print truecrypt
            print robocopy
            subprocess.call(truecrypt)
            subprocess.call(robocopy)
            subprocess.call(dismount)
    argList = []

