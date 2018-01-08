#!/usr/bin/env python3
# encoding: utf-8

import os
import smtplib
import emaildata
import emailconfig
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def main(): 
    
    for recipientdata in emaildata.getRecipients():        
        recipientemail = recipientdata[0]
        subject = emailconfig.SUBJECT if recipientdata[1] == '' else recipientdata[1]
        composed = getComposed(recipientemail, subject);
        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(emailconfig.SENDER, emailconfig.GMAIL_PASSWORD)
                smtp.sendmail(emailconfig.SENDER, recipientemail, composed)
                smtp.close()
            print("Email sented! "+recipientemail)
        except:
            print("Unable to send the email. Error: ", sys.exc_info()[0])
            raise

def getComposed(recipientemail, subject):

    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['To'] = recipientemail
    outer['From'] = emailconfig.SENDER
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    body = emaildata.getEmailBody();
    outer.attach(MIMEText(body, 'plain'))
    
    # Add attachments 
    for file in emaildata.getAttachments():
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise

    return outer.as_string()


if __name__ == '__main__':
    main()