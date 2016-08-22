#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName ApiException.py
# Author: HeyNiu
# Created Time: 2016/8/22
"""
自定义异常类
"""


class TokenException(Exception):
    """
    gettoken失败时抛出此异常
    """
    pass


class LoginException(Exception):
    """
    登录失败时抛出此异常
    """
    pass


class ApiNotRecorded(FileNotFoundError):
    """
    接口未录制时抛出此异常
    """
    pass


class MappingError(Exception):
    """
    app_type映射的api_type错误时抛出此异常
    """
    pass

if __name__ == '__main__':
    pass
