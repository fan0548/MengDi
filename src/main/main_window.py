# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QLabel, QListWidget, QListWidgetItem, QMessageBox)
from PyQt5.QtCore import Qt
from src.main.wechat_reader import get_user_list
from src.main.chat_window import ChatWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.chat_win = None  # 用来持有聊天窗口的实例
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('微信聊天记录查看器')
        self.setGeometry(300, 300, 500, 350)

        layout = QVBoxLayout()

        # 标题
        title_label = QLabel('微信聊天记录本地查看工具')
        title_label.setAlignment(Qt.AlignCenter)
        font = title_label.font()
        font.setPointSize(16)
        font.setBold(True)
        title_label.setFont(font)
        layout.addWidget(title_label)

        # 加载用户按钮
        self.load_users_btn = QPushButton('1. 点击加载已登录的微信用户')
        self.load_users_btn.clicked.connect(self.load_users)
        layout.addWidget(self.load_users_btn)

        # 用户列表标签
        user_list_label = QLabel('2. 双击选择要查看的账号:')
        layout.addWidget(user_list_label)

        # 用户列表
        self.user_list_widget = QListWidget()
        self.user_list_widget.itemDoubleClicked.connect(self.open_chat_window)
        layout.addWidget(self.user_list_widget)

        self.setLayout(layout)

        # 在非Windows环境下，为了方便演示，自动加载模拟用户数据
        if os.name != 'nt':
            self.load_users()

    def load_users(self):
        """
        加载用户列表到UI
        """
        self.user_list_widget.clear()
        self.user_list_widget.addItem("正在加载，请稍候...")
        QApplication.processEvents()  # 强制UI更新

        users = get_user_list()
        self.user_list_widget.clear()

        # 检查返回结果是否为错误字符串
        if isinstance(users, str):
            error_message = users
            QMessageBox.critical(self, '加载错误', error_message)
            # 在列表中也显示错误的第一行，以供参考
            self.user_list_widget.addItem(error_message.split('\n')[0])
            return

        if not users:
            QMessageBox.information(self, '提示', '未找到任何登录的微信用户。')
            self.user_list_widget.addItem('未找到用户，请确认微信是否已登录。')
            return

        for user in users:
            # 显示更详细的用户信息以便区分
            display_text = f"{user.get('name', '未知昵称')} ({user.get('account', '未知账号')}) - {user.get('mobile', '未知手机')}"
            item = QListWidgetItem(display_text)
            # 将完整的用户信息字典存储在item中
            item.setData(Qt.UserRole, user)
            self.user_list_widget.addItem(item)

    def open_chat_window(self, item):
        """
        双击用户项时，打开聊天窗口
        """
        user_data = item.data(Qt.UserRole)
        if not user_data:
            return

        # ChatWindow将负责获取自己的数据并处理其中的错误
        self.chat_win = ChatWindow(user_data)
        # 将主窗口的引用传递给聊天窗口，以便在关闭时重新显示主窗口
        self.chat_win.main_window = self
        self.chat_win.show()
        self.hide()