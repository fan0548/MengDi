# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QApplication
from src.main.main_window import MainWindow

def main():
    """
    应用程序主入口
    """
    app = QApplication(sys.argv)

    main_win = MainWindow()
    main_win.show()

    # 在非Windows环境下，为了方便演示，自动加载模拟用户数据
    # 在真实的Windows环境中，用户需要手动点击按钮选择文件夹
    if os.name != 'nt':
        print("开发模式：自动加载模拟用户数据。")
        main_win.load_users("/mock/path/to/wechat/files")

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()