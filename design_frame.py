# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrameMain
###########################################################################

class MyFrameMain ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"多线程下载器", pos = wx.DefaultPosition, size = wx.Size( 700,400 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button_add = wx.Button( self, wx.ID_ANY, u"添加", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_button_add, 0, wx.ALL, 5 )

		self.m_button_start = wx.Button( self, wx.ID_ANY, u"开始", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_button_start, 0, wx.ALL, 5 )

		self.m_button_stop = wx.Button( self, wx.ID_ANY, u"暂停", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_button_stop, 0, wx.ALL, 5 )

		self.m_button_delete = wx.Button( self, wx.ID_ANY, u"删除", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_button_delete, 0, wx.ALL, 5 )

		self.m_button_setting = wx.Button( self, wx.ID_ANY, u"设置", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_button_setting, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer4, 0, wx.EXPAND, 5 )

		self.m_staticline41 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline41, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.m_listCtrl_dwonload = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_HRULES|wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VRULES )
		bSizer2.Add( self.m_listCtrl_dwonload, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )

		self.m_staticline4 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_gauge_total = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge_total.SetValue( 0 )
		bSizer3.Add( self.m_gauge_total, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer3.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText_total_size = wx.StaticText( self, wx.ID_ANY, u"[0/0]-[0%]", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_ELLIPSIZE_START )
		self.m_staticText_total_size.Wrap( -1 )

		bSizer3.Add( self.m_staticText_total_size, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer3.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText_total_speed = wx.StaticText( self, wx.ID_ANY, u"0.0 B/S", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.ST_ELLIPSIZE_START )
		self.m_staticText_total_speed.Wrap( -1 )

		self.m_staticText_total_speed.SetMinSize( wx.Size( 200,-1 ) )

		bSizer3.Add( self.m_staticText_total_speed, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer1.Add( bSizer3, 0, wx.EXPAND, 5 )

		self.m_staticline10 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline10, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText_status = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_ELLIPSIZE_MIDDLE )
		self.m_staticText_status.Wrap( -1 )

		bSizer1.Add( self.m_staticText_status, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		self.m_timer_total = wx.Timer()
		self.m_timer_total.SetOwner( self, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button_add.Bind( wx.EVT_BUTTON, self.add )
		self.m_button_start.Bind( wx.EVT_BUTTON, self.start_task )
		self.m_button_stop.Bind( wx.EVT_BUTTON, self.stop_task )
		self.m_button_delete.Bind( wx.EVT_BUTTON, self.delete )
		self.m_button_setting.Bind( wx.EVT_BUTTON, self.setting )
		self.m_listCtrl_dwonload.Bind( wx.EVT_LIST_ITEM_SELECTED, self.select_data )
		self.Bind( wx.EVT_TIMER, self.update_total, id=wx.ID_ANY )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def add( self, event ):
		event.Skip()

	def start_task( self, event ):
		event.Skip()

	def stop_task( self, event ):
		event.Skip()

	def delete( self, event ):
		event.Skip()

	def setting( self, event ):
		event.Skip()

	def select_data( self, event ):
		event.Skip()

	def update_total( self, event ):
		event.Skip()


###########################################################################
## Class MyDialog_task_info
###########################################################################

class MyDialog_task_info ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"新建任务", pos = wx.DefaultPosition, size = wx.Size( 494,726 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"目标网址", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer6.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textCtrl_target_url = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_textCtrl_target_url, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_button10 = wx.Button( self, wx.ID_ANY, u"预加载", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_button10, 0, wx.ALL, 5 )


		bSizer5.Add( bSizer6, 0, wx.EXPAND, 5 )

		self.m_staticline5 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer5.Add( self.m_staticline5, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"连接超时（ms）", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		bSizer10.Add( self.m_staticText7, 0, wx.ALL, 5 )

		self.m_textCtrl_connect_timeout = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_textCtrl_connect_timeout, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"读取超时（ms）", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		bSizer10.Add( self.m_staticText8, 0, wx.ALL, 5 )

		self.m_textCtrl_read_time_out = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_textCtrl_read_time_out, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"线程数量", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		bSizer10.Add( self.m_staticText9, 0, wx.ALL, 5 )

		self.m_textCtrl_thread_num = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_textCtrl_thread_num, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"单次下载包大小（字节）", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		bSizer10.Add( self.m_staticText10, 0, wx.ALL, 5 )

		self.m_textCtrl_chunk_size = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_textCtrl_chunk_size, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText111 = wx.StaticText( self, wx.ID_ANY, u"状态轮询间隔（秒）", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText111.Wrap( -1 )

		bSizer10.Add( self.m_staticText111, 0, wx.ALL, 5 )

		self.m_textCtrl_loop_sleep = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_textCtrl_loop_sleep, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"连接延时(秒)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		bSizer10.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.m_textCtrl_connect_delay = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_textCtrl_connect_delay, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, u"线程重置触发阈值", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )

		bSizer10.Add( self.m_staticText13, 0, wx.ALL, 5 )

		self.m_textCtrl_thread_reset_limit = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_textCtrl_thread_reset_limit, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText16 = wx.StaticText( self, wx.ID_ANY, u"文件大小（B）", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )

		bSizer10.Add( self.m_staticText16, 0, wx.ALL, 5 )

		self.m_textCtrl_file_size = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		bSizer10.Add( self.m_textCtrl_file_size, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer9.Add( bSizer10, 1, wx.EXPAND, 5 )

		self.m_staticline8 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer9.Add( self.m_staticline8, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"headers", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		bSizer12.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_button_header_add = wx.Button( self, wx.ID_ANY, u"添加", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.m_button_header_add, 0, wx.ALL, 5 )

		self.m_button_header_remove = wx.Button( self, wx.ID_ANY, u"删除", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.m_button_header_remove, 0, wx.ALL, 5 )


		bSizer11.Add( bSizer12, 0, wx.EXPAND, 5 )

		self.m_listCtrl_headers = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_HRULES|wx.LC_REPORT|wx.LC_VRULES )
		bSizer11.Add( self.m_listCtrl_headers, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticline9 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer11.Add( self.m_staticline9, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"cookies", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer14.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_button_cookie_add = wx.Button( self, wx.ID_ANY, u"添加", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.m_button_cookie_add, 0, wx.ALL, 5 )

		self.m_button_Cookie_remove = wx.Button( self, wx.ID_ANY, u"删除", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.m_button_Cookie_remove, 0, wx.ALL, 5 )


		bSizer11.Add( bSizer14, 0, wx.EXPAND, 5 )

		self.m_listCtrl_cookies = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_EDIT_LABELS|wx.LC_HRULES|wx.LC_REPORT|wx.LC_VRULES )
		bSizer11.Add( self.m_listCtrl_cookies, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer13 = wx.BoxSizer( wx.VERTICAL )


		bSizer11.Add( bSizer13, 1, wx.EXPAND, 5 )


		bSizer9.Add( bSizer11, 1, wx.EXPAND, 5 )


		bSizer5.Add( bSizer9, 1, wx.EXPAND, 5 )

		self.m_staticline7 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer5.Add( self.m_staticline7, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"保存位置", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		bSizer8.Add( self.m_staticText11, 0, wx.ALL, 5 )

		bSizer141 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_textCtrl_save = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		bSizer141.Add( self.m_textCtrl_save, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_button_save = wx.Button( self, wx.ID_ANY, u"设置路径", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer141.Add( self.m_button_save, 0, wx.ALL, 5 )


		bSizer8.Add( bSizer141, 1, wx.EXPAND, 5 )


		bSizer5.Add( bSizer8, 0, wx.ALIGN_RIGHT|wx.EXPAND, 5 )

		self.m_staticline6 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer5.Add( self.m_staticline6, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer30 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText_size = wx.StaticText( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_size.Wrap( -1 )

		bSizer30.Add( self.m_staticText_size, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		m_sdbSizer1 = wx.StdDialogButtonSizer()
		self.m_sdbSizer1OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer1.AddButton( self.m_sdbSizer1OK )
		self.m_sdbSizer1Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer1.AddButton( self.m_sdbSizer1Cancel )
		m_sdbSizer1.Realize();

		bSizer30.Add( m_sdbSizer1, 0, wx.EXPAND, 5 )


		bSizer5.Add( bSizer30, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer5 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button10.Bind( wx.EVT_BUTTON, self.per_load )
		self.m_button_header_add.Bind( wx.EVT_BUTTON, self.header_add )
		self.m_button_header_remove.Bind( wx.EVT_BUTTON, self.header_remove )
		self.m_listCtrl_headers.Bind( wx.EVT_LIST_ITEM_RIGHT_CLICK, self.header_change )
		self.m_button_cookie_add.Bind( wx.EVT_BUTTON, self.cookie_add )
		self.m_button_Cookie_remove.Bind( wx.EVT_BUTTON, self.cookie_remove )
		self.m_listCtrl_cookies.Bind( wx.EVT_LIST_ITEM_RIGHT_CLICK, self.cookie_change )
		self.m_button_save.Bind( wx.EVT_BUTTON, self.save )
		self.m_sdbSizer1Cancel.Bind( wx.EVT_BUTTON, self.cancel_work )
		self.m_sdbSizer1OK.Bind( wx.EVT_BUTTON, self.ok_work )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def per_load( self, event ):
		event.Skip()

	def header_add( self, event ):
		event.Skip()

	def header_remove( self, event ):
		event.Skip()

	def header_change( self, event ):
		event.Skip()

	def cookie_add( self, event ):
		event.Skip()

	def cookie_remove( self, event ):
		event.Skip()

	def cookie_change( self, event ):
		event.Skip()

	def save( self, event ):
		event.Skip()

	def cancel_work( self, event ):
		event.Skip()

	def ok_work( self, event ):
		event.Skip()


###########################################################################
## Class MyDialog_setting
###########################################################################

class MyDialog_setting ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 484,574 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer22 = wx.BoxSizer( wx.VERTICAL )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"连接超时（ms）", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		bSizer10.Add( self.m_staticText7, 0, wx.ALL, 5 )

		self.m_textCtrl_connect_timeout = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_textCtrl_connect_timeout, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"读取超时（ms）", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		bSizer10.Add( self.m_staticText8, 0, wx.ALL, 5 )

		self.m_textCtrl_read_time_out = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_textCtrl_read_time_out, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"线程数量", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		bSizer10.Add( self.m_staticText9, 0, wx.ALL, 5 )

		self.m_textCtrl_thread_num = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_textCtrl_thread_num, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"单次下载包大小（字节）", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		bSizer10.Add( self.m_staticText10, 0, wx.ALL, 5 )

		self.m_textCtrl_chunk_size = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_textCtrl_chunk_size, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText111 = wx.StaticText( self, wx.ID_ANY, u"状态轮询间隔（秒）", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText111.Wrap( -1 )

		bSizer10.Add( self.m_staticText111, 0, wx.ALL, 5 )

		self.m_textCtrl_loop_sleep = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_textCtrl_loop_sleep, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"连接延时(秒)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		bSizer10.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.m_textCtrl_connect_delay = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_textCtrl_connect_delay, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, u"线程重置触发阈值", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )

		bSizer10.Add( self.m_staticText13, 0, wx.ALL, 5 )

		self.m_textCtrl_thread_reset_limit = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_textCtrl_thread_reset_limit, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText16 = wx.StaticText( self, wx.ID_ANY, u"预加载方法", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )

		bSizer10.Add( self.m_staticText16, 0, wx.ALL, 5 )

		m_choice_verbChoices = [ u"GET", u"PUT", u"HEAD", u"OPTIONS", u"POST", u"DELETE", u"PATCH" ]
		self.m_choice_verb = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_verbChoices, 0 )
		self.m_choice_verb.SetSelection( 0 )
		bSizer10.Add( self.m_choice_verb, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer9.Add( bSizer10, 1, wx.EXPAND, 5 )

		self.m_staticline8 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer9.Add( self.m_staticline8, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"headers", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		bSizer12.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_button_header_add = wx.Button( self, wx.ID_ANY, u"添加", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.m_button_header_add, 0, wx.ALL, 5 )

		self.m_button_header_remove = wx.Button( self, wx.ID_ANY, u"删除", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.m_button_header_remove, 0, wx.ALL, 5 )


		bSizer11.Add( bSizer12, 0, wx.EXPAND, 5 )

		self.m_listCtrl_headers = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_HRULES|wx.LC_REPORT|wx.LC_VRULES )
		bSizer11.Add( self.m_listCtrl_headers, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_staticline9 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer11.Add( self.m_staticline9, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"cookies", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer14.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_button_cookie_add = wx.Button( self, wx.ID_ANY, u"添加", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.m_button_cookie_add, 0, wx.ALL, 5 )

		self.m_button_Cookie_remove = wx.Button( self, wx.ID_ANY, u"删除", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.m_button_Cookie_remove, 0, wx.ALL, 5 )


		bSizer11.Add( bSizer14, 0, wx.EXPAND, 5 )

		self.m_listCtrl_cookies = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_EDIT_LABELS|wx.LC_HRULES|wx.LC_REPORT|wx.LC_VRULES )
		bSizer11.Add( self.m_listCtrl_cookies, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer13 = wx.BoxSizer( wx.VERTICAL )


		bSizer11.Add( bSizer13, 1, wx.EXPAND, 5 )


		bSizer9.Add( bSizer11, 1, wx.EXPAND, 5 )


		bSizer22.Add( bSizer9, 1, wx.EXPAND, 5 )

		self.m_staticline16 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer22.Add( self.m_staticline16, 0, wx.EXPAND |wx.ALL, 5 )

		m_sdbSizer3 = wx.StdDialogButtonSizer()
		self.m_sdbSizer3OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer3.AddButton( self.m_sdbSizer3OK )
		self.m_sdbSizer3Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer3.AddButton( self.m_sdbSizer3Cancel )
		m_sdbSizer3.Realize();

		bSizer22.Add( m_sdbSizer3, 0, wx.ALIGN_RIGHT, 5 )


		self.SetSizer( bSizer22 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button_header_add.Bind( wx.EVT_BUTTON, self.header_add )
		self.m_button_header_remove.Bind( wx.EVT_BUTTON, self.header_remove )
		self.m_listCtrl_headers.Bind( wx.EVT_LIST_ITEM_RIGHT_CLICK, self.header_change )
		self.m_button_cookie_add.Bind( wx.EVT_BUTTON, self.cookie_add )
		self.m_button_Cookie_remove.Bind( wx.EVT_BUTTON, self.cookie_remove )
		self.m_listCtrl_cookies.Bind( wx.EVT_LIST_ITEM_RIGHT_CLICK, self.cookie_change )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def header_add( self, event ):
		event.Skip()

	def header_remove( self, event ):
		event.Skip()

	def header_change( self, event ):
		event.Skip()

	def cookie_add( self, event ):
		event.Skip()

	def cookie_remove( self, event ):
		event.Skip()

	def cookie_change( self, event ):
		event.Skip()


###########################################################################
## Class MyDialog_add_data
###########################################################################

class MyDialog_add_data ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 421,204 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer15 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, u"名称", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )

		bSizer15.Add( self.m_staticText14, 0, wx.ALL, 5 )

		self.m_textCtrl_key = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer15.Add( self.m_textCtrl_key, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText15 = wx.StaticText( self, wx.ID_ANY, u"值", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )

		bSizer15.Add( self.m_staticText15, 0, wx.ALL, 5 )

		self.m_textCtrl_value = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer15.Add( self.m_textCtrl_value, 0, wx.ALL|wx.EXPAND, 5 )

		m_sdbSizer2 = wx.StdDialogButtonSizer()
		self.m_sdbSizer2OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer2.AddButton( self.m_sdbSizer2OK )
		self.m_sdbSizer2Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer2.AddButton( self.m_sdbSizer2Cancel )
		m_sdbSizer2.Realize();

		bSizer15.Add( m_sdbSizer2, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer15 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_sdbSizer2Cancel.Bind( wx.EVT_BUTTON, self.cancel_work )
		self.m_sdbSizer2OK.Bind( wx.EVT_BUTTON, self.ok_work )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def cancel_work( self, event ):
		event.Skip()

	def ok_work( self, event ):
		event.Skip()


