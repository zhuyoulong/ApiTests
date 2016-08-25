#!/usr/bin/python
# -*- coding: UTF-8 -*-

# FileName SendEmail.py
# Author: HeyNiu
# Created Time: 20160818

import os
import smtplib
import urllib.request
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import utils.GlobalList


def send_email():
    """
    邮件发送
    :return:
    """
    conf = utils.GlobalList.CONF
    app_name = conf['project']
    app_version = conf['versionName']
    app_build_version = conf['versionCode']

    # 邮件接受者
    mail_receiver = []

    # 邮箱配置
    mail_host = 'smtp.qq.com'
    mail_port = 465
    mail_user = ''
    mail_pwd = ''
    mail_to = ','.join(mail_receiver)

    mail_title = 'Api Test Report for %sV%s b%s' % (app_name, app_version, app_build_version)
    # html body
    message = open(os.path.join(os.getcwd()[::-1].split('\\', 1)[-1][::-1], 'report', 'Email.html'),
                   encoding='utf-8').read()

    body = MIMEText(message, _subtype='html', _charset='utf-8')
    # 本次测试结果附件
    part = MIMEApplication(open(os.path.join(utils.GlobalList.SESSIONS_PATH, 'History Sessions',
                                             utils.GlobalList.ZIP_NAME), 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=urllib.request.quote(utils.GlobalList.ZIP_NAME))

    msg = MIMEMultipart()
    msg.attach(body)
    # msg.attach(image)
    msg.attach(part)
    msg['to'] = mail_to
    msg['from'] = mail_user
    msg['Subject'] = mail_title

    try:
        smtp = smtplib.SMTP_SSL(mail_host, mail_port)
        smtp.login(mail_user, mail_pwd)
        smtp.sendmail(mail_user, mail_receiver, msg.as_string())
        smtp.quit()
        print('邮件发送成功')
    except Exception as e:
        print('邮件发送失败')
        print(e)


if __name__ == '__main__':
    send_email()
