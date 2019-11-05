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
 bp.id,
 bp.`code`,
 bp.`project_name` AS '项目',
 ap.owner_name AS '业主',
 CONCAT(
  seb.build_name,
  '-',
  seb.floor_name,
  '-',
  seb.shop_code
 ) AS '铺位号',
 CASE bp.`fee_type`
WHEN '1' THEN
 '租金'
WHEN '2' THEN
 '意向金'
WHEN '3' THEN
 '定金'
WHEN '4' THEN
 '补充金额'
WHEN '5' THEN
 '交接后补充金额'
WHEN '6' THEN
 '赔偿金'
WHEN '7' THEN
 '个人所得税'
WHEN '8' THEN
 '历史数据校准'
ELSE
 '-'
END AS '账单类型',
 bp.bill_payment_no AS '账单编号',
 bp.`fee_amount` AS '账单金额(元)',
 bp.`payment_amount` AS '已付金额(元)',
 bp.`wait_payment_amount` AS '待处理金额(元)',
 bp.`unpaid_amount` AS '待付金额(元)',

IF (
 action_type = 2,
 CONCAT(
  bp.`adjust_start_time`,
  '~',
  bp.`adjust_end_time`
 ),
 CONCAT(
  bp.`bill_start_time`,
  '~',
  bp.`bill_end_time`
 )
) AS '账单周期',
 CASE bp.`approve_status`
WHEN '1' THEN
 '审批中'
WHEN '2' THEN
 '审批完成'
WHEN '3' THEN
 '审批驳回'
ELSE
 '-'
END AS '审批状态',
 bp.`bill_payment_time` AS 应付日期,
 CASE bp.`settle_state`
WHEN '10' THEN
 '未付清'
WHEN '20' THEN
 '已付清'
WHEN '30' THEN
 '欠付'
WHEN '40' THEN
 '无需付款'
END AS 付款状态,
cf.form_json->>'$.ownerBankAccountName' as '收款户名',
cf.form_json->>'$.ownerBankAccount' as '收款卡号',
cf.form_json->>'$.bankBranch' as '收款开户行'
FROM
 bill_payment bp
JOIN account_payment ap ON ap.contract_info_number = bp.contract_info_number
JOIN sys_expand_bunk seb ON seb. CODE = ap.bunk_code
LEFT JOIN contract_process cp on bp.contract_info_number = cp.contract_no
LEFT JOIN contract_form cf on cf.process_code = cp.code
WHERE
 bp.delete_state = 0
ORDER BY
 bp.id DESC;
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

lst = [("A1","id"),("B1","code"),("C1","项目"),("D1","业主"),("E1","铺位号"),("F1","账单类型"),("G1","账单编号"),
("H1","账单金额(元)"),("I1","已付金额(元)"),("J1","待处理金额(元)"),("K1","待付金额(元)"),("L1","账单周期"),("M1","审批状态"),("N1","应付日期"),
("O1","付款状态"),("P1","收款户名"),("Q1","收款卡号"),("R1","收款开户行")]
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
filename = write_excel("项目付款账单" + "_" + datetime.datetime.now().strftime("%Y-%m-%d") + '.xlsx',sql_data)
