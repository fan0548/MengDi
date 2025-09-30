# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QLabel, QListWidget, QListWidgetItem, QFileDialog)
from PyQt5.QtCore import Qt
from src.main.wechat_reader import get_user_list


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('微信聊天记录查看器')
        self.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()

        # 标题
        title_label = QLabel('微信聊天记录本地查看工具')
        title_label.setAlignment(Qt.AlignCenter)
        font = title_label.font()
        font.setPointSize(16)
        font.setBold(True)
        title_label.setFont(font)
        layout.addWidget(title_label)

        # 选择文件夹按钮
        self.select_folder_btn = QPushButton('1. 点击选择微信文件夹')
        self.select_folder_btn.clicked.connect(self.select_wechat_folder)
        layout.addWidget(self.select_folder_btn)

        # 用户列表标签
        user_list_label = QLabel('2. 选择要查看的账号:')
        layout.addWidget(user_list_label)

        # 用户列表
        self.user_list_widget = QListWidget()
        self.user_list_widget.itemDoubleClicked.connect(self.open_chat_window)
        layout.addWidget(self.user_list_widget)

        self.setLayout(layout)

    def select_wechat_folder(self):
        """
        打开文件夹选择对话框
        """
        # 在非Windows环境下，我们无法真正地选择文件夹，所以直接使用模拟数据
        # 在真实的Windows应用中，QFileDialog可以正常工作
        folder_path = QFileDialog.getExistingDirectory(self, "选择微信文件(WeChat Files)所在的文件夹")

        # 如果用户取消了选择，则不执行任何操作
        if not folder_path and os.name == 'nt':
            return

        print(f"选择的文件夹路径: {folder_path}")
        self.load_users(folder_path)

    def load_users(self, path):
        """
        加载用户列表到UI
        """
        self.user_list_widget.clear()
        try:
            users = get_user_list(path)
            if not users:
                self.user_list_widget.addItem('未找到用户，请确认文件夹路径是否正确。')
                return

            for user in users:
                # QListWidgetItem用于在列表中显示每个用户
                item = QListWidgetItem(user['name'])
                # 将用户的完整信息（包括wxid）存储在item中，方便后续使用
                item.setData(Qt.UserRole, user)
                self.user_list_widget.addItem(item)
        except Exception as e:
            self.user_list_widget.addItem(f'加载出错: {e}')

    def open_chat_window(self, item):
        """
        双击用户项时，打开聊天窗口（将在后续步骤中实现）
        """
        user_data = item.data(Qt.UserRole)
        wxid = user_data['wxid']
        name = user_data['name']
        print(f"准备为用户 {name} ({wxid}) 打开聊天窗口...")
        # 在这里，我们将创建并显示聊天窗口
        from src.main.chat_window import ChatWindow
        self.chat_win = ChatWindow(user_data)
        self.chat_win.show()
        self.hide() # 隐藏主窗口
