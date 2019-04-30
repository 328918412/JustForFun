#!/usr/bin/env python3


from email.mime.text import MIMEText
from email.header import Header
import smtplib
import sys
from admin import *

"""
Get configuration from admin module.
"""
from_addr=FROM
password=PASSWD
to_addr=TO
smtp_server=SMTP
server_port=PORT

""" 
Set msg's From,To,Subject,Context.
"""
msg=MIMEText(("网站: %s 无法访问了。时间:%s" % (sys.argv[1],sys.argv[2])),"plain","utf-8")
msg['From']=from_addr
msg['To']=to_addr
msg['Subject']=Header("网站可用性监控",'utf-8').encode()

"""
Login to smtp server then  send e-mail.
"""
server=smtplib.SMTP(smtp_server,25)
server.set_debuglevel(1)
server.login(from_addr,password)
server.sendmail(from_addr,[to_addr],msg.as_string())
server.quit()
