#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName HandleJson.py
# Author: HeyNiu
# Created Time: 20160728
"""
处理json信息，用于后面response body字段比较（含字段类型）
"""

import json


class HandleJson(object):
    def __init__(self):
        self.json_list = []
        self.time_param_list = []

    @staticmethod
    def print_json(json_data):
        """
        以树形结构打印json
        :param json_data: json数据源
        :return:
        """
        try:
            decode = json.loads(json_data)
            print(json.dumps(decode, ensure_ascii=False, sort_keys=True, indent=2))
        except (ValueError, KeyError, TypeError):
            print("JSON format error")

    def decode_json(self, json_data):
        """
        解析json并返回对应的key|value
        :param json_data: json数据源
        :return: 返回json各字段以及字段值
        """
        try:
            data = json.loads(json_data)
        except Exception as e:
            print(e)
            print("JSON format error")
            return []
        self.__iterate_json(data)
        return self.json_list

    def is_time_param(self, json_body):
        """
        response body是否有time参数，如果有返回它的长度，无则返回0
        :param json_body:json数据源
        :return:
        """
        self.__is_time_param(json_body)
        return self.time_param_list

    def __iterate_json(self, json_data, i=0):
        """
        遍历json
        :param i: 遍历深度
        :param json_data: json数据源
        :return: 返回json各字段以及字段值
        """
        if isinstance(json_data, dict):
            for k in json_data.keys():
                self.json_list.append('%s|%s' % (k, str(type(json_data[k])).split("'")[1]))
                if isinstance(json_data[k], list):
                    if len((json_data[k])) and isinstance(json_data[k][0], dict):
                        self.__iterate_json(json_data[k][0], i=i + 1)
                if isinstance(json_data[k], dict):
                    self.__iterate_json(json_data[k], i=i + 1)
        else:
            print("JSON format error")

    def __is_time_param(self, json_body, i=0):
        """
        response body是否有time参数，如果有返回它的长度，无则返回0
        :param i: 遍历深度
        :param json_body: json数据源
        :return:
        """
        if isinstance(json_body, dict):
            json_data = json_body
        else:
            json_data = json.loads(json_body)
        if isinstance(json_data, dict):
            for k in json_data.keys():
                if isinstance(json_data[k], list):
                    if len((json_data[k])) and isinstance(json_data[k][0], dict):
                        self.__is_time_param(json_data[k][0], i=i + 1)
                if isinstance(json_data[k], dict):
                    self.__is_time_param(json_data[k], i=i + 1)
                if k.lower().find('time') != -1:
                    if isinstance(json_data[k], int):
                        length = len(str(json_data[k]))
                        self.time_param_list.append('%s|%s' % (k, length))
        else:
            print("JSON format error")


if __name__ == "__main__":
    h = HandleJson()
