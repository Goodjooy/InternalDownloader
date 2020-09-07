# -*- coding: utf-8 -*-
# @Author: FrozenString
# @Date:   2020-08-22 16:56:00
# @Last Modified by:   FrozenString
# @Last Modified time: 2020-09-07 12:28:45

import os
import sys

import wx

from main_frame import MainFrame

if __name__ == "__main__":
    work_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
    app = wx.App()
    f = MainFrame(None, work_path)
    f.Show()
    app.MainLoop()
