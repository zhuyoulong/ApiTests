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

import sessions.ReadConf
import utils.GlobalList


def choose_app_type(app_type):
    """
    选择app
    :param app_type: 0 >> 咚咚找房; 1 >> 咚咚抢客; 2 >> 家在; 3 >> 装修
    :return:
    """
    if app_type == 0:
        import sessions.DongDongRequests
        sessions.DongDongRequests.DongDongRequests(0).start()
    if app_type == 1:
        import sessions.DongDongRequests
        sessions.DongDongRequests.DongDongRequests(1).start()
    if app_type == 2:
        import sessions.JiaZaiRequests
        sessions.JiaZaiRequests.JiaZaiRequests().start()
    if app_type == 3:
        import sessions.DecorationRequests
        sessions.DecorationRequests.DecorationRequests().start()


def clear_data(app_type):
    """
    每次运行前清理测试数据
    :param app_type: 0 >> 咚咚找房; 1 >> 咚咚抢客; 2 >> 家在; 3 >> 装修
    :return:
    """
    print('清理测试数据...')
    if app_type == 0:
        d = utils.GlobalList.get_dd_type(0)
        utils.GlobalList.CURRENT_CONF_PATH = d.split("|")[0]
        print(utils.GlobalList.CURRENT_CONF_PATH)
        sessions.ReadConf.ReadConf(d.split("|")[0]).get_conf()
    if app_type == 1:
        d = utils.GlobalList.get_dd_type(1)
        utils.GlobalList.CURRENT_CONF_PATH = d.split("|")[0]
        sessions.ReadConf.ReadConf(d.split("|")[0]).get_conf()
    if app_type == 2:
        read = sessions.ReadConf.ReadConf(utils.GlobalList.JIAZAI_CONF_PATH)
        utils.GlobalList.CURRENT_CONF_PATH = utils.GlobalList.JIAZAI_CONF_PATH
        read.get_conf()
    if app_type == 3:
        read = sessions.ReadConf.ReadConf(utils.GlobalList.DECORATION_CONF_PATH)
        utils.GlobalList.CURRENT_CONF_PATH = utils.GlobalList.DECORATION_CONF_PATH
        read.get_conf()
    path = '%s\\Sessions\\%s' % (utils.GlobalList.SESSIONS_PATH, utils.GlobalList.HOST)
    if os.path.exists(path):
        shutil.rmtree(path)


def launcher_api_test(app_type):
    """
    请求总入口
    :param app_type: 0 >> A 1 >> B; 2 >> C; 3 >> D
    :return:
    """
    clear_data(app_type)
    choose_app_type(app_type)


if __name__ == "__main__":
    print('接口回归测试启动...')
    launcher_api_test(0)
