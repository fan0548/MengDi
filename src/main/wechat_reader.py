# -*- coding: utf-8 -*-

"""
微信数据读取模块
负责调用 pywxdump 并返回处理后的数据
"""

import os
import time
from collections import defaultdict

# --- 模拟数据 (保留以便在非Windows环境下进行UI开发和测试) ---
def get_mock_user_list():
    """返回模拟的用户列表"""
    return [
        {'name': '用户A (模拟)', 'wxid': 'wxid_aaaaaaaa', 'mobile': '13800138000', 'account': 'mock_a', 'key': 'mock_key_a', 'path': '/mock/path/WeChat Files'},
        {'name': '用户B (模拟)', 'wxid': 'wxid_bbbbbbbb', 'mobile': '13900139000', 'account': 'mock_b', 'key': 'mock_key_b', 'path': '/mock/path/WeChat Files'},
    ]

def get_mock_data(wxid):
    """返回指定wxid的模拟联系人和聊天记录"""
    contacts = {
        'filehelper': {'wxid': 'filehelper', 'nickname': '文件传输助手', 'remark': ''},
        'zhangsan_wxid': {'wxid': 'zhangsan_wxid', 'nickname': '张三', 'remark': '三儿'},
        '123456789@chatroom': {'wxid': '123456789@chatroom', 'nickname': '家庭群', 'remark': '家庭群'},
    }

    chat_history = defaultdict(list)
    # type: 1 for text, 3 for image. is_sender: 1 for self, 0 for others.
    chat_history['filehelper'] = [
        {'is_sender': 1, 'type': 1, 'content': '这是一条我发送的测试消息', 'create_time': int(time.time()) - 3600},
        {'is_sender': 0, 'type': 1, 'content': '收到，这是一条来自文件助手的回复。', 'create_time': int(time.time()) - 3500},
        {'is_sender': 1, 'type': 3, 'content': 'https://via.placeholder.com/150', 'create_time': int(time.time()) - 3000},
    ]
    chat_history['zhangsan_wxid'] = [
        {'is_sender': 0, 'type': 1, 'content': '你好啊！', 'create_time': int(time.time()) - 86400},
        {'is_sender': 1, 'type': 1, 'content': f'你好，我是{wxid}', 'create_time': int(time.time()) - 86300},
    ]
    chat_history['123456789@chatroom'] = [
        {'is_sender': 0, 'type': 1, 'content': '大家好，我是李四', 'create_time': int(time.time()) - 7200, 'sender_name': '李四'},
        {'is_sender': 1, 'type': 1, 'content': '大家好！', 'create_time': int(time.time()) - 7000, 'sender_name': '用户A (模拟)'},
    ]
    return contacts, chat_history

# --- 真实数据读取 ---

def get_user_list():
    """
    获取所有已登录的用户信息。
    :return: 成功时返回用户列表(list of dicts)，失败时返回错误信息(str)。
    """
    if os.name != 'nt':
        print("警告：当前非 Windows 环境，返回模拟用户数据。")
        return get_mock_user_list()

    try:
        from pywxdump import read_info
        users = read_info()
        if not users:
            return "错误：未找到任何登录的微信用户。请确保微信PC版已经运行并登录。"
        return list(users) # read_info返回的是元组，转换为列表
    except ImportError:
        return "错误：核心库 'pywxdump' 未安装或安装不正确。\n请在命令行运行 'pip install -r requirements.txt' 进行安装。"
    except Exception as e:
        error_msg = f"获取用户信息时发生未知错误：{e}\n\n"
        error_msg += "请检查以下几点：\n"
        error_msg += "1. 微信是否已经登录？\n"
        error_msg += "2. 是否以管理员权限运行本程序？\n"
        error_msg += "3. 当前 pywxdump 版本是否支持您的微信版本？"
        return error_msg

def get_all_data(user_info):
    """
    获取一个用户的所有数据，包括联系人、群聊和所有聊天记录。
    :param user_info: 单个用户的信息字典，来自 get_user_list 的返回结果。
    :return: (contacts, chat_history) 元组。出错时，某一项或两项可能为错误字符串。
    """
    wxid = user_info.get('wxid')
    if os.name != 'nt':
        print(f"警告：当前非 Windows 环境，为 wxid='{wxid}' 返回模拟数据。")
        return get_mock_data(wxid)

    key = user_info.get('key')
    wx_files_path = user_info.get('path')

    if not all([wxid, key, wx_files_path]):
        err_msg = "错误：获取到的用户信息不完整，缺少 wxid, key, 或 path。"
        return err_msg, err_msg

    # 构造各种数据库的路径
    # 注意: pywxdump的函数可能需要非常具体的路径
    msg_path = os.path.join(wx_files_path, wxid, 'Msg')
    micro_path = os.path.join(msg_path, 'MicroMsg.db')
    media_path = os.path.join(wx_files_path, wxid, 'FileStorage', 'MsgAttach')

    contacts_result = {}
    chathistory_result = {}

    # 读取联系人
    try:
        from pywxdump import get_contact
        contacts_result = get_contact(key, micro_path)
    except Exception as e:
        contacts_result = f"读取联系人列表时出错：{e}"

    # 读取聊天记录
    try:
        from pywxdump import read_chat_history
        # read_chat_history 需要 wxid, key 和包含所有MSG.db的文件夹路径
        chathistory_result = read_chat_history(wxid, key, msg_path)
    except Exception as e:
        chathistory_result = f"读取聊天记录时出错：{e}"

    return contacts_result, chathistory_result