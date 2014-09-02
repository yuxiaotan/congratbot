import password

def send_email(FROM, TO, SUBJECT, MESSAGE):
    if (not(isinstance(TO, list))) : 
        print "stopping"
        return

    import smtplib

    gmail_user = "congratbotcs3110@gmail.com"
    gmail_pwd = password.password

    print 'initiating mail send'
    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(TO), SUBJECT, MESSAGE)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.quit()
        server.close()
        print 'successfully sent the mail'
    except:
        print 'failed to send'
