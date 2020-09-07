# -*- coding: utf-8 -*-
# @Author: FrozenString
# @Date:   2020-08-27 19:18:45
# @Last Modified by:   FrozenString
# @Last Modified time: 2020-09-07 12:28:24


import os

import wx

from data_entry import DataEntry
from design_frame import MyDialog_task_info
from struct_class import DownloadCtrl, bit_transform


class PerDownload(MyDialog_task_info):
    def __init__(self, parent, downloader: DownloadCtrl) -> None:
        super().__init__(parent)
        self.downloader = downloader
        self.is_load = False
        self.is_ok = False
        self.is_set_temp = False

        self.save_path = ""

        self.file_name = ""
        self.wild_card = ""

        self.header = self.downloader.headers
        self.header_name = []
        self.header_count = 0
        self.cookie = self.downloader.cookies
        self.cookie_name = []
        self.cookie_count = 0
        self.set_value()
        self.set_header()
        self.set_cookie()

    def set_value(self):
        self.m_textCtrl_target_url.SetValue(str(self.downloader.target))
        self.m_textCtrl_save.SetValue(str(self.downloader.save_file_path))
        # self.m_textCtrl_temp.SetValue(str(self.downloader.temp_path))
        self.m_textCtrl_connect_timeout.SetValue(
            str(self.downloader.connect_timeout))
        self.m_textCtrl_read_time_out.SetValue(
            str(self.downloader.read_timeout))
        self.m_textCtrl_thread_num.SetValue(str(self.downloader.thread_num))

        self.m_textCtrl_chunk_size.SetValue(str(self.downloader.chunk_size))
        self.m_textCtrl_loop_sleep.SetValue(str(self.downloader.sleep_time))
        self.m_textCtrl_thread_reset_limit.SetValue(
            str(self.downloader.stop_count_limit))
        self.m_textCtrl_connect_delay.SetValue(str(self.downloader.link_delay))
        self.m_staticText_size.SetLabel(
            f"文件大小：{bit_transform(self.downloader.total_file_size,add_speed=False)}")

    def get_value(self):
        self.downloader.save_file_path = self.m_textCtrl_save.GetValue()
        # self.downloader.temp_path = self.m_textCtrl_temp.GetValue()
        self.downloader.connect_timeout = float(self.m_textCtrl_connect_timeout.GetValue())
        self.downloader.read_timeout = float(self.m_textCtrl_read_time_out.GetValue())

        self.downloader.thread_num = int(self.m_textCtrl_thread_num.GetValue())

        self.downloader.chunk_size = int(self.m_textCtrl_chunk_size.GetValue())
        self.downloader.sleep_time = float(self.m_textCtrl_loop_sleep.GetValue())
        self.downloader.stop_count_limit = int(self.m_textCtrl_thread_reset_limit.GetValue())
        self.downloader.link_delay = float(self.m_textCtrl_connect_delay.GetValue())

        self.downloader.headers = self.header
        self.downloader.cookies = self.cookie

        self.downloader.make_temp_file()

    def set_header(self):
        self.m_listCtrl_headers.InsertColumn(0, "名称", wx.LIST_FORMAT_CENTRE)
        self.m_listCtrl_headers.InsertColumn(
            1, "值", width=wx.LIST_AUTOSIZE_USEHEADER)

        for k, v in self.header.items():
            self.insert_header(k, v)

    def set_cookie(self):
        self.m_listCtrl_cookies.InsertColumn(0, "名称", wx.LIST_FORMAT_CENTRE)
        self.m_listCtrl_cookies.InsertColumn(
            1, "值", width=wx.LIST_AUTOSIZE_USEHEADER)

        for k, v in self.cookie.items():
            self.insert_cookie(k, v)

    def insert_header(self, k, v):
        self.header_name.append(k)
        index = self.m_listCtrl_headers.InsertItem(self.header_count, k)
        self.header_count = index + 1
        self.m_listCtrl_headers.SetItem(index, 1, v)

    def insert_cookie(self, k, v):
        self.cookie_name.append(k)
        index = self.m_listCtrl_cookies.InsertItem(self.cookie_count, k)
        self.cookie_count = index + 1
        self.m_listCtrl_cookies.SetItem(index, 1, v)

    def per_load(self, event):
        try:
            self.downloader.target = self.m_textCtrl_target_url.GetValue()
            self.get_value()
            self.downloader.initial_download()

            save_path = os.path.split(self.downloader.save_file_path)[0]
            file_name = self.downloader.file_name
            file_ex = os.path.splitext(file_name)[-1]

            self.wild_card = f"{self.downloader.file_type}-[{self.downloader.file_ex}]({file_ex})|{file_ex}"
            self.save_path = save_path
            self.file_name = file_name

            if self.downloader.is_single:
                self.m_textCtrl_thread_num.Enable(False)
                wx.MessageBox(f"网址：【{self.downloader.target}】不支持多线程下载，将使用单线程下载", "提示", wx.ICON_INFORMATION)

            else:
                self.m_textCtrl_thread_num.Enable(True)

            self.set_value()
        except Exception as err:
            wx.MessageBox(f"预加载时出错，请检查目标网址是否正确和网络连接状态；\n【{str(err)}】", "预加载错误", wx.ICON_ERROR)
        else:
            self.is_load = True

    def header_add(self, event):
        dialog = DataEntry(self)
        dialog.ShowModal()
        if dialog.is_ok:
            if dialog.getkey() not in self.header_name:
                self.insert_header(dialog.getkey(), dialog.getvalue())
                self.header[dialog.getkey()] = dialog.getvalue()
            else:
                wx.MessageBox(f"名称：{dialog.getkey()} 已经存在！")

    def header_remove(self, event):
        index = item = self.m_listCtrl_headers.GetFocusedItem()

        self.m_listCtrl_headers.DeleteItem(item)
        k = self.header_name[index]
        del self.header[k]
        del self.header_name[index]
        self.header_count -= 1

    def header_change(self, event):
        index = event.GetIndex()
        k = self.header_name[index]
        v = self.header[k]
        dialog = wx.TextEntryDialog(self, f"修改请求头中{k}的值", value=v)
        if dialog.ShowModal() == wx.ID_OK:
            v = dialog.GetValue()
            self.header[k] = v
            self.m_listCtrl_headers.SetItem(index, 1, v)

    def cookie_add(self, event):
        dialog = DataEntry(self)
        dialog.ShowModal()
        if dialog.is_ok:
            if dialog.getkey() not in self.cookie_name:
                self.insert_cookie(dialog.getkey(), dialog.getvalue())
                self.cookie[dialog.getkey()] = dialog.getvalue()
            else:
                wx.MessageBox(f"名称：{dialog.getkey()} 已经存在！")

    def cookie_change(self, event):
        index = event.GetIndex()
        k = self.cookie_name[index]
        v = self.cookie[k]
        dialog = wx.TextEntryDialog(self, f"修改COOKIE中{k}的值", value=v)
        if dialog.ShowModal() == wx.ID_OK:
            v = dialog.GetValue()
            self.cookie[k] = v
            self.m_listCtrl_cookies.SetItem(index, 1, v)

    def cookie_remove(self, event):
        index = item = self.m_listCtrl_cookies.GetFocusedItem()

        self.m_listCtrl_cookies.DeleteItem(item)
        k = self.cookie_name[index]
        del self.cookie[k]
        del self.cookie_name[index]
        self.header_count -= 1

    def ok_work(self, event):
        if self.is_load:
            self.is_ok = True
            self.get_value()
            self.Destroy()
        else:
            wx.MessageBox("请先进行预加载！")

    def save(self, event):
        if not self.is_load:
            wx.MessageBox("请先进行预加载！")
            return
        dialog = wx.FileDialog(self, "保存文件", self.save_path, self.file_name, self.wild_card,
                               wx.FD_SAVE | wx.FD_CHANGE_DIR | wx.FD_OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            self.save_path = dialog.GetPath()
            self.file_name = dialog.GetFilename()

            self.m_textCtrl_save.SetValue(self.save_path)

            self.downloader.save_file_path = self.save_path
            self.downloader.file_name = self.file_name

    def get_download(self):
        return self.downloader
