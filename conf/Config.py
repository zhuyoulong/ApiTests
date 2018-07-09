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

import utils.Consts


class Config(object):
    def __init__(self, api_type):
        """
        初始化
        :param api_type:
        """
        self.config = configparser.ConfigParser()
        self.conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.conf')
        if not os.path.exists(self.conf_path):
            # 持续集成时配置文件目录有改变，需要兼容
            self.conf_path = os.path.join(os.path.dirname(
                os.path.abspath(__file__)[::-1].split('\\', 1)[-1][::-1]), 'conf', 'config.conf')
            if not os.path.exists(self.conf_path):
                raise FileNotFoundError("请确保配置文件存在！")
        self.config.read(self.conf_path, encoding='utf-8')
        self.type = api_type
        self.conf = {
            'tester': '',
            'project': '',
            'versionName': '',
            'versionCode': '',
            'AppBuild': '',
            'host': '',
            'systemType': '',
            'DeviceId': '',
            'Model': '',
            'DeviceOS': '',
            'Release': '',
            'getTokenHost': '',
            'loginHost': '',
            'loginInfo': '',
            'SessionsPath': '',
            'ApiURL': '',
            'SpecialSessions': '',
            'SessionsPair': '',
            'DuplicateSwitch': False
        }

    def get_conf(self):
        """
        配置文件读取，并赋值给全局参数
        :return:
        """
        print('读取配置文件中...')
        self.conf['tester'] = self.config.get(self.config.sections()[self.type], 'tester')
        self.conf['project'] = self.config.get(self.config.sections()[self.type], 'project')
        self.conf['versionName'] = self.config.get(self.config.sections()[self.type], 'versionName')
        self.conf['versionCode'] = self.config.get(self.config.sections()[self.type], 'versionCode')
        self.conf['AppBuild'] = self.conf['versionCode']
        self.conf['host'] = self.config.get(self.config.sections()[self.type], 'host')
        utils.Consts.HOST = self.conf['host']
        self.conf['getTokenHost'] = self.config.get(self.config.sections()[self.type], 'getTokenHost')
        self.conf['loginHost'] = self.config.get(self.config.sections()[self.type], 'loginHost')
        self.conf['loginInfo'] = self.config.get(self.config.sections()[self.type], 'loginInfo')
        self.conf['SessionsPath'] = self.config.get(self.config.sections()[self.type], 'SessionsPath')
        utils.Consts.SESSIONS_PATH = self.conf['SessionsPath']
        self.conf['ApiURL'] = self.config.get(self.config.sections()[self.type], 'ApiURL')
        utils.Consts.API_URL = self.conf['ApiURL']
        self.conf['SpecialSessions'] = self.config.get(self.config.sections()[self.type], 'SpecialSessions')
        utils.Consts.SPECIAL_SESSIONS = self.conf['SpecialSessions']
        # self.conf['SessionsPair'] = self.config.get(self.config.sections()[self.type], 'SessionsPair')
        # utils.Consts.SESSIONS_PAIR = self.conf['SessionsPair']
        self.conf['DuplicateSwitch'] = self.config.getboolean(self.config.sections()[self.type], 'DuplicateSwitch')
        utils.Consts.DUPLICATE_SWITCH = self.conf['DuplicateSwitch']
        # self.__init_data()
        utils.Consts.CONF = self.conf

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
            utils.Consts.CREATE_DICT[session_create_name] = session_create_parameter
            utils.Consts.DELETE_DICT[session_delete_name] = session_delete_parameter
            utils.Consts.MAPPING_DICT[session_delete_name] = session_create_name

    def save_conf(self):
        """
        保存本次配置文件
        :return:
        """
        dir0 = '%s\\Sessions' % (utils.Consts.SESSIONS_PATH,)
        if not os.path.exists(dir0):
            os.mkdir(dir0)
        dir1 = '%s\\%s\\' % (dir0, utils.Consts.HOST)
        if not os.path.exists(dir1):
            os.mkdir(dir1)
        conf_dir = '%sConf' % (dir1,)
        if not os.path.exists(conf_dir):
            os.mkdir(conf_dir)
        path = '%s\\conf.conf' % (conf_dir,)
        with open(path, 'w', encoding='utf-8') as f:
            d = self.config.sections()[self.type]
            f.write('[%s]' % (d,))
            f.write('\n')
            for k, v in self.config.items(d):
                f.write('%s = %s' % (k, v))
                f.write('\n')

if __name__ == '__main__':
    Config(0)
