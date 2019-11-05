#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/22 16:13
# @Author  : tchua
# @Email   : tchuaxiaohua@163.com
# @File    : receipt bill.py
# @Software: PyCharm
import pymysql
from openpyxl import Workbook
import datetime
#from send_mail import send_mail
import os

sql="""
SELECT
bp.bill_payment_no as '账单号',
bpf.bill_payment_flow_no as '流水号',
sop.sys_operator_company_name as '付款公司',
bp.project_name as '项目',
sop.bank_name as '付款公司账户类型',
sop.bank_card_number as '付款公司账号',
b.bank_name as '收款人银行',
aer.owner_name as '委托人姓名',
bpf.receiver_name as '收款人姓名',
concat(bp.bill_start_time,'-',bp.bill_end_time) as '付款账期起止日期',
bp.bill_payment_time as '应付业主日期',
bpf.tax_with_amount as '应付金额',
bpf.tax_amount as '税额',
bpf.amount as '实付金额',
bpf.pay_time as '实付日期'
FROM
bill_payment_flow bpf
left join bill_payment bp on bp.code = bpf.bill_payment_code
left join account_entrust_rule aer on aer.contract_info_number = bp.contract_info_number
left join sys_operator_pay sop on sop.sys_operator_code = aer.operator_code
left join banks b on b.big_branch_code = bpf.big_branch_code;
"""

## 连接数据库函数
HOST_IP = "rm-bp1cfa3lz40mu707wuo.mysql.rds.aliyuncs.com"
def sql_connect(sql):
    conn = pymysql.connect(HOST_IP, 'one_read', '4KE6xIfm5T', 'onedb_pd')
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

## excel 菜单头
lst = [("A1","账单号"),("B1","流水号"),("C1","付款公司"),("D1","项目"),("E1","付款公司账户类型"),("F1","付款公司账号"),("G1","收款人银行"),
("H1","委托人姓名"),("I1","收款人姓名"),("J1","付款账期起止日期"),("K1","应付业主日期"),("L1","应付金额"),("M1","税额"),("N1","实付金额"),("O1","实付日期")]

## 写入Excel表格函数
def write_excel(filename,data):
    wb = Workbook()
    ws = wb.active
    for el in lst:
         ws[el[0]] = el[1]
    for d in data:
        ws.append(d)
    wb.save(filename)
    return filename

sql_data = sql_connect(sql)
filename2 = write_excel("项目付款账单流水" + "_" + datetime.datetime.now().strftime("%Y-%m-%d") + '.xlsx',sql_data)
