#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName RequestApi.py
# Author: HeyNiu
# Created Time: 20160729
"""
运行api测试总入口
"""
import os
import shutil

import conf.Config
import utils.Consts
import utils.Errors


def choose_app_type(app_type):
    """
    选择app
    :param app_type: 1 >> A; 2 >> B; 3 >> C
    :return:
    """
    if app_type == 1:
        import sessions.A
        sessions.A.A().start()
    if app_type == 2:
        pass


def clear_data(api_type):
    """
    每次运行前清理测试数据
    :param api_type: 接口类型
    :return:
    """
    print('清理测试数据...')
    c = conf.Config.Config(api_type)
    c.get_conf()  # 读取配置文件
    path = '%s\\Sessions\\%s' % (utils.Consts.SESSIONS_PATH, utils.Consts.HOST)
    if os.path.exists(path):
        shutil.rmtree(path)
    c.save_conf()  # 保存本次配置


def launcher_api_test(app_type, api_type=0):
    """
    请求总入口
    :param api_type: 接口类型
    0:A  内网测试  服务
    1:A  线上测试  服务
    2:B  内网测试  服务
    3:B  线上正式  服务
    ......
    :param app_type: 1 >> A; 2 >> B; 3 >> C
    :return:
    """
    mapping = {1: '01', 2: '23'}
    if str(api_type) not in mapping[app_type]:
        raise utils.Errors.MappingError('应用类型与接口类型不匹配，请确认！')
    clear_data(api_type)
    choose_app_type(app_type)


if __name__ == "__main__":
    print('接口回归测试启动...')
    launcher_api_test(1)
