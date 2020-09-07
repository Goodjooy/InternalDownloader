# -*- coding: utf-8 -*-
# @Author: FrozenString
# @Date:   2020-08-27 17:51:33
# @Last Modified by:   FrozenString
# @Last Modified time: 2020-09-07 12:28:50

import os
from threading import Thread
import json
import shutil

import wx

from design_frame import MyFrameMain
from perdownload import PerDownload
from struct_class import DownloadCtrl, bit_transform


class MainFrame(MyFrameMain):
    def __init__(self, parent, work_path) -> None:
        super().__init__(parent)

        self.work_path = work_path

        w = self.m_listCtrl_dwonload.GetSize()[0]
        self.m_listCtrl_dwonload.InsertColumn(
            0, "文件名称", wx.LIST_FORMAT_CENTER, width=int(w / 2))
        self.m_listCtrl_dwonload.InsertColumn(
            1, "下载进度", wx.LIST_FORMAT_LEFT, width=int(w / 2.75))
        self.m_listCtrl_dwonload.InsertColumn(
            2, "速度", wx.LIST_FORMAT_LEFT, width=wx.LIST_AUTOSIZE_USEHEADER)
        try:
            with open(os.path.join(self.work_path, "setting.json"), "r")as f:
                self.setting_info = json.load(f)
        except Exception as t:
            self.setting_info = None
            self.m_staticText_status.SetLabel(str(t))

        self.worker_group = []
        self.thread_group = []

        self.next_index = 0

        self.total_size = 0
        self.total_downloaded = 0
        self.total_speed = 0

        self.select_index = -1

        self.m_timer_total.Start()
        self.init_load()

    def init_load(self):
        recover_dir = os.path.join(self.work_path, "recover_work")
        target_groups = os.listdir(recover_dir)
        for filename in target_groups:
            target = os.path.join(recover_dir, filename)
            if os.path.isfile(target) and target.lower().endswith(".json"):
                self.recover_from_file(target)

    def recover_from_file(self, filename):
        with open(filename, "r") as target:
            temp = json.load(target)
            ctrl = DownloadCtrl.recover_task(temp, self.m_listCtrl_dwonload, self.next_index, len(
                self.worker_group), self.m_staticText_status)
            self.append_ctrl(ctrl)

    def append_ctrl(self, ctrl: DownloadCtrl):
        self.next_index = ctrl.add_to_list() + 1

        thread = Thread(target=ctrl.start_download)
        thread.setDaemon(True)
        ctrl.watch_thread = thread
        self.worker_group.append(ctrl)
        self.thread_group.append(thread)
        return thread

    def reset_ctrl(self, index):
        ctrl: DownloadCtrl = self.worker_group[index]
        thread = Thread(target=ctrl.start_download)
        thread.setDaemon(True)
        ctrl.watch_thread = thread
        self.worker_group[index] = ctrl
        self.thread_group[index] = thread
        return thread

    def add(self, event):
        temp = DownloadCtrl(
            "", os.getcwd(), self.m_listCtrl_dwonload, self.next_index, len(self.worker_group),
            self.m_staticText_status, default_setting=self.setting_info)
        dialog = PerDownload(self, temp)
        dialog.ShowModal()

        if dialog.is_ok:
            temp = dialog.get_download()

            thread = self.append_ctrl(temp)
            temp.append_thread(False)
            thread.start()

    def start_task(self, event):
        target_index = self.m_listCtrl_dwonload.GetFocusedItem()
        target: DownloadCtrl = self.worker_group[target_index]
        if target.is_done:
            return
        target.append_thread(True)
        if target.watch_thread is not None:
            target.watch_thread.start()
        self.worker_group[target_index].is_stop = False
        self.select_data(None, target_index)

    def stop_task(self, event):
        target_index = self.m_listCtrl_dwonload.GetFocusedItem()
        target: DownloadCtrl = self.worker_group[target_index]

        target.cancel()
        self.reset_ctrl(target_index)
        self.worker_group[target_index].is_stop = True
        self.select_data(None, target_index)

    def delete(self, event):
        target_index = self.m_listCtrl_dwonload.GetFocusedItem()

        del self.worker_group[target_index]
        del self.thread_group[target_index]
        self.m_listCtrl_dwonload.DeleteItem(target_index)

        for i in range(target_index, len(self.worker_group)):
            target: DownloadCtrl = self.worker_group[i]
            target.move_pos()
        self.next_index -= 1

    def update_total(self, event):
        active = list(filter(lambda x: not x.is_done, self.worker_group))
        self.total_size = 0
        self.total_downloaded = 0
        self.total_speed = 0
        for i in active:
            self.total_size += i.total_file_size
            self.total_downloaded += i.downloaded_size
            self.total_speed += i.down_speed
        if self.total_size == 0:
            return
        present = 100 * (self.total_downloaded / self.total_size)

        self.m_gauge_total.SetValue(round(present))
        self.m_staticText_total_size.SetLabel(
            f"[{bit_transform(self.total_downloaded, add_speed=False)}"
            f"/{bit_transform(self.total_size, add_speed=False)}]-[{round(present, 2)}%]")
        self.m_staticText_total_speed.SetLabel(
            "%s" % bit_transform(self.total_speed))

    def select_data(self, event, index=-1):

        if event is None:
            self.select_index = index
        else:
            self.select_index = event.GetSelection()
        target: DownloadCtrl = self.worker_group[self.select_index]
        if target.is_done:
            self.m_button_start.Enable(False)
            self.m_button_stop.Enable(False)
            self.m_button_delete.Enable(True)
        if target.is_stop:
            self.m_button_start.Enable(True)
            self.m_button_stop.Enable(False)
            self.m_button_delete.Enable(True)
        else:
            self.m_button_start.Enable(False)
            self.m_button_stop.Enable(True)
            self.m_button_delete.Enable(False)

    def setting(self, event):
        pass

    def Destroy(self):
        try:
            target_path = os.path.join(self.work_path, f"recover_work")
            shutil.rmtree(target_path, True)
            os.makedirs(target_path)

            for i in self.worker_group:
                i: DownloadCtrl
                i.download_size_load()
                i.cancel()
                break_data = i.break_save()
                with open(os.path.join(target_path, f"{i.task_count}.json"), "w") as target:
                    json.dump(break_data, target, indent=4)
        finally:
            return super().Destroy()
