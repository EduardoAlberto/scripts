# imports for sending email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

txt = 'teste'

# we will built the message using the email library and send using smtplib
msg = MIMEMultipart()
msg['Subject'] = "Automated customer report"  # set email subject
msg.attach(MIMEText(txt))  # add text contents
       
# we will send via outlook, first we initialise connection to mail server
smtp = smtplib.SMTP('smtp-mail.outlook.com', '587')
smtp.ehlo()  # say hello to the server
smtp.starttls()  # we will communicate using TLS encryption
       
# login to outlook server, using generic email and password
smtp.login('***********@outlook.com', '*****************')

# send email to our boss
smtp.sendmail('***********@outlook.com', '***********@outlook.com', msg.as_string())

# finally, disconnect from the mail server
smtp.quit()
  