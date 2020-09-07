# -*- coding: utf-8 -*-
# @Author: FrozneString
# @Date:   2020-08-27 19:25:03
# @Last Modified by:   FrozenString
# @Last Modified time: 2020-09-07 12:28:33


from design_frame import MyDialog_add_data

class DataEntry(MyDialog_add_data):
    def __init__(self,parent) -> None:
        super().__init__(parent)
        self.is_ok=False
    def getvalue(self):
        return  self.m_textCtrl_value.GetValue()
    def getkey(self): 
        return self.m_textCtrl_key.GetValue()
    
    def ok_work(self, event):
        self.is_ok=True
        self.Destroy()
        
