

import zipfile
import imaplib
import email
import os
import sys
import datetime
from itertools import ifilter
from cStringIO import StringIO
from HTMLParser import HTMLParser, HTMLParseError


d = []
lineCount = 0
count = 0
date = ""




def convert(data):
    if 'TB' in data:
        num = float(data.strip("TB,"))
        num = round((num * 1024), 3)
        return str(num) + ","
    elif 'MB' in data:
        #print data
        num = float(data.strip("MB,"))
        num = round((num / 1024), 3)
        return str(num) + ","
    elif 'GB' in data:
        num = float(data.strip("GB,"))
        num = round(num, 3)
        return str(num) + ","
    elif 'bytes' in data:
        return data.strip("bytes,")
    else:
        return data


def mod_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


class ReportParser(HTMLParser):
    """
    Report parser: HTMLParser with a few overridden handlers


    def __init__(self):
        super(ReportParser, self).__init__()
    """
    def handle_data(self, data):
        global output
        global count
        if data not in ["\n", " ", " \n"]:
            output += data


        #every row has 7 elements, so each line of output should have 6 commas,
        #one between each of the 7 fields. Each column endtag results in a comma
        #except for the last one in each row. Since the very last row only has 6 fields,
        #the lineCount keeps track of when the table ends so the last line doesn't have the
        #trailing comma which could throw off the Excel export


    def handle_starttag(self, tag, attrs):
        if tag == "tr" and ('class', "fc1") in attrs:
            CSV.write(date + ",")
        elif tag == "tr" and ('class', "fc2") in attrs:
            CSV.write(date + ",")
        elif ('class', "fc3") in attrs:
            self.error("End File")


    def handle_endtag(self, tag):
        global output
        global count
        #global date
        if tag == "td" or tag == "th":
            if count == 6: 
                CSV.write(convert(output) + "\n")
                count = 0
            else:
                output += ","
                count += 1
                CSV.write(convert(output))




#mail server fetching
mail = imaplib.IMAP4_SSL("XXX")  # Establishes Exchange server connection
mail.login("DataGathering", "XXXX")
mail.select("Inbox")
typ, data = mail.search(None, 'ALL')
msgidlist = ','.join(data[0].split())
#text = mailList.split()
#for latest_msg in text:
typ, allmsgs = mail.fetch(msgidlist, '(RFC822)')


# fanciness to filter out the flags strings, every other item on the list.
for msg in ifilter(lambda x: isinstance(x, tuple), allmsgs):
    msgtext = email.message_from_string(msg[1])
    if msgtext.is_multipart():
        #print 'multipart'
        #print mail.list()
        for part in msgtext.walk():
            ctype = part.get_content_type()
            #print ctype
            if ctype == 'application/x-gzip':
                print "done", msg[0]
                #open(part.get_filename(), 'wb').write(part.get_payload(decode=True))
                memfile = StringIO()
                memfile.write(part.get_payload(decode=True))
                d.append((part.get_filename(), memfile))  # push file name on list with file


mail.copy(msgidlist, "Inbox/Processed")
mail.store(msgidlist, '+FLAGS', '\\Deleted')
mail.expunge()
mail.logout()


print "beginning zip processing"


os.system('C:\Python27\Data Gathering\netDriveMap.bat')
CSV = open("P:\\Administrative\\IT\\Logging\\Logging.csv", "a")


for fname, zfile in iter(d):
    files = zipfile.ZipFile(zfile)  # Fetches the name of the .zip attachment
    
    for f in files.namelist():  # Search the archive for the HTML file
        if f.rfind(".html") > -1:


            #Open the HTML file and create a CSV file with the same name
            p = ReportParser()
            i = files.open(f, "r")


            rawDate = files.getinfo(f).date_time
            date = str(rawDate[1])+"-"+str(rawDate[2])+"-"+str(rawDate[0])
            
            #All of the report files are exactly
            #the same, save for the data in them. The table with the information
            #starts and ends on the same line in every HTML file, which is why
            #hard-coding the line location in the data works.


            for line in i:
                output = ""
                lineCount += 1
                try:
                    if lineCount in xrange(87, 500):p.feed(line)
                except HTMLParseError:
                    break
            i.close()
            lineCount = 0
            count = 0
    files.close()
CSV.close()
