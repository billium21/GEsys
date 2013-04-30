#Sandbox Python Script. Play with Python

import zipfile
import imaplib
import email
from HTMLParser import HTMLParser

d = []
lineCount = 0
count = 0


def convert(data):
    num = 0
    result = ""
    if data.rfind("TB") > -1:
        num = float(data.strip("TB,"))
        num = round((num * 1024), 3)
        result = str(num) + " GB,"
    elif data.rfind("MB") > -1:
        print data
        num = float(data.strip("MB,"))
        num = round((num / 1024), 3)
        result = str(num) + " GB,"
    else:
        return data
    return result


class ReportParser(HTMLParser):
    """
    Report parser: HTMLParser with a few overridden handlers
    """
    def __init__(self):
        super(ReportParser, self).__init__()

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
                r.write(output + "\n")
                count = 0
            else:
                output += ","
                count += 1
                r.write(convert(output))


#mail server fetching
mail = imaplib.IMAP4_SSL("xxxxxxxx")  # Establishes Exchange server connection
mail.login("xxxxxx", "xxxxxxx")
mail.select("inbox")
typ, data = mail.search(None, '(From "Thomas Alberi")')
mailList = data[0]
text = mailList.split()
for latest_msg in text:
    typ, msg = mail.fetch(latest_msg, '(RFC822)')
    msgtext = email.message_from_string(msg[0][1])
    if msgtext.is_multipart():
        #print 'multipart'
        for part in msgtext.walk():
            ctype = part.get_content_type()
            #print ctype
            if ctype == 'application/x-gzip':
                #print "done"
                open(part.get_filename(), 'wb').write(part.get_payload(decode=True))
                d.append(part.get_filename())

p = ReportParser()
for s in iter(d):
    files = zipfile.ZipFile(s)  # Fetches the name of the .zip attachment
    for f in files.namelist():  # Search the archive for the HTML file
        if f.rfind(".html") > -1:

            #Open the HTML file and create a CSV file with the same name

            i = files.open(f, "r")
            r = open("CSVDump\\" + f.replace(".html", ".csv"), "w")

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
            lineCount = 0
