#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName Config.py
# Author: HeyNiu
# Created Time: 2016/8/22
"""
http接口测试框架配置信息解析器
"""
import configparser
import os

import utils.GlobalList


class Config(object):
    def __init__(self, api_type):
        self.config = configparser.ConfigParser()
        self.conf_path = os.path.join(os.getcwd()[::-1].split('\\', 1)[-1][::-1], 'conf', 'config.conf')
        if not os.path.exists(self.conf_path):
            raise FileNotFoundError("请确保配置文件存在！")
        self.config.read(self.conf_path, encoding='utf-8')
        self.type = api_type
        self.conf = {'tester': '', 'project': '', 'versionName': '', 'versionCode': '', 'AppBuild': '', 'host': '',
                     'systemType': '2', 'DeviceId': 'ffffffff-b3f1-87ad-90ef-ebeb00000000', 'Model': 'MI+4LTE',
                     'DeviceOS': '23', 'Release': '6.0.1', 'getTokenHost': '', 'loginHost': '', 'loginInfo': '',
                     'SessionsPath': '', 'ApiURL': '', 'SpecialSessions': '', 'SessionsPair': ''}
        self.__get_conf()

    def __get_conf(self):
        print('读取配置文件中...')
        self.conf['tester'] = self.config.get(self.config.sections()[self.type], 'tester')
        self.conf['project'] = self.config.get(self.config.sections()[self.type], 'project')
        self.conf['versionName'] = self.config.get(self.config.sections()[self.type], 'versionName')
        self.conf['versionCode'] = self.config.get(self.config.sections()[self.type], 'versionCode')
        self.conf['AppBuild'] = self.conf['versionCode']
        self.conf['host'] = self.config.get(self.config.sections()[self.type], 'host')
        utils.GlobalList.HOST = self.conf['host']
        self.conf['getTokenHost'] = self.config.get(self.config.sections()[self.type], 'getTokenHost')
        self.conf['loginHost'] = self.config.get(self.config.sections()[self.type], 'loginHost')
        self.conf['loginInfo'] = self.config.get(self.config.sections()[self.type], 'loginInfo')
        self.conf['SessionsPath'] = self.config.get(self.config.sections()[self.type], 'SessionsPath')
        utils.GlobalList.SESSIONS_PATH = self.conf['SessionsPath']
        self.conf['ApiURL'] = self.config.get(self.config.sections()[self.type], 'ApiURL')
        utils.GlobalList.API_URL = self.conf['ApiURL']
        self.conf['SpecialSessions'] = self.config.get(self.config.sections()[self.type], 'SpecialSessions')
        utils.GlobalList.SPECIAL_SESSIONS = self.conf['SpecialSessions']
        self.conf['SessionsPair'] = self.config.get(self.config.sections()[self.type], 'SessionsPair')
        utils.GlobalList.SESSIONS_PAIR = self.conf['SessionsPair']
        self.__init_data()
        utils.GlobalList.CONF = self.conf

    def __init_data(self):
        """
        初始化接口对，提取出创建数据接口与删除数据接口
        :return:
        """
        for i in eval(self.conf['SessionsPair']):
            session_create_name = i.split(':')[0]
            session_create_parameter = i.split(':')[1].split('|')[0]
            session_delete_name = i.split('|')[-1].split(':')[0]
            session_delete_parameter = i.split(':')[-1]
            utils.GlobalList.CREATE_DICT[session_create_name] = session_create_parameter
            utils.GlobalList.DELETE_DICT[session_delete_name] = session_delete_parameter
            utils.GlobalList.MAPPING_DICT[session_delete_name] = session_create_name

if __name__ == '__main__':
    Config(0)
