# -*- coding: utf-8 -*-
# @Author: FrozenString
# @Date:   2020-08-22 19:09:46
# @Last Modified by:   FrozenString
# @Last Modified time: 2020-09-07 12:29:04


import os
import time

import requests


# from struct_class import ThreadData


class ZeroDownloadError(Exception):
    pass


class CancelledException(Exception):
    pass


class DownloadWork(object):
    def __init__(self, thread_count, url, session: requests.Session, is_single=False) -> None:
        self.session = session
        self.id = thread_count
        self.url = url
        self.is_single = is_single

        self.range = tuple()
        self.target_range = tuple()
        self.temp_path = str()
        self.temp_file = str()

        self.finished_data_size = 0
        self.last_downloaded = 0
        self.is_done = False

        self.param = {}
        self._headers = {}
        self._cookies = {}
        self.connect_timeout = 5
        self.read_timeout = 5
        self.chunk_size = 1024

        self.resp = None
        self.download_iter = None

        self.target_url = ""

        self.resp_headers = {}
        self.resp_size = 0
        self.resp_range = ()

        self.fp = None

        self.is_release_link = False

        self.is_stopped = False
        self.stop_count_limit = 10
        self.stop_count = 0

        self.link_delay = 1

        self.is_except = False

        self.is_recover = False
        self.should_reset = False

        self.except_info = None

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        if isinstance(value, dict):
            for key, value in value.items():
                self._headers[key] = value
        else:
            return

    @property
    def cookies(self):
        return self._cookies

    @cookies.setter
    def cookies(self, value):
        if isinstance(value, dict):
            for key, value in value.items():
                self._cookies[key] = value
        else:
            return

    @property
    def timeout(self):
        return self.connect_timeout, self.read_timeout

    def check_stop(self):
        if self.last_downloaded == 0:
            if self.finished_data_size > 0:
                self.last_downloaded = self.finished_data_size
                return True
            else:
                return False
        elif self.last_downloaded < self.finished_data_size:
            self.last_downloaded = self.finished_data_size
            return False
        else:
            return True

    def stop_count_work(self, is_stop):
        if is_stop:
            self.is_stopped = True
            self.stop_count += 1
        else:
            self.is_stopped = False
            self.stop_count = 0

    def need_stop(self):
        if self.stop_count >= self.stop_count_limit and self.is_stopped:
            return True
        else:
            return False

    def set_range(self, start, end, is_init=True):
        if is_init:
            self.target_range = (start, end)
        self.range = (start, end)
        self.headers = (
            {'Range': 'bytes=%d-%d' % (self.range[0], self.range[1])})

    def set_path(self, temp_path):
        self.temp_path = temp_path
        self.temp_file = os.path.join(self.temp_path, f"tmp-{self.id}.tp")

    def prepare(self, is_reset=False):
        """准备阶段"""
        write_code = "wb"
        # 如果是重置或者断点徐传
        if is_reset:
            write_code = "ab"
            self.set_range(self.finished_data_size +
                           self.target_range[0], self.target_range[1], is_init=False)
        if self.is_single:
            del self._headers["Range"]

        time.sleep(self.link_delay)
        self.resp = self.session.get(self.url, headers=self.headers,
                                     stream=True, timeout=self.timeout, cookies=self.cookies, params=self.param)
        self.resp.raise_for_status()

        self.resp_headers = self.resp.headers
        self.resp_size = self.resp_headers.get("Content-Length")
        if is_reset:
            self.resp_size = int(self.resp_size) + self.finished_data_size
        self.target_url = self.resp.url
        # 打开文件，while循环，下载完成后退出
        self.fp = open(self.temp_file, write_code)
        # 下载迭代器，None为有数据就写入
        self.download_iter = self.resp.iter_content(chunk_size=self.chunk_size)

    def end(self):
        # 等待文件写入完成
        if self.fp is not None:
            self.fp.flush()
            os.fsync(self.fp)
            self.fp.close()
        # 关闭连接
        if self.is_release_link is False and self.resp is not None:
            self.resp.close()
            self.is_release_link = True

    def run(self):
        while True:
            try:

                data = next(self.download_iter)

            except StopIteration:
                if self.is_release_link:
                    raise CancelledException("cancel! in %d" % self.id)
                else:
                    break
            else:
                # 如果数据长度为0，触发错误，退出
                if len(data) == 0:
                    raise ZeroDownloadError("下载的数据大小为0！")
                # 写入数据
                self.finished_data_size += len(data)
                self.fp.write(data)

                if self.finished_data_size == self.resp_size:
                    self.is_done = True
                    break

    def cancel(self, reset=True):
        """
        reset为False 取消后不重置
        """
        if self.resp is not None:
            self.resp.close()
        self.is_release_link = True
        if reset:
            self.should_reset = True
        else:
            self.should_reset = False

    def start(self):
        """开始干活"""
        try:
            # 准备工作
            self.prepare()
            # 主要过程
            self.run()
        except Exception as t:
            self.except_info = t
            self.is_except = True
        finally:
            # print("end")
            self.end()

    def reset_start(self):
        """
        在断点续传和重置时调用
        """
        try:
            self.is_release_link = False
            self.is_except = False
            self.is_stopped = False
            self.stop_count = 0

            # 准备工作
            self.prepare(True)
            # 主要过程
            self.run()
        except Exception as t:
            self.except_info = t
            self.is_except = True
        finally:
            # print("end")
            self.end()

    def break_save(self):
        return {
            "range": self.target_range,
            "finished_data_size": self.finished_data_size,
            "is_done": self.is_done,
            "is_recover": True
        }

    def recover(self, data):
        self.target_range = data["range"]
        self.finished_data_size = data["finished_data_size"]
        self.is_done = data["is_done"]
        self.is_recover = data['is_recover']
