#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName Consts.py
# Author: HeyNiu
# Created Time: 20160801
"""
接口常量全局文件
"""

CONF = {}  # 请求头配置文件字典
ZIP_NAME = ''  # 测试数据另存的压缩文件名
SESSIONS_PATH = 'D:\\Fiddler Sessions'  # 接口的存储/读取路径
API_URL = ''  # 拉取接口名的地址
SPECIAL_SESSIONS = ''  # 屏蔽的接口列表
SESSIONS_PAIR = ''  # 接口对 e.g: 创建数据接口:字段|删除数据接口:字段
CREATE_DICT = {'Sessions':'/Manage/aAccount/Login'}  # 创建数据接口字典 key >> 接口名 value >> 返回字段id
DELETE_DICT = {}  # 删除数据接口字典 key >> 接口名 value >> 请求字段id
MAPPING_DICT = {}  # 映射字典，即删除数据接口对应的创建数据接口
HOST = ''  # 接口host
BEFORE_SESSIONS = []  # 遍历前的全部接口，即ReadSessions读取的接口
DUPLICATE_SWITCH = False  # 接口请求去重开关

TOTAL_SESSIONS = 1  # 请求的接口总数
RESULT = False

# 接口压测全局配置
STRESS_SWITCH = False
STRESS_LIST = []  # 接口耗时列表

BEAR_TOKEN='Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdW56aGVuIiwianRpIjoiODVkYjNkMDUtMTlmNC00MGRiLWE0M2UtZjE5ZWZjOTg1YTM2IiwiZ2l2ZW5fbmFtZSI6IuWtmeecnyIsIkdyb3VwIjoiMWY4OTczYzctM2UzMy00Y2U4LWE4NDQtODc0OGNhYWM4ZTcxIiwiVG9rZW4iOiI2NTY4ZmUyMjBhZDQ3YjI3ZTQwMzkxY2E2YmQzNmE4MmM2ZGE2MzVkIiwiZXhwIjoxNTMzNzgxMzk2LCJpc3MiOiJodHRwOi8vdWMucHVwdXZpcC5jb20iLCJhdWQiOiJodHRwOi8vdWMucHVwdXZpcC5jb20ifQ.8wLt9LqriAqr1MQ6YKlvVzj7xdbx_m0FZRNFcRYNeI4'
