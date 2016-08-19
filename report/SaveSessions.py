#!/usr/bin/evn python
# -*- coding:utf-8 -*-

# FileName SaveSessions.py
# Author: HeyNiu
# Created Time: 20160818
"""
另存测试数据，方便以后查阅
1.打包sessions文件夹下所有内容
2.打包项目配置文件
3.将上述步骤合并为一个压缩包以项目+版本号+时间形式保存
"""

import utils.GlobalList
import utils.TimeUtil
import utils.FileUtil
import zipfile
import os
import shutil


class SaveSessions(object):
    def __init__(self):
        self.sessions_path = '%s\\Sessions\\%s\\' % (utils.GlobalList.SESSIONS_PATH, utils.GlobalList.HOST)
        self.format_time = '%Y%m%d%H%M%S'
        self.zip_name = '%sV%s_b%s_%s' % (utils.GlobalList.CONF['project'], utils.GlobalList.CONF['versionName'],
                                          utils.GlobalList.CONF['versionCode'],
                                          utils.TimeUtil.timestamp(self.format_time))
        utils.GlobalList.ZIP_NAME = self.zip_name
        self.save_path = '%s\\History Sessions' % (utils.GlobalList.SESSIONS_PATH,)

    def __compression_file(self):
        """
        数据包含配置文件、接口数据、测试报告
        :return: 数据压缩为zip文件
        """
        conf_path = utils.GlobalList.CURRENT_CONF_PATH
        zip1 = zipfile.ZipFile(self.zip_name, 'w')
        files = utils.FileUtil.get_files_root(self.sessions_path)
        for f in files:
            zip1.write(f, f.split('\\Sessions')[-1])
        zip1.write(conf_path, conf_path[::-1].split('\\', 1)[0][::-1])
        zip1.close()

    def save_file(self):
        """
        文件保存在fiddler sessions文件夹下
        :return:
        """
        self.__compression_file()
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)
        source_dir = os.path.join(os.getcwd(), self.zip_name)
        target_dir = os.path.join(self.save_path, self.zip_name)
        shutil.copy(source_dir, target_dir)


if __name__ == "__main__":
    s = SaveSessions()

