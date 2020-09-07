from design_frame import MyDialog_setting
from perdownload import PerDownload
from struct_class import DownloadCtrl


class SettingFrame(PerDownload):
    def __init__(self, parent, setting_info):
        self.download: DownloadCtrl = DownloadCtrl("", "", None, None, None, None, None, setting_info)
        super(SettingFrame, self).__init__(parent, self.download)
        self.setting_info = setting_info
