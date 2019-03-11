#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/3/11 11:32
# @Author  : tchua
# @Email   : tchuaxiaohua@163.com
# @File    : 00.py
# @Software: PyCharm
import requests
from email.mime.text import MIMEText
from email.header import Header
import smtplib


url = 'http://www.tchua.com.cn'

def get_server_status(url):
    res = requests.head(url)
    if res.status_code != 200:
        message = "{} is error".format(url)
        return message

msg = MIMEText(get_server_status(url),'plain','utf-8')

msg['Subject'] = Header("ONE平台监控",'utf-8')
msg['From'] = Header('tchuaxiaohua@163.com')
msg['To'] = Header('运维组','utf-8')

from_addr = 'tchua@163.com'    #发件邮箱(发件人)
password = '******'			   #邮箱客户端授权码(注：非邮箱密码)
to_addr = 'tchua@qq.com'	   #接收邮箱(接收人)

smtp_server = 'smtp.163.com'   


try:
    #server = smtplib.SMTP(smtp_server)
    server = smtplib.SMTP_SSL(smtp_server,994)
    server.login(from_addr,password)
    server.sendmail(from_addr,to_addr,msg.as_string())
    server.quit()
except smtplib.SMTPException as e:
    print("邮件发送失败",e)