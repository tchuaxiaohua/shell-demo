#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/23 10:40
# @Author  : tchua
# @Email   : tchuaxiaohua@163.com
# @File    : send_mail_acc.py
# @Software: PyCharm
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from email.header import Header
import pay_bill
import pay_flow

def send_mail(subject,message,to_user,filename,filename2):

    msg = MIMEMultipart()
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = Header('tangchunhua@vanje.com.cn')
    msg['To'] = Header(to_user, 'utf-8')
    msg.attach(MIMEText(message, 'plain', 'utf-8'))
    ## 附件
    att1 = MIMEApplication(open(filename,"rb").read())
    att1.add_header("Content-Disposition", "attachment", filename=filename)
    msg.attach(att1)
    ## 附件2
    att2 = MIMEApplication(open(filename2,"rb").read())
    att2.add_header("Content-Disposition", "attachment", filename=filename2)
    msg.attach(att2)


    from_addr = 'tangchunhua@vanje.com.cn'  # 发件邮箱
    password = 'Tang!@#123'  # 邮箱密码(或者客户端授权码)
    to_addr = to_user  # 收件邮箱

    smtp_server = "smtp.mxhichina.com"  # 企业邮箱地址，若是个人邮箱地址为：smtp.163.com

    server = smtplib.SMTP_SSL(smtp_server, 465)  # 第二个参数为默认端口为25，这里使用ssl，端口为994
    server.login(from_addr, password)  # 登录邮箱
    server.sendmail(from_addr, to_addr, msg.as_string())  # 将msg转化成string发出
    server.quit()

if __name__ == '__main__':
    #send_mail("项目付款账单数据导出", "项目付款账单信息见附件，有问题及时联系，谢谢。", "471445404@qq.com", pay_bill.filename,pay_flow.filename2)
    send_mail("项目付款账单数据导出", "项目付款账单信息见附件，有问题及时联系，谢谢。", "644656658@qq.com", pay_bill.filename,pay_flow.filename2)
    os.system("rm -rf /opt/mysql_excel/payment/*.xlsx")
