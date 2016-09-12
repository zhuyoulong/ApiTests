#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName Report.py
# Author: HeyNiu
# Created Time: 20160801
"""
生成HTML报告
pass:
报告保存在对应host下面的report目录
"""


import os
import utils.Consts
import utils.FileUtil
import sessions.ReadSessions


class Report(object):
    def __init__(self):
        """
        初始化
        """
        self.pass_sessions_path = '%s\\Sessions\\%s\\' % (utils.Consts.SESSIONS_PATH, utils.Consts.HOST)
        self.check_sessions_path = '%sCheck\\' % (self.pass_sessions_path,)

    def get_total_sessions(self):
        """
        获取本次请求的全部接口数量
        :return:
        """
        total_sessions = []
        pass_sessions = self.__get_pass_sessions()
        check_sessions = self.__get_check_sessions()
        for s in pass_sessions:
            for i in s:
                total_sessions.append('%s.txt' % (i[0].split('/')[-1],))
        for s in check_sessions:
            for i in s:
                total_sessions.append('%s.txt' % (i[0].split('/')[-1],))

        utils.Consts.TOTAL_SESSIONS = len(total_sessions)
        return len(total_sessions)

    def __get_check_sessions(self):
        """
        获取check文件夹下所有接口请求
        :return:
        """
        return self.__get_sessions(self.check_sessions_path)

    def __get_pass_sessions(self):
        """
        获取当前请求保存路径文件夹下所有接口请求，不含check文件夹
        :return:
        """
        return self.__get_sessions(self.pass_sessions_path)

    @staticmethod
    def __get_sessions(target_path):
        """
        获取给定路径下的所有请求
        :return:
        """
        files = utils.FileUtil.get_files_exclude_folder(target_path)
        return (sessions.ReadSessions.ReadSessions().get_single_session_full_path(f) for f in files)

    def get_the_results(self):
        """
        本次测试结果
        :return: true or false
        """
        if os.path.exists(self.check_sessions_path):
            if os.path.exists('%sProgramCrash.txt' % (self.check_sessions_path,)):
                return False
            if os.path.exists('%sFieldChange.txt' % (self.check_sessions_path,)):
                return False
            if os.path.exists('%sErrorResponse.txt' % (self.check_sessions_path,)):
                return False
            if os.path.exists('%sTimestampCompare.txt' % (self.check_sessions_path,)):
                return False
        return True


if __name__ == "__main__":
    r = Report()
    print(r.get_the_results())
