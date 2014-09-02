import imaplib
import email.utils
import random
import string
from sendmail import send_email
from password import password
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.message import MIMEMessage


def parseemail(message):
    original = email.message_from_string((message[0][1]))
    for part in original.walk():
        if (part.get('Content-Disposition')
            and part.get('Content-Disposition').startswith("attachment")):

            part.set_type("text/plain")
            part.set_payload("Attachment removed: %s (%s, %d bytes)"
                         %(part.get_filename(), 
                           part.get_content_type(), 
                           len(part.get_payload(decode=True))))
            del part["Content-Disposition"]
            del part["Content-Transfer-Encoding"]
    
    new = MIMEMultipart("mixed")
    body = MIMEMultipart("alternative")
    body.attach( MIMEText("reply body text", "plain") )
    body.attach( MIMEText("<html>reply body text</html>", "html") )
    new.attach(body)

    new["Message-ID"] = email.utils.make_msgid()
    new["In-Reply-To"] = original["Message-ID"]
    new["References"] = original["Message-ID"]
    new["Subject"] = "Re: "+original["Subject"]
    new["To"] = original["Reply-To"] or original["From"]
    new["From"] = "cornellcscongratbot@gmail.com"

    tolist = [new["To"]]
    tolist = tolist + string.split(original["To"], ",")
    tolist = tolist + ([] if original["CC"] == None else original["CC"])
    isRepeat = repeatedCongratBot(tolist) 
    
    print "Is a repeat:"
    print isRepeat
    if (not(isRepeat)):
        print "sending emails"
        send_email(new["From"], tolist, new["Subject"], getMessage()+"\r\n \r\n --CS3110 Congrats Bot")

def repeatedCongratBot(tolist) :
    count = 0
    for email in tolist:
        if ("cornellcscongratbot" in email):
           count += 1
    if (count > 1):
        return True
    return False

def getMessage():
    congratFile = open('congratulations')
    lines = congratFile.readlines()
    numval = random.randint(0, len(lines)-1)
    toReturn = lines[numval] 
    print toReturn
    congratFile.close()
    return toReturn

def reademail():
    conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    conn.login("cornellcscongratbot@gmail.com", password)
    conn.select()

    typ, data = conn.search(None, 'UNSEEN')
    try: 
        for num in data[0].split():
            typ, msg_data = conn.fetch(num, '(RFC822)')
            parseemail(msg_data)
            for response_part in msg_data:
                msg = email.message_from_string(response_part[1])
                #if isinstance(response_part, tuple):
                    #print email.utils.parseaddr(msg['From'])
                    #print email.utils.parseaddr(msg['CC'])
    finally:
        conn.close()
        conn.logout()

reademail()
