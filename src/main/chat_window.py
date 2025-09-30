# -*- coding: utf-8 -*-

import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QListWidget,
                             QLabel, QListWidgetItem, QSplitter, QLineEdit, QMessageBox)
from PyQt5.QtGui import QFont, QPixmap, QColor, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
from src.main.wechat_reader import get_all_data

# --- 自定义文本聊天气泡 ---
class TextBubble(QWidget):
    def __init__(self, text, sender_name=None):
        super().__init__()
        self.padding = 10
        self.radius = 15
        self.font = QFont("Microsoft YaHei", 12)

        # 如果是群聊，显示发送者名字
        full_text = text
        if sender_name:
            sender_label = QLabel(sender_name)
            sender_label.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
            sender_label.setStyleSheet("color: #888;")

        self.label = QLabel(full_text)
        self.label.setFont(self.font)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.label.setMaximumWidth(450)

        layout = QVBoxLayout(self)
        layout.setSpacing(2)
        if sender_name:
            layout.addWidget(sender_label)
        layout.addWidget(self.label)
        layout.setContentsMargins(self.padding, self.padding, self.padding, self.padding)
        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        is_sender = getattr(self.parent(), 'is_sender', False)
        bubble_color = QColor("#95EC69") if is_sender else QColor("#FFFFFF")
        painter.setBrush(QBrush(bubble_color))
        painter.setPen(QPen(Qt.NoPen))
        painter.drawRoundedRect(self.rect(), self.radius, self.radius)

# --- 自定义图片聊天气泡 ---
class ImageBubble(QWidget):
    # (代码与之前版本相同，为了完整性而保留)
    def __init__(self, url):
        super().__init__()
        self.padding = 5
        self.radius = 15
        self.image_label = QLabel("图片加载中...")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(150, 150)
        self.image_label.setStyleSheet("background-color: #E0E0E0;")
        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)
        layout.setContentsMargins(self.padding, self.padding, self.padding, self.padding)
        self.setLayout(layout)
        self.load_image(url)

    def load_image(self, url):
        try:
            # 增加User-Agent以模拟浏览器，避免一些网站的403 Forbidden错误
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, stream=True, timeout=10, headers=headers)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                self.image_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.image_label.setText(f"加载失败({response.status_code})")
        except Exception as e:
            self.image_label.setText("加载出错")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        is_sender = getattr(self.parent(), 'is_sender', False)
        bubble_color = QColor("#95EC69") if is_sender else QColor("#FFFFFF")
        painter.setBrush(QBrush(bubble_color))
        painter.setPen(QPen(Qt.NoPen))
        painter.drawRoundedRect(self.rect(), self.radius, self.radius)

# --- 聊天窗口主类 ---
class ChatWindow(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.wxid = user_data['wxid']
        self.main_window = None  # 用于持有主窗口的引用

        self.init_ui()
        self.load_all_data()

    def init_ui(self):
        # (UI初始化代码与之前版本基本相同)
        self.setWindowTitle(f"聊天记录 - {self.user_data.get('name', '未知用户')}")
        self.setGeometry(100, 100, 800, 600)
        main_layout = QHBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0,0,0,0)
        contact_label = QLabel("联系人")
        contact_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        left_layout.addWidget(contact_label)
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("搜索联系人...")
        self.search_box.textChanged.connect(self.filter_contacts)
        left_layout.addWidget(self.search_box)
        self.contact_list_widget = QListWidget()
        self.contact_list_widget.setStyleSheet("QListWidget { font-size: 14px; }")
        self.contact_list_widget.itemClicked.connect(self.on_contact_selected)
        left_layout.addWidget(self.contact_list_widget)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(5,0,5,0)
        self.chat_target_label = QLabel("选择一个联系人开始查看")
        self.chat_target_label.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        right_layout.addWidget(self.chat_target_label)
        self.chat_history_widget = QListWidget()
        self.chat_history_widget.setSpacing(10)
        self.chat_history_widget.setStyleSheet("QListWidget { background-color: #F5F5F5; border: none; }")
        self.chat_history_widget.setWordWrap(True)
        right_layout.addWidget(self.chat_history_widget)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([250, 550])
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def load_all_data(self):
        """加载所有数据并处理错误"""
        self.contacts, self.chat_history = get_all_data(self.user_data)

        error_occured = False
        if isinstance(self.contacts, str):
            QMessageBox.critical(self, "联系人加载失败", self.contacts)
            error_occured = True

        if isinstance(self.chat_history, str):
            QMessageBox.critical(self, "聊天记录加载失败", self.chat_history)
            error_occured = True

        if error_occured:
            self.close() # 如果有任何错误，直接关闭此窗口
            return

        self.load_contacts()

    def filter_contacts(self):
        search_text = self.search_box.text().lower()
        for i in range(self.contact_list_widget.count()):
            item = self.contact_list_widget.item(i)
            item_text = item.text().lower()
            item.setHidden(search_text not in item_text)

    def load_contacts(self):
        self.contact_list_widget.clear()
        # 将联系人按备注或昵称排序
        sorted_contacts = sorted(self.contacts.values(), key=lambda c: c.get('remark', '') or c.get('nickname', ''))
        for cinfo in sorted_contacts:
            name = cinfo.get('remark') or cinfo.get('nickname')
            cid = cinfo.get('wxid')
            if not name or not cid: continue
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, cid)
            self.contact_list_widget.addItem(item)

    def on_contact_selected(self, item):
        cid = item.data(Qt.UserRole)
        name = item.text()
        self.chat_target_label.setText(name)
        self.load_chat_history(cid)

    def load_chat_history(self, cid):
        self.chat_history_widget.clear()
        messages = self.chat_history.get(cid, [])
        if not messages:
            self.add_system_message("没有找到聊天记录")
            return

        for msg in messages:
            is_sender = msg.get('is_sender') == 1
            msg_type = msg.get('type')
            content = msg.get('content', '')

            # 在群聊中，获取发言人的名字
            sender_name = None
            if '@chatroom' in cid and not is_sender:
                sender_wxid = msg.get('sender_name') # pywxdump中，群聊的发言人wxid在sender_name字段
                contact_info = self.contacts.get(sender_wxid, {})
                sender_name = contact_info.get('remark') or contact_info.get('nickname', sender_wxid)

            if msg_type == 1: # 文本消息
                bubble = TextBubble(content, sender_name)
            elif msg_type == 3: # 图片消息
                # 图片路径可能是本地的，也可能是URL。这里简化处理，假设为URL
                bubble = ImageBubble(content)
            else:
                bubble = TextBubble(f"[不支持的消息类型: {msg_type}]")

            self.add_message_widget(bubble, is_sender)
        self.chat_history_widget.scrollToBottom()

    def add_message_widget(self, widget, is_sender):
        container = QWidget()
        container.is_sender = is_sender
        layout = QHBoxLayout(container)
        layout.setContentsMargins(5,0,5,0)
        if is_sender:
            layout.addStretch()
            layout.addWidget(widget)
        else:
            layout.addWidget(widget)
            layout.addStretch()
        container.setLayout(layout)
        item = QListWidgetItem(self.chat_history_widget)
        item.setSizeHint(container.sizeHint())
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        self.chat_history_widget.addItem(item)
        self.chat_history_widget.setItemWidget(item, container)

    def add_system_message(self, text):
        item = QListWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(QColor("#DADADA"))
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        self.chat_history_widget.addItem(item)

    def closeEvent(self, event):
        """当窗口关闭时，重新显示主窗口"""
        if self.main_window:
            self.main_window.show()
        event.accept()