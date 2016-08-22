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
import utils.GlobalList
import utils.ApiException


def choose_app_type(app_type):
    """
    选择app
    :param app_type: 1 >> A; 2 >> B; 3 >> C
    :return:
    """
    if app_type == 1:
        import sessions.DongDongRequests
        sessions.DongDongRequests.DongDongRequests().start()
    if app_type == 2:
        import sessions.JiaZaiRequests
        sessions.JiaZaiRequests.JiaZaiRequests().start()
    if app_type == 3:
        import sessions.DecorationRequests
        sessions.DecorationRequests.DecorationRequests().start()


def clear_data(api_type):
    """
    每次运行前清理测试数据
    :param api_type: 接口类型
    :return:
    """
    print('清理测试数据...')
    conf.Config.Config(api_type)
    path = '%s\\Sessions\\%s' % (utils.GlobalList.SESSIONS_PATH, utils.GlobalList.HOST)
    if os.path.exists(path):
        shutil.rmtree(path)


def launcher_api_test(app_type, api_type=0):
    """
    请求总入口
    :param api_type: 接口类型
    0:A  内网测试  服务
    1:A  线上测试  服务
    2:B 内网测试  服务
    3:B  线上正式  服务
    ......
    :param app_type: 1 >> A; 2 >> B; 3 >> C
    :return:
    """
    mapping = {1: '01', 2: '23'}
    if mapping[app_type].find(str(api_type)) == -1:
        raise utils.ApiException.MappingError('应用类型与接口类型不匹配，请确认！')
    clear_data(api_type)
    choose_app_type(app_type)


if __name__ == "__main__":
    print('接口回归测试启动...')
    launcher_api_test(1)
