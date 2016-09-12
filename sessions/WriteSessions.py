#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName WriteSessions.py
# Author: HeyNiu
# Created Time: 20160728
"""
把请求session相关信息写入文件
包含
request url
request header
request body
response code
response body
"""

import os
import threading

import utils.Consts

mutex = threading.Lock()


def write_sessions(threading_id, threading_name, threading_queue, session, error_path):
    """
    封装线程
    :param threading_id:
    :param threading_name:
    :param threading_queue:
    :param session: 将要写入文件的session
    :param error_path: session的文件路径（文件名）
    :return:
    """
    w = WriteSessions(threading_id, threading_name, threading_queue, session, error_path)
    w.start()
    w.join()  # 主线程等待子线程完成后退出，否则可能出现数据还未写完，就退出程序了


class WriteSessions(threading.Thread):
    def __init__(self, threading_id, threading_name, threading_queue, session, error_path):
        threading.Thread.__init__(self)
        self.threading_id = threading_id
        self.threading_name = threading_name
        self.threading_queue = threading_queue
        self.session = session
        self.error_path = error_path
        self.path = ""

    def run(self):
        """
        执行线程操作
        :return:
        """
        global mutex
        if mutex.acquire():
            self.__write_session()
            mutex.release()

    def __write_session(self):
        """
        把请求写入文件，一个请求一个文件
        :return:
        """
        dir1 = '%s\\Sessions\\%s\\' % (utils.Consts.SESSIONS_PATH, utils.Consts.HOST)
        if len(self.error_path) == 0:
            self.path = '%s%s%s' % (dir1, self.session[0], ".txt")
        else:
            if not os.path.exists('%sCheck\\' % (dir1,)):
                os.mkdir('%sCheck\\' % (dir1,))
            self.path = '%sCheck\\%s.txt' % (dir1, self.error_path)
        with open(self.path, 'a', encoding='utf-8') as f:
            for i in self.session:
                f.write(i)
                f.write("\n")
            f.write("Session end")
            f.write("\n")
            f.write("\n")


if __name__ == "__main__":
    pass
