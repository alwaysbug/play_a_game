import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart

sender = "***"
receive = "***"
passwd = "***"
mailserver = "smtp.126.com"
port = '25'
sub = "__对冲模型__"

class Mail(object):
    @classmethod
    def send(cls, text):
        try:
            msg = MIMEMultipart("related")
            msg['Form'] = formataddr(["sender", sender])
            msg['To'] = formataddr(["receiver", receive])
            msg["Subject"] = sub
            txt = MIMEText(text, 'plain', 'utf-8')
            msg.attach(txt)

            server = smtplib.SMTP(mailserver, port)
            server.login(sender, passwd)
            server.sendmail(sender, receive, msg.as_string())
            server.quit()
        except Exception as e:
            print(e)
