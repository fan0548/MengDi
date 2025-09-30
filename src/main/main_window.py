# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QListWidget, QListWidgetItem, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt
# get_users_from_path 将在下一步中创建
from src.main.wechat_reader import get_user_list, get_users_from_path
from src.main.chat_window import ChatWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.chat_win = None
        self.load_mode = None  # 'online' or 'manual'
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('微信聊天记录查看器')
        self.setGeometry(300, 300, 500, 350)

        layout = QVBoxLayout()

        title_label = QLabel('微信聊天记录本地查看工具')
        title_label.setAlignment(Qt.AlignCenter)
        font = title_label.font()
        font.setPointSize(16)
        font.setBold(True)
        title_label.setFont(font)
        layout.addWidget(title_label)

        button_layout = QHBoxLayout()
        self.load_online_users_btn = QPushButton('1. 自动加载在线用户')
        self.load_online_users_btn.clicked.connect(self.load_online_users)
        button_layout.addWidget(self.load_online_users_btn)

        self.manual_select_btn = QPushButton('2. 手动选择路径')
        self.manual_select_btn.setEnabled(False)
        self.manual_select_btn.setToolTip("当自动加载失败时，此按钮将被激活")
        self.manual_select_btn.clicked.connect(self.select_wechat_folder_manually)
        button_layout.addWidget(self.manual_select_btn)

        layout.addLayout(button_layout)

        user_list_label = QLabel('3. 双击选择要查看的账号:')
        layout.addWidget(user_list_label)

        self.user_list_widget = QListWidget()
        self.user_list_widget.itemDoubleClicked.connect(self.open_chat_window)
        layout.addWidget(self.user_list_widget)

        self.setLayout(layout)

        if os.name != 'nt':
            self.load_online_users()

    def load_online_users(self):
        """尝试通过读取在线微信进程来加载用户列表"""
        self.user_list_widget.clear()
        self.user_list_widget.addItem("正在加载在线用户，请稍候...")
        QApplication.processEvents()

        users = get_user_list()
        self.user_list_widget.clear()

        if isinstance(users, str):
            error_message = users
            QMessageBox.critical(self, '自动加载失败', error_message)
            self.user_list_widget.addItem("自动加载失败，请尝试手动选择路径。")
            self.manual_select_btn.setEnabled(True) # 激活手动按钮
            return

        self.load_mode = 'online'
        for user in users:
            display_text = f"在线用户: {user.get('name', '未知昵称')} ({user.get('account', '未知账号')})"
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, user)
            self.user_list_widget.addItem(item)

    def select_wechat_folder_manually(self):
        """让用户手动选择 WeChat Files 文件夹"""
        folder_path = QFileDialog.getExistingDirectory(self, "请选择 'WeChat Files' 文件夹")
        if not folder_path:
            return

        self.load_users_from_path(folder_path)

    def load_users_from_path(self, path):
        """从文件夹路径加载历史用户列表"""
        self.user_list_widget.clear()
        self.user_list_widget.addItem(f"正在从 {path} 加载...")
        QApplication.processEvents()

        users = get_users_from_path(path)
        self.user_list_widget.clear()

        if isinstance(users, str):
            QMessageBox.critical(self, '手动加载失败', users)
            return

        self.load_mode = 'manual'
        for user in users:
            display_text = f"历史用户: {user.get('wxid', '未知wxid')}"
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, user)
            self.user_list_widget.addItem(item)

    def open_chat_window(self, item):
        """双击列表项的核心处理逻辑"""
        user_data = item.data(Qt.UserRole)
        if not user_data:
            return

        if self.load_mode == 'online':
            # 在线模式，user_data 已经包含 key，直接打开
            self.start_chat_window(user_data)
        elif self.load_mode == 'manual':
            # 手动模式，user_data 只有 wxid 和 path，需要获取 key
            wxid_to_find = user_data.get('wxid')

            # 提示用户登录
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText(f"需要获取账号 {wxid_to_find} 的密钥。")
            msg_box.setInformativeText("请现在登录该微信账号，然后点击 '我已登录' 按钮继续。")
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg_box.button(QMessageBox.Ok).setText('我已登录')
            ret = msg_box.exec_()

            if ret == QMessageBox.Ok:
                # 用户确认登录后，再次尝试获取在线用户列表
                QMessageBox.information(self, "请稍候", "正在重新获取在线用户信息以匹配密钥...")
                online_users = get_user_list()
                if isinstance(online_users, str):
                    QMessageBox.critical(self, "获取密钥失败", online_users)
                    return

                found_user = None
                for u in online_users:
                    if u.get('wxid') == wxid_to_find:
                        found_user = u
                        break

                if found_user and found_user.get('key'):
                    # 找到了匹配的用户和密钥，更新user_data
                    user_data['key'] = found_user.get('key')
                    user_data['name'] = found_user.get('name')
                    self.start_chat_window(user_data)
                else:
                    QMessageBox.warning(self, "匹配失败", f"无法在当前登录的账号中找到 {wxid_to_find} 的密钥。\n请确认您登录的是正确的微信账号。")

    def start_chat_window(self, user_data):
        """创建并显示聊天窗口"""
        self.chat_win = ChatWindow(user_data)
        self.chat_win.main_window = self
        self.chat_win.show()
        self.hide()