#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName Request.py
# Author: HeyNiu
# Created Time: 20160728
"""
请求接口核心文件
"""

import datetime
import difflib
import json
import time

import requests
import threadpool

import report.Report
import report.SaveSessions
import report.SendEmail
import retry.Retry
import sessions.DelaySessions
import sessions.ReadSessions
import sessions.WriteSessions
import utils.CodeUtil
import utils.Consts
import utils.HandleJson
import utils.TimeUtil


def thread_pool(app_type, sessions1):
    """
    线程池，根据app类型进行请求
    :param app_type: app类型
    :param sessions1: 请求list
    :return:
    """
    requests1 = []
    pool = threadpool.ThreadPool(8)
    if app_type == 1:
        import sessions.A
        requests1 = threadpool.makeRequests(sessions.A.A().thread_pool, sessions1)
    elif app_type == 2:
        pass
    [pool.putRequest(req) for req in requests1]
    pool.wait()


class Request(object):
    def __init__(self, thread_count=8):
        """
        初始化
        """
        self.thread_count = thread_count
        self.session = requests.session()
        self.TOKEN_NAME = ""
        self.TOKEN_VALUE = ""
        self.uId = "0"
        self.uName = ""
        self.uPhone = ""
        self.SessionId = ""
        self.uType = "0"
        self.temp = ""
        self.time = ""
        self.format_time = ''
        self.threading_id = 0

    def get_token_des(self):
        """
        生成token密文
        :return:
        """
        pass

    def get_session_des(self, method_name):
        """
        生成普通请求密文
        :return:
        """
        pass

    def __diff_verify_write(self, sessions1, expect_json_body, expect_json_list, result_json_body, result_json_list,
                            diff, session_name):
        """
        主要用于差异化写入文件
        :param sessions1: 请求返回的session
        :param expect_json_body: 预期json body
        :param expect_json_list: 预期json list
        :param result_json_body: 实际json body
        :param result_json_list: 实际json list
        :param diff: 差异化list
        :param session_name: 保存session的文件名
        :return:
        """
        sessions1.append('Expect json body: %s' % (expect_json_body,))
        sessions1.append('Expect json dict: %s' % (expect_json_list,))
        sessions1.append('Result json body: %s' % (result_json_body,))
        sessions1.append('Result json dict: %s' % (result_json_list,))
        sessions1.append('Diff: %s' % (diff,))
        sessions.WriteSessions.write_sessions(self.threading_id, "t", self.threading_id, sessions1, session_name)

    def post_request(self, sessions1, key1, key2):
        """
        请求接口，获得session
        :param sessions1: 返回的sessions
        :param key1: 类似之前的StatsCode
        :param key2: 类似之前的Message
        :return:
        """
        # verify response body
        expect_json_body = sessions1[-1]
        expect_json_list = sessions1[-2]
        result_json_body = sessions1[-3]
        result_json_list = utils.HandleJson.HandleJson().decode_json(result_json_body)
        diff = list(set(expect_json_list) ^ set(result_json_list))  # 求差集

        if sessions1[0] != 200:
            sessions.WriteSessions.write_sessions(self.threading_id, "t", self.threading_id, sessions1[1],
                                                  "ErrorResponse")
            return
        if not diff:
            self.__un_diff_verify_write(sessions1, key1, key2)
        elif 0.8 < difflib.SequenceMatcher(None, expect_json_list, result_json_list).ratio() < 1.0:
            # 相似度最低限度初定为80%，后续跟进实际情况调整
            # 计算2个list相似度，大于80%小于100%才判断预期，排除大部分数据影响
            self.__diff_verify_write(sessions1[1], expect_json_body, expect_json_list, result_json_body,
                                     result_json_list, diff, "Unexpected")
        elif len(expect_json_list) == len(result_json_list):
            if json.loads(sessions1[-1])[key1] == json.loads(sessions1[-3])[key1]:
                # 长度相等且response json code相等时 主要验证字段类型改变 如：整型变成布尔型
                self.__diff_verify_write(sessions1[1], expect_json_body, expect_json_list, result_json_body,
                                         result_json_list, diff, "FieldChange")
            else:
                sessions.WriteSessions.write_sessions(self.threading_id, "t", self.threading_id, sessions1[1],
                                                      "VerifyRequest")
        else:
            # 相似度太低一般由于数据影响，这一块暂不考虑
            self.__un_diff_verify_write(sessions1, key1, key2)

    def __un_diff_verify_write(self, sessions1, key1, key2):
        """
        没有差异化以及差异化太大时的验证
        :param sessions1: 返回的sessions
        :param key1: 类似之前的StatsCode
        :param key2: 类似之前的Message
        :return:
        """
        crash = ['异常', '找不到方法', '	服务器无法在已发送', '已成功与服务器建立连接', '给定关键字不在字典中',
                 '未将对象引用', '格式化程序尝试对消息反序列化时引发异常', '附近有语法错误', '	列名',
                 'SQL Server', '超时时间已到', '在控制器', '溢出', '转换为', '远程主机强迫关闭了一个现有的连接',
                 'could not connect to redis', '未能加载文件或程序集', '该字符串未被识别为有效的', '程序集',
                 '必须声明标量变量', '输入字符串的格式不正确', '握手期间', '无法连接到远程服务器', '未能解析此远程名称',
                 'Unable to Connect', 'Timeout', '接收时发生错误', '格式化程序尝试']
        status = json.loads(sessions1[-3])[key1]
        if status != 1 and status != -1 and status != 200:
            for i in crash:
                if i in json.loads(sessions1[-3])[key2]:
                    sessions.WriteSessions.write_sessions(self.threading_id, "t", self.threading_id, sessions1[1],
                                                          "ProgramCrash")
                else:
                    expect_json_body = sessions1[-1]
                    result_json_body = sessions1[-3]
                    expect_code = utils.HandleJson.HandleJson.response_json_stats_code(key1, expect_json_body)
                    result_code = utils.HandleJson.HandleJson.response_json_stats_code(key1, result_json_body)
                    if expect_code == result_code:
                        sessions.WriteSessions.write_sessions(self.threading_id, "t", self.threading_id, sessions1[1],
                                                              "")
                    else:
                        sessions.WriteSessions.write_sessions(self.threading_id, "t", self.threading_id, sessions1[1],
                                                              "VerifyRequest")
        else:
            self.__timestamp__compare(sessions1)

    def __timestamp__compare(self, sessions2):
        """
        time参数时间戳长度对比，不一致则存入TimestampCompare文件
        :return:
        """
        result_param_length = utils.HandleJson.HandleJson().is_time_param(sessions2[-3])
        expect_param_length = utils.HandleJson.HandleJson().is_time_param(sessions2[-1])
        if len(result_param_length) > 0 and len(expect_param_length) > 0:

            diff = list(set(result_param_length) ^ set(expect_param_length))
            length = len(diff)
            if length > 1 and length % 2 == 0:  # 是2的倍数的才写入文件，单数时是由于未读等原因时间是0长度为1，不属于bug
                sessions2[1].append('Expect json body: %s' % (sessions2[-1],))
                sessions2[1].append('Result json body: %s' % (sessions2[-3],))
                sessions2[1].append('Timestamp diff length: %s' % (diff,))
                sessions.WriteSessions.write_sessions(self.threading_id, "t", self.threading_id, sessions2[1],
                                                      "TimestampCompare")
            else:
                sessions.WriteSessions.write_sessions(self.threading_id, "t", self.threading_id, sessions2[1], "")
        else:
            sessions.WriteSessions.write_sessions(self.threading_id, "t", self.threading_id, sessions2[1], "")

    def __post_session(self, url1, headers, json_dict, json_body, data1=None):
        """
        发送请求并简单校验response，再写入文件
        :param url1: 请求的url
        :param headers: 请求头
        :param json_dict: json字典 >> 键值对方式 key：字段 value：字段类型
        :param json_body: 请求返回的response json body
        :param data1: 请求参数
        :return:
        """
        if not url1.startswith("http://"):
            url1 = '%s%s' % ("http://", url1)
        print(url1)
        try:
            if data1 is None:
                response = self.session.post(url1, headers=headers, timeout=30)
            else:
                data1 = utils.CodeUtil.url_encode(data1)
                response = self.session.post(url1, headers=headers, data=data1, timeout=30)
        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ', url1))
            print(e)
            return ()
        except Exception as e:
            print('%s%s' % ('Exception url: ', url1))
            print(e)
            return ()
        self.threading_id += 1
        # 接口耗时记录
        time_consuming = response.elapsed.microseconds / 1000
        utils.Consts.STRESS_LIST.append(time_consuming)
        return (response.status_code,
                [url1.split("/")[-1], 'Request url: %s' % (url1,), "Request headers: %s" % (headers,),
                 'Request body: %s' % (data1,), 'Response code: %s' % (response.status_code,),
                 'Response body: %s' % (response.text,), 'Time-consuming: %sms' % (time_consuming,),
                 'Sole-mark: %s' % (time.time(),)], response.text, json_dict, json_body)

    def post(self, sessions1, session_header, key1, key2):
        """
        请求接口
        :param sessions1:返回的sessions
        :param session_header: 获取头部方法
        :param key1: 类似之前的StatsCode
        :param key2: 类似之前的Message
        :return:
        """
        sessions2 = self.__post_session(sessions1[0], session_header, sessions1[2], sessions1[-1], sessions1[1])
        self.post_request(sessions2, key1, key2)

    def start_thread_pool(self, thread_pool1, app_type):
        """
        开始请求接口
        :param thread_pool1: 线程池
        :param app_type: 1 >> 咚咚; 2 >> 家在; 3 >> 装修
        :return:
        """
        d1 = datetime.datetime.now()
        s = sessions.ReadSessions.ReadSessions()
        print("读取接口数据中...")
        s.check_create_sessions()
        l = s.get_will_request_sessions()  # 获取将要请求的所有接口数据
        print("接口请求中，请等待...")

        pool = threadpool.ThreadPool(self.thread_count)
        requests1 = threadpool.makeRequests(thread_pool1, l)
        [pool.putRequest(req) for req in requests1]
        pool.wait()
        print("接口请求完成！")

        # 重试机制
        retry.Retry.retry11(app_type)

        # 清理数据
        print("正在整理创建的数据...")
        sessions.DelaySessions.clear_up(app_type)
        print("测试报告准备中...")
        print("备份测试数据中...")
        # 备份本次测试数据
        report.SaveSessions.SaveSessions().save_file()
        print("发送邮件中...")
        # 发送邮件
        report.SendEmail.send_email()
        d2 = datetime.datetime.now()
        t = d2 - d1
        print('接口回归测试完成！')
        report.Report.Report().get_total_sessions()
        print('完成%s个接口请求' % (utils.Consts.TOTAL_SESSIONS,))
        print("%s %s%s" % ("耗时：", t.seconds, "s"))
