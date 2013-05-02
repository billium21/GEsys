#Sandbox Python Script. Play with Python

import zipfile
import imaplib
import email
import os
from HTMLParser import HTMLParser

d = []
lineCount = 0
count = 0


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
    else:
        return data


class ReportParser(HTMLParser):
    """
    Report parser: HTMLParser with a few overridden handlers

    def __init__(self):
        super(ReportParser, self).__init__()
    """
    def handle_data(self, data):
        global output
        if data not in ["\n", " ", " \n"]:
            output += data

        #every row has 7 elements, so each line of output should have 6 commas,
        #one between each of the 7 fields. Each column endtag results in a comma
        #except for the last one in each row. Since the very last row only has 6 fields,
        #the lineCount keeps track of when the table ends so the last line doesn't have the
        #trailing comma which could throw off the Excel export

    def handle_endtag(self, tag):
        global output
        global count
        if tag == "td" or tag == "th":
            if count == 6 or lineCount == 435:
                r.write(convert(output) + "\n")
                count = 0
            else:
                output += ","
                count += 1
                r.write(convert(output))


#mail server fetching
mail = imaplib.IMAP4_SSL("10.154.128.22")  # Establishes Exchange server connection
mail.login("DataGathering", "DGmail123!")
mail.select("Inbox")
typ, data = mail.search(None, 'ALL')
mailList = data[0]
text = mailList.split()
for latest_msg in text:
    typ, msg = mail.fetch(latest_msg, '(RFC822)')
    msgtext = email.message_from_string(msg[0][1])
    if msgtext.is_multipart():
        #print 'multipart'
        #print mail.list()
        for part in msgtext.walk():
            ctype = part.get_content_type()
            #print ctype
            if ctype == 'application/x-gzip':
                #print "done"
                open(part.get_filename(), 'wb').write(part.get_payload(decode=True))
                mail.copy(latest_msg, "Inbox/Processed")
                mail.store(latest_msg, '+FLAGS', '\\Deleted')
                d.append(part.get_filename())
                mail.expunge()

p = ReportParser()
for s in iter(d):
    files = zipfile.ZipFile(s)  # Fetches the name of the .zip attachment
    for f in files.namelist():  # Search the archive for the HTML file
        if f.rfind(".html") > -1:

            #Open the HTML file and create a CSV file with the same name

            i = files.open(f, "r")
            r = open("P:\\Administrative\\IT\\Logging\\" + f.replace(".html", ".csv"), "w")

            #All of the report files are exactly
            #the same, save for the data in them. The table with the information
            #starts and ends on the same line in every HTML file, which is why
            #hard-coding the line location in the data works.

            for line in i:
                lineCount += 1
                if lineCount in xrange(70, 436):
                    output = ""
                    p.feed(line)
            r.close()
            i.close()
            lineCount = 0
    files.close()
    os.remove(s)
