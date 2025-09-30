# -*- coding: utf-8 -*-

import sys
import requests
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QListWidget,
                             QLabel, QListWidgetItem, QSplitter, QLineEdit)
from PyQt5.QtGui import QFont, QPixmap, QColor, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QRectF
from src.main.wechat_reader import get_chat_history, get_contact_list

# --- 自定义文本聊天气泡 ---
class TextBubble(QWidget):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.padding = 10
        self.radius = 15

        self.font = QFont("Microsoft YaHei", 12)

        # 使用QLabel来显示文本
        self.label = QLabel(text)
        self.label.setFont(self.font)
        self.label.setWordWrap(True)  # 自动换行
        self.label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        # 设置一个最大宽度，让文本可以换行
        self.label.setMaximumWidth(400)

        # 创建一个布局来管理label
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.setContentsMargins(self.padding, self.padding, self.padding, self.padding)
        self.setLayout(layout)

    def paintEvent(self, event):
        # 这个函数负责绘制气泡背景
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 根据父控件（is_sender）的属性来决定颜色
        is_sender = getattr(self.parent(), 'is_sender', False)
        bubble_color = QColor("#95EC69") if is_sender else QColor("#FFFFFF")

        painter.setBrush(QBrush(bubble_color))
        painter.setPen(QPen(Qt.NoPen))
        painter.drawRoundedRect(self.rect(), self.radius, self.radius)


# --- 自定义图片聊天气泡 ---
class ImageBubble(QWidget):
    def __init__(self, url):
        super().__init__()
        self.padding = 5
        self.radius = 15

        self.image_label = QLabel("图片加载中...")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(150, 150) # 初始大小
        self.image_label.setStyleSheet("background-color: #E0E0E0;")

        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)
        layout.setContentsMargins(self.padding, self.padding, self.padding, self.padding)
        self.setLayout(layout)

        self.load_image(url)

    def load_image(self, url):
        # 在一个新线程中加载图片以避免UI阻塞（简化版，实际项目推荐用QThread）
        try:
            response = requests.get(url, stream=True, timeout=5)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                # 缩放图片
                self.image_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.image_label.setText("图片加载失败")
        except Exception as e:
            print(f"Error loading image: {e}")
            self.image_label.setText("图片加载出错")

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
        self.chat_history = get_chat_history(self.wxid)
        self.contact_list = get_contact_list(self.wxid)
        self.init_ui()
        self.load_contacts()

    def init_ui(self):
        self.setWindowTitle(f"聊天记录 - {self.user_data['name']}")
        self.setGeometry(100, 100, 800, 600)

        # 主布局
        main_layout = QHBoxLayout(self)

        # 创建一个可分割的窗口
        splitter = QSplitter(Qt.Horizontal)

        # --- 左侧联系人列表 ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0,0,0,0)

        contact_label = QLabel("联系人")
        contact_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        left_layout.addWidget(contact_label)

        # 添加搜索框
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("搜索联系人...")
        self.search_box.textChanged.connect(self.filter_contacts)
        left_layout.addWidget(self.search_box)

        self.contact_list_widget = QListWidget()
        self.contact_list_widget.setStyleSheet("QListWidget { font-size: 14px; }")
        self.contact_list_widget.itemClicked.connect(self.on_contact_selected)
        left_layout.addWidget(self.contact_list_widget)

        # --- 右侧聊天记录 ---
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(5,0,5,0)

        self.chat_target_label = QLabel("选择一个联系人开始查看")
        self.chat_target_label.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        right_layout.addWidget(self.chat_target_label)

        self.chat_history_widget = QListWidget()
        self.chat_history_widget.setSpacing(10) # 消息间的间距
        self.chat_history_widget.setStyleSheet("QListWidget { background-color: #F5F5F5; border: none; }")
        self.chat_history_widget.setWordWrap(True)
        right_layout.addWidget(self.chat_history_widget)

        # 将左右面板添加到分割器
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([200, 600]) # 初始大小

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def filter_contacts(self):
        """根据搜索框内容过滤联系人列表"""
        search_text = self.search_box.text().lower()
        for i in range(self.contact_list_widget.count()):
            item = self.contact_list_widget.item(i)
            item_text = item.text().lower()
            # 隐藏不匹配的项
            item.setHidden(search_text not in item_text)

    def load_contacts(self):
        """加载联系人列表"""
        self.contact_list_widget.clear()
        for cid, cinfo in self.contact_list.items():
            # 优先显示备注名，如果没有则显示昵称
            name = cinfo.get('remark') or cinfo.get('name', cid)
            if not name: continue # 跳过没有名字的联系人
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, cid) # 存储wxid
            self.contact_list_widget.addItem(item)

    def on_contact_selected(self, item):
        """当用户选择一个联系人时"""
        cid = item.data(Qt.UserRole)
        name = item.text()
        self.chat_target_label.setText(name)
        self.load_chat_history(cid)

    def load_chat_history(self, cid):
        """加载与特定联系人的聊天记录"""
        self.chat_history_widget.clear()
        messages = self.chat_history.get(cid, [])

        if not messages:
            self.add_system_message("没有找到聊天记录")
            return

        for msg in messages:
            is_sender = (msg['sender'] == self.wxid)

            if msg['type'] == 'text':
                bubble = TextBubble(msg['content'])
            elif msg['type'] == 'image':
                bubble = ImageBubble(msg['content'])
            else:
                # 对于不支持的消息类型，显示一个占位符
                bubble = TextBubble(f"[不支持的消息类型: {msg['type']}]")

            self.add_message_widget(bubble, is_sender)

    def add_message_widget(self, widget, is_sender):
        """将消息控件（气泡）添加到聊天记录中，并处理对齐"""
        # 创建一个容器widget，并为其设置一个布局
        container = QWidget()
        container.is_sender = is_sender # 附加一个属性，供paintEvent使用
        layout = QHBoxLayout(container)
        layout.setContentsMargins(5,0,5,0)

        # 根据发送者添加弹簧和控件，实现左右对齐
        if is_sender:
            layout.addStretch() # 左侧弹簧
            layout.addWidget(widget)
        else:
            layout.addWidget(widget)
            layout.addStretch() # 右侧弹簧

        container.setLayout(layout)

        # 创建一个QListWidgetItem，并将容器设置为其widget
        item = QListWidgetItem(self.chat_history_widget)
        item.setSizeHint(container.sizeHint())
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        self.chat_history_widget.addItem(item)
        self.chat_history_widget.setItemWidget(item, container)
        self.chat_history_widget.scrollToBottom()


    def add_system_message(self, text):
        item = QListWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(QColor("#DADADA"))
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        self.chat_history_widget.addItem(item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 模拟用户数据
    mock_user = {'name': '模拟用户', 'wxid': 'wxid_mockuser'}
    chat_win = ChatWindow(mock_user)
    chat_win.show()
    sys.exit(app.exec_())