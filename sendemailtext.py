import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
 
fromaddr = "xiangnan.g12@gmail.com"
toaddr = ['xiangnan.g12@gmail.com']
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = ','.join(toaddr)
msg['Subject'] = "send email test"
 
body = "hello world"
msg.attach(MIMEText(body, 'plain'))
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "gxn910218")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
