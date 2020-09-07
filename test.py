# -*- coding: utf-8 -*-
# @Author: FrozneString
# @Date:   2020-08-23 15:39:42
# @Last Modified by:   FrozneString
# @Last Modified time: 2020-08-28 15:04:06

import os
from threading import Thread

import wx

from design_frame import MyDialog_task_info, MyFrameMain
from main_frame import MainFrame
from struct_class import DownloadCtrl


class down_info(MyDialog_task_info): 
    def __init__(self, parent, downloader: DownloadCtrl) -> None:
        super().__init__(parent)
        self.downloader = downloader

        self.save_path=""
        self.file_name=""
        self.wild_card=""

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
        self.m_textCtrl_target_url.SetValue(str(self.downloader.real_url))
        self.m_textCtrl_save.SetLabel(str(self.downloader.save_path))

        # self.downloader.hearders
        # self.downloader.cookies
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

    def set_header(self):
        self.m_listCtrl_headers.InsertColumn(0, "名称", wx.LIST_FORMAT_CENTRE)
        self.m_listCtrl_headers.InsertColumn(
            1, "值", width=wx.LIST_AUTOSIZE_USEHEADER)

        for k, v in self.header.items():
            self.header_name.append(k)
            index = self.m_listCtrl_headers.InsertItem(self.header_count, k)
            self.header_count = index+1
            self.m_listCtrl_headers.SetItem(index, 1, v)

    def set_cookie(self):
        self.m_listCtrl_cookies.InsertColumn(0, "名称", wx.LIST_FORMAT_CENTRE)
        self.m_listCtrl_cookies.InsertColumn(
            1, "值", width=wx.LIST_AUTOSIZE_USEHEADER)

        for k, v in self.cookie.items():
            self.cookie_name.append(k)
            index = self.m_listCtrl_cookies.InsertItem(self.cookie_count, k)
            self.cookie_count = index+1
            self.m_listCtrl_cookies.SetItem(index, 1, v)

    def per_load(self, event):
        self.downloader.target=self.m_textCtrl_target_url.GetValue()
        self.downloader.initial_download()

        save_path = os.path.split(self.downloader.save_path)[0]
        file_name = self.downloader.file_name
        file_ex = os.path.splitext(file_name)[-1]

        self.wild_card=f"{self.downloader.file_type}-[{self.downloader.file_ex}]({file_ex})|{file_ex}"
        self.save_path=save_path
        self.file_name=file_name

        self.set_value()
        
    def header_add(self, event):
        index=self.header_count
        

    def header_change(self, event):
        index = event.GetIndex()
        k = self.header_name[index]
        v = self.header[k]
        dailog = wx.TextEntryDialog(self, f"修改请求头中{k}的值", value=v)
        if dailog.ShowModal() == wx.ID_OK:
            v=dailog.GetValue()
            self.header[k]=v
            self.m_listCtrl_headers.SetItem(index,1,v)
    
    def cookie_change(self, event):
        index = event.GetIndex()
        k = self.cookie_name[index]
        v = self.cookie[k]
        dailog = wx.TextEntryDialog(self, f"修改COOKIE中{k}的值", value=v)
        if dailog.ShowModal() == wx.ID_OK:
            v=dailog.GetValue()
            self.cookie[k]=v
            self.m_listCtrl_cookies.SetItem(index,1,v)


def main():
    app = wx.App()
    f = MainFrame(None)
    f.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
