#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName A.py
# Author: HeyNiu
# Created Time: 20160811
"""
A request
"""

import json

import base.Request
import utils.Consts
import utils.HandleJson
import utils.Errors


class A(base.Request.Request):
    def __init__(self):
        """
        初始化
        """
        super(A, self).__init__()
        self.conf = utils.Consts.CONF
        self.AUTHORIZATION = ""
        self.AUTHORIZATION_TOKEN = ""
        self.uuid = "0"
        self.__get_token_header()
        self.__login_session()
        self.url = ""
        self.request_body = ""
        self.data = ""
        self.sessions = ()

    def __get_token_header(self):
        """
        生成token头部
        :return:
        """
        des = self.get_token_des()
        arr = (des,)
        authorization = self.AUTHORIZATION_TOKEN % arr
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8', 'Authorization': authorization}
        response = self.session.post(self.conf['getTokenHost'], headers=headers)
        if json.loads(response.text)['A'] == 200:
            pass
        else:
            utils.HandleJson.HandleJson.print_json(response.text)
            raise utils.Errors.TokenException("GetToken失败，请手动检查！")

    def __login_session(self):
        """
        调用登录接口，这样后面的接口都能正常访问了
        :return:
        """
        url_login = self.conf['loginHost']
        headers = self.__get_session_header(url_login.split('api/')[-1])
        data_login = r'%s' % self.conf['loginInfo']
        response = self.session.post(url_login, headers=headers, data=data_login)
        if json.loads(response.text)['A'] == 200:
            pass
        else:
            utils.HandleJson.HandleJson.print_json(response.text)
            raise utils.Errors.LoginException("登录失败，请手动检查！")

    def __get_session_header(self, method_name):
        """
        生成session头部
        :return:
        """
        des = self.get_session_des(method_name)
        arr = (des[1], method_name, des[0])
        authorization = self.AUTHORIZATION % arr
        return {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8', 'Authorization': authorization}

    def thread_pool(self, l):
        """
        准备线程池请求接口
        :param l: 接口列表
        :return:
        """
        if l is None or len(l) == 0:
            return
        try:
            self.post(l, self.__get_session_header(l[0].split("api/")[-1]), '', '')
        except IndexError:
            print('%s%s' % ('IndexError url:\n', l[0]))

    def start(self):
        """
        开启线程池请求接口
        :return:
        """
        self.start_thread_pool(self.thread_pool, 1)

if __name__ == '__main__':
    dd = A()
    dd.start()
