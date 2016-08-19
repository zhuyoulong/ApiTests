#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName FileUtil.py
# Author: HeyNiu
# Created Time: 20160809


import os


def get_file_list(sessions_path):
    """
    获取目标地址目录下的文件列表
    :param sessions_path: 文件地址
    :return: 返回标地址目录下的文件列表
    """
    return (f for root, dirs, files in os.walk(sessions_path) for f in files)


def get_files_root(sessions_path):
    """
    获取目标地址目录下的文件列表路径
    :param sessions_path: 文件地址
    :return:
    """
    return (os.path.join(root, f) for root, dirs, files in os.walk(sessions_path) for f in files)
