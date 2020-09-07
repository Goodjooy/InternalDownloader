# -*- coding: utf-8 -*-
# @Author: FrozenString
# @Date:   2020-08-22 21:09:52
# @Last Modified by:   FrozenString
# @Last Modified time: 2020-09-07 12:28:55


import math
import os
import re
import shutil
import time
from concurrent.futures import ThreadPoolExecutor
from urllib import parse

import requests
import wx

from theard_work import DownloadWork


def bit_transform(bit, var=2, edge=0.9, add_speed=True):
    b2kb = bit / 1024
    kb2mb = b2kb / 1024
    mb2gb = kb2mb / 1024
    gb2tb = mb2gb / 1024

    if add_speed:
        if b2kb <= edge:
            return f"{round(bit, var)} B/S\t\t"
        elif b2kb > edge >= kb2mb:
            return f"{round(b2kb, var)} KB/S\t\t"
        elif kb2mb > edge >= mb2gb:
            return f"{round(kb2mb, var)} MB/S\t\t"
        elif mb2gb > edge >= gb2tb:
            return f"{round(mb2gb, var)} GB/S\t\t"
        else:
            return f"{round(gb2tb, var)} TB/S\t\t"
    else:
        if b2kb <= edge:
            return f"{round(bit, var)} B"
        elif b2kb > edge >= kb2mb:
            return f"{round(b2kb, var)} KB"
        elif kb2mb > edge >= mb2gb:
            return f"{round(kb2mb, var)} MB"
        elif mb2gb > edge >= gb2tb:
            return f"{round(mb2gb, var)} GB"
        else:
            return f"{round(gb2tb, var)} TB"


class DownloadCtrl(object):
    def __init__(self, target_url, save_path, workshop: wx.ListCtrl, list_count, task_count, info_shop: wx.StaticText,
                 is_recover=False, default_setting=None) -> None:
        self.target = target_url
        self.save_path = save_path
        self.workshop = workshop
        self.task_count = task_count
        self.info_shop = info_shop

        # 网络请求的参数
        self.param = {}
        self.headers = {}
        self.cookies = {}

        self.connect_timeout = 5
        self.read_timeout = 5
        # 预读取返回信息
        self.res_headers = {}
        self.res_status_code = 0
        # 线程控制
        self.thread_num = 32
        self.thread_pool = None
        self.thread_ctrl_group = []
        self.thread_future = []
        self.watch_thread = None
        # 文件类型控制组
        self.temp_path = ""
        self.save_file_path = ''
        self.file_name = ""
        self.file_type = None
        self.file_ex = None
        self.file_encode = None
        self.re_charset = re.compile(r'^(?:charset=)(.+?)$')
        self.re_filename = re.compile(r'^(?:.+);filename="(.+?)"$')

        self.is_accept_range = False
        # 下载控制组
        self.total_file_size = 0
        self.downloaded_size = 0
        self.addon_size = 0
        self.each_size = 0
        self.down_speed = 0

        self.real_url = ""

        self.chunk_size = 1024

        self.sleep_time = 0.25
        # 下载大小为0，触发线程重置的计数次数
        self.stop_count_limit = 50
        self.link_delay = 1
        # 列表显示控制
        self.list_index = 0
        self.list_count = list_count
        # 状态控制
        self.is_single = False
        self.is_done = False
        self.is_stop = False
        # 当为断点续传恢复状态；有以下情况
        # 1 不进行预加载
        # 2 不计算每块大小
        # 3 不自动开始
        self.is_recover = is_recover

        self.reset_count = 1

        if default_setting is not None:
            for k, v in default_setting.items():
                if k == "children":
                    break
                else:
                    self.__setattr__(k, v)

        self.session = requests.session()

    @staticmethod
    def recover_task(data: dict, workshop: wx.ListCtrl, list_count, task_count, info_shop: wx.StaticText):
        """
        断点续传恢复调用，返回DownloadCtrl对象
        函数行为：
            1-新建对象
            2-将data的参数传递进去
            3-生成多线程控制器
            4-计算已经下载的大小
            5-校对文件大小（未实现）
            6-初始化下载控制器
        """
        # 新建对象
        temp = DownloadCtrl("", "", workshop, list_count,
                            task_count, info_shop, True)
        # 传递参数
        for k, v in data.items():
            if k == "children":
                break
            else:
                temp.__setattr__(k, v)
        # 生成多线程控制器
        os.makedirs(temp.temp_path, exist_ok=True)

        data_group = data['children']
        count = 0
        for k_data in data_group:
            temp_k = temp.init_thread_worker(
                count, 0, 0, k_data, False, True, temp.is_single)
            temp.thread_ctrl_group.append(temp_k)
            count += 1
        # 计算已下载的大小
        temp.download_size_load()
        # 初始化下载控制器
        temp.initial_download(is_recover=True)
        temp.is_stop = True
        return temp

    def break_save(self):
        """
        记录当前状态，以dict对象返回（用于断点）
        函数行为：
            1-记录基本参数
            2-记录线程控制器参数
        """
        temp = {
            "target": self.target,
            "save_path": self.save_path,
            "param": self.param,
            "headers": self.headers,
            "cookies": self.cookies,
            "connect_timeout": self.connect_timeout,
            "read_timeout": self.read_timeout,
            "thread_num": self.thread_num,
            "save_file_path": self.save_file_path,
            "temp_path": self.temp_path,
            "file_name": self.file_name,
            "file_type": self.file_type,
            "file_ex": self.file_ex,
            "file_encode": self.file_encode,
            "is_accept_range": self.is_accept_range,
            "each_size": self.each_size,
            "total_file_size": self.total_file_size,
            # "downloaded_size": self.downloaded_size,
            "chunk_size": self.chunk_size,
            "sleep_time": self.sleep_time,
            "stop_count_limit": self.stop_count_limit,
            "link_delay": self.link_delay,
            "is_done": self.is_done,
        }
        temp_2 = []
        for t in self.thread_ctrl_group:
            t: DownloadWork
            temp_2.append(t.break_save())

        temp["children"] = temp_2

        return temp

    def cancel(self):
        """
        进行外部强行中断（切断连接）
        函数行为：
            中断所有控制线程连接
        """
        for i in self.thread_ctrl_group:
            i: DownloadWork
            i.cancel(False)

    def move_pos(self):
        self.list_index -= 1
        self.list_count -= 1

    @property
    def timeout(self):
        return self.connect_timeout, self.read_timeout

    def init_thread_worker(self, i, start, end, data, is_range=True, is_recover=False, is_single=False):
        """
        初始化线程控制器
        """
        temp = DownloadWork(i, self.target, self.session, is_single)
        if is_recover:
            temp.recover(data)
        if is_range:
            temp.set_range(start, end)
        temp.set_path(self.temp_path)
        temp.chunk_size = self.chunk_size
        temp.headers = self.headers
        temp.cookies = self.cookies
        temp.param = self.param
        temp.connect_timeout = self.connect_timeout
        temp.read_timeout = self.read_timeout
        temp.stop_count_limit = self.stop_count_limit
        temp.link_delay = self.link_delay

        return temp

    def except_call(self, id_thread):
        """
        当线程抛出error时，对线程进行重置
        """
        target = self.thread_ctrl_group[id_thread]

        temp = self.thread_pool.submit(target.reset_start)
        # 更新参数
        self.thread_future[id_thread] = temp
        self.thread_ctrl_group[id_thread] = target

        self.info_shop.SetLabel(
            f"{self.reset_count})=> in task {self.task_count},"
            f"thread {target.id} reset! Exception: {target.except_info}")
        self.reset_count += 1

    def download_size_load(self):
        """
        更新已经下载的大小和新增大小
        """
        down = 0
        for j in self.thread_ctrl_group:
            down += j.finished_data_size
        self.addon_size = down - self.downloaded_size
        self.downloaded_size = down

    def file_type_load(self):
        """
        解析respond的返回文件类型，和文件名
        """
        file_type_temp = self.res_headers.get("Content-Type")
        temp_2 = file_type_temp.split(";")
        self.file_type = temp_2[0].split("/")[0]
        self.file_ex = temp_2[0].split("/")[1]
        if len(temp_2) == 1:
            self.file_encode = None
        else:
            re_group = self.re_charset.match(temp_2[1].strip())
            if re_group is None:
                self.file_encode = None
            else:
                self.file_encode = re_group.group(1)

        file_temp_name = self.res_headers.get("Content-Disposition")
        if file_temp_name is None:
            self.file_name = parse.unquote(os.path.basename(self.real_url))
        else:
            re_group = self.re_filename.match(file_temp_name.strip())
            if re_group is None:
                self.file_name = parse.unquote(os.path.basename(self.target))
            else:
                self.file_name = re_group.group(1)

        if self.file_name.split(".").__len__() < 2:
            self.file_name = f"{self.file_name}.{self.file_ex}"

        self.save_file_path = os.path.join(self.save_path, self.file_name)

    def make_temp_file(self, path=None, is_make=True):
        # 创建临时文件夹
        if path is None:
            self.temp_path = self.save_file_path + "-temp-files"
        else:
            self.temp_path = path + "-temp-files"
        if is_make:
            os.makedirs(self.temp_path, exist_ok=True)
        return self.temp_path

    def file_size_load(self):
        """
        获取文件大小，并计算每块大小
        """
        self.total_file_size = self.res_headers.get("Content-Length")
        if self.total_file_size is None:
            self.total_file_size = 0

            self.each_size = 0
        else:
            self.total_file_size = int(self.total_file_size)
            self.each_size = math.ceil(
                self.total_file_size / self.thread_num)

    def request_range_load(self):
        """
        根据线程数量向线程控制器列表中添加线程控制器
        """
        for i in range(self.thread_num):
            start = self.each_size * i
            if i == self.thread_num - 1:
                end = int(self.total_file_size) - 1
            else:
                end = start + self.each_size - 1
            # 添加实例到线程控制组
            temp = self.init_thread_worker(i, start, end, None)

            self.thread_ctrl_group.append(temp)

    def initial_download(self, act_word="GET", is_recover=False):
        """
        初始化下载器（预加载）
        """
        # 如果是断点续传，不进行预请求
        if not is_recover:
            # 网站请求
            res = requests.request(act_word, self.target, stream=True,
                                   headers=self.headers, data=self.param, cookies=self.cookies)
            try:
                res.raise_for_status()
                # 获取实际url
                self.real_url = res.url
                self.res_headers = res.headers
                # 计算原始尺寸，计算每块的大小
                self.file_type_load()
                # 是否支持分块下载
                if self.res_headers.get("Accept-Ranges") is not None:
                    self.is_accept_range = True
                # 文件尺寸处理
                self.file_size_load()
            finally:
                res.close()

        # 多线程控制处理
        # 如果请求目标支持分块下载
        if self.is_accept_range:
            # 启动线程池
            self.thread_pool = ThreadPoolExecutor(self.thread_num)
        # 否则，进行单线程下载
        else:
            # 单线程下载
            self.thread_pool = ThreadPoolExecutor(1)
            self.is_single = True
            self.thread_num = 1

    def append_thread(self, is_recover=False):
        """
        将下载线程添加到线程池【在initial_download后调用】
        {只能在主线程添加线程到线程池？}
        """
        # 进行添加线程控制器
        # 如果为断点续传恢复，则不进行
        if not is_recover:
            if self.is_accept_range:
                # 如果请求支持单线程下载
                self.request_range_load()
            else:
                # 否则，只添加一个线程
                temp = self.init_thread_worker(
                    0, 0, self.total_file_size, None, is_single=True)
                self.thread_ctrl_group.append(temp)

        # 遍历所有线程控制器
        for target in self.thread_ctrl_group:
            target: DownloadWork
            # 将线程添加到线程池
            if is_recover:
                temp = self.thread_pool.submit(target.reset_start)
            else:
                temp = self.thread_pool.submit(target.start)
            # 记录线程对象【future】
            self.thread_future.append(temp)

    def add_to_list(self):
        """
        将下载信息添加到下载器的显示窗口中，返回index
        """
        self.list_index = self.workshop.InsertItem(
            self.list_count, f"{self.file_name}[{bit_transform(self.total_file_size, add_speed=False)}]")
        if self.is_done:
            self.workshop.SetItem(
                self.list_index, 1, f"下载完成！")
        return self.list_index

    def start_download(self):
        """
        开始下载任务【启动下载监控】
        【在append_thread后立即调用】
        """
        # 在辅助线程中运行
        try:
            time.sleep(self.link_delay)
            # 循环检查，直到全部完成,循环打印消息
            self.information_work()
        finally:
            self.thread_pool.shutdown()

        # 完成下载，进行文件合并
        self.workshop.SetItem(
            self.list_index, 1, f"合并文件中...")
        # 合并文件
        with open(self.file_name, "wb") as target:
            count = 1
            for i in range(self.thread_num):
                self.workshop.SetItem(
                    self.list_index, 1, f"合并文件中...[{count}/{self.thread_num}]")
                f: DownloadWork = self.thread_ctrl_group[i]
                with open(f.temp_file, "rb") as fp:
                    target.write(fp.read())
                count += 1
        self.workshop.SetItem(
            self.list_index, 1, f"合并文件完成！")

        shutil.rmtree(self.temp_path, True)

        self.is_done = True
        self.workshop.SetItem(
            self.list_index, 1, f"下载完成！")

    def information_work(self):
        """
        下载监控器【只在start_download中调用】
        """
        while True:
            self.download_size_load()
            # 显示数据
            self.down_speed = self.addon_size / self.sleep_time
            speed = bit_transform(self.down_speed, 1, 0.9)
            self.workshop.SetItem(
                self.list_index, 1,
                f"[{bit_transform(self.downloaded_size, add_speed=False)}/"
                f"{bit_transform(self.total_file_size, add_speed=False)}]"
                f"【{round(100 * (self.downloaded_size / int(self.total_file_size)), 4, )}%】")
            self.workshop.SetItem(self.list_index, 2, speed)
            # 退出行为
            if self.downloaded_size == self.total_file_size:
                break

            for target in self.thread_ctrl_group:
                # 检查速度为0的提交
                target: DownloadWork
                target.stop_count_work(target.check_stop())
                if target.need_stop():
                    target.cancel()
                # 重新连接，下载
                if target.is_except and target.should_reset:
                    self.except_call(target.id)
            # 循环休眠
            time.sleep(self.sleep_time)
