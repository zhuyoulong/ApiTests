#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName GlobalList.py
# Author: HeyNiu
# Created Time: 20160801
"""
接口全局文件
"""

CURRENT_CONF_PATH = ''
CONF = {}
ZIP_NAME = ''
TOTAL_SESSIONS = 0
SESSIONS_PATH = 'D:\\Fiddler Sessions'
API_URL = ''
SPECIAL_SESSIONS = 'GetToken'  # 默认值
SESSIONS_PAIR = ''
CREATE_DICT = {}  # 创建数据接口字典 key >> 接口名 value >> 返回字段id
DELETE_DICT = {}  # 删除接口字典 key >> 接口名 value >> 请求字段id
MAPPING_DICT = {}  # 映射字典，即删除数据接口对应的创建数据接口
HOST = ''
BEFORE_SESSIONS = []  # 遍历前的全部接口，即ReadSessions读取的接口
