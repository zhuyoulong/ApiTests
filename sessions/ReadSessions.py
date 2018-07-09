#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName ReadSessions.py
# Author: HeyNiu
# Created Time: 20160729
"""
读取录制的所有接口信息
"""

import os

import utils.FileUtil
import utils.Consts
import utils.HandleJson
import utils.Errors


class ReadSessions(object):
    def __init__(self):
        """
        初始化
        """
        self.sessions_path = '%s%s%s' % (utils.Consts.SESSIONS_PATH, "\\Api\\", utils.Consts.HOST)

    def __remove_special_files(self):
        """
        删除特定的不加入遍历接口的文件
        e.g.
        金钱相关、发文章等在外网的接口
        :return:
        """
        f = utils.FileUtil.get_file_list(self.sessions_path)
        # str数据转换成list
        remove_sessions = eval(utils.Consts.SPECIAL_SESSIONS)
        for i in f:
            for j in remove_sessions:
                if i.startswith(j):
                    os.remove('%s%s%s' % (self.sessions_path, "\\", i))

            # 移除录制异常的接口，即无数据的接口，否则重试时会计算进去
            file_path = '%s%s%s' % (self.sessions_path, '\\', i)
            if os.path.exists(file_path) and os.path.getsize(file_path) < 100:
                print('无效文件，执行删除：%s' % (i,))
                os.remove(file_path)

    def check_create_sessions(self):
        """
        检查是否存在对应的创建数据接口
        数据对应配置文件的SessionsPair
        :return:
        """
        for s in utils.Consts.CREATE_DICT.keys():
            file_path = '%s\\%s.txt' % (self.sessions_path, s)
            if not os.path.exists(file_path):
                raise utils.Errors.ApiNotRecorded('%s接口未录制，接口回归测试退出' % (s, ))

        # for s in utils.Consts.DELETE_DICT.keys():
        #     file_path = '%s\\%s.txt' % (self.sessions_path, s)
        #     if not os.path.exists(file_path):
        #         raise utils.Errors.ApiNotRecorded('%s接口未录制，接口回归测试退出' % (s, ))

    def __ignore_sessions(self):
        """
        忽略删除接口，用于延迟执行
        :return:
        """
        #删除特殊文件
        self.__remove_special_files()

        #获取sessions文件列表
        files = list(utils.FileUtil.get_file_list(self.sessions_path))

        #忽略删除接口
        for s in utils.Consts.DELETE_DICT.keys():
            file_path = '%s.txt' % (s, )
            if file_path in files:
                files.remove(file_path)
        return files

    def get_single_session_full_path(self, path):
        """
        获取单个文件的所有请求（单个请求的url，请求参数，json_dict，响应体）
        :param path: 完整路径
        :return:
        """
        return self.__read_session(path)

    @staticmethod
    def __read_session(path):
        """
        读取session
        :param path: 路径
        :return:
        """
        single_session = []
        total_session = []
        try:
            l1 = open(path, 'r', encoding='utf-8').readlines()
        except UnicodeDecodeError:
            l1 = open(path, 'r', encoding='utf-16-le').readlines()

        for i1 in l1:
            if not i1.startswith("\n"):
                # if i1.startswith("Request url: "):
                if"Request url: " in i1:
                    single_session.append(i1.split("Request url: ")[-1].replace("\n", ""))
                if"Request body: " in i1:
                    single_session.append(i1.split("Request body: ")[-1].replace("\n", ""))
                if"Response body: " in i1:
                    json_body = i1.split("Response body: ")[-1].replace("\n", "")
                    single_session.append(utils.HandleJson.HandleJson().decode_json(json_body))
                    single_session.append(json_body)

                # if i1.startswith("Request url: "):
                #     single_session.append(i1.split("Request url: ")[-1].replace("\n", ""))
                # if i1.startswith("Request body: "):
                #     single_session.append(i1.split("Request body: ")[-1].replace("\n", ""))
                # if i1.startswith("Response body: "):
                #     json_body = i1.split("Response body: ")[-1].replace("\n", "")
                #     single_session.append(utils.HandleJson.HandleJson().decode_json(json_body))
                #     single_session.append(json_body)
            if i1.startswith("Session end"):
                if len(single_session) == 4 and utils.Consts.HOST in single_session[0]:
                    if utils.Consts.DUPLICATE_SWITCH:
                        if len(total_session) == 0:
                            total_session.append(single_session)
                        else:
                            # 去除重复请求，依据request body判断
                            need_append = False
                            for s in total_session:
                                if single_session[0] == s[0] and single_session[1] == s[1]:
                                    break
                                if single_session[0] == s[0] and single_session[1] != s[1]:
                                    total_session.append(single_session)
                                    break
                                if single_session[0] != s[0]:
                                    need_append = True
                            if need_append:
                                total_session.append(single_session)
                    else:
                        total_session.append(single_session)

                single_session = []
        return total_session

    def get_single_session(self, path):
        """
        获取单个文件的所有请求（单个请求的url，请求参数，响应体）
        :param path: 局部路径
        :return:
        """
        file_path = '%s%s%s' % (self.sessions_path, "\\", path)
        return self.__read_session(file_path)

    def __get_all_session(self):
        """
        获取所有请求
        :return:
        """
        files = self.__ignore_sessions()
        utils.Consts.BEFORE_SESSIONS.clear()
        for i2 in files:
            utils.Consts.BEFORE_SESSIONS.append(i2)
            yield (self.get_single_session(i2))

    def get_will_request_sessions(self):
        """
        将要请求的最新接口数据源
        :return:
        """
        sessions = self.__get_all_session()
        return (j for i in sessions for j in i)


if __name__ == "__main__":
    r = ReadSessions()
