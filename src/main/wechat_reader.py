# -*- coding: utf-8 -*-

"""
微信数据读取模块
负责调用 pywxdump 并返回处理后的数据
在非 Windows 环境下，此模块返回模拟数据用于UI开发
"""

import os
import time
from collections import defaultdict


def get_user_list(wechat_path: str):
    """
    根据微信路径获取所有登录过的用户列表
    :param wechat_path: 微信安装路径下的 "WeChat Files" 文件夹路径
    :return: 用户列表，每个用户是一个包含'name', 'wxid', 'path'的字典
    """
    # 在非 Windows 环境下返回模拟数据
    if os.name != 'nt':
        print("警告：当前非 Windows 环境，返回模拟用户数据。")
        return [
            {'name': '用户A (模拟)', 'wxid': 'wxid_aaaaaaaa', 'path': '/mock/path/wxid_aaaaaaaa'},
            {'name': '用户B (模拟)', 'wxid': 'wxid_bbbbbbbb', 'path': '/mock/path/wxid_bbbbbbbb'},
            {'name': '用户C (模拟)', 'wxid': 'wxid_cccccccc', 'path': '/mock/path/wxid_cccccccc'},
        ]

    # TODO: 在 Windows 环境下，将在这里调用 pywxdump 的真实代码
    # from pywxdump import read_info
    # user_list = read_info()
    # return user_list
    return []


def get_chat_history(wxid: str):
    """
    根据用户的 wxid 获取其所有聊天记录
    :param wxid: 用户的 wxid
    :return: 一个字典，key是聊天对象（朋友或群），value是消息列表
    """

    # 在非 Windows 环境下返回模拟数据
    if os.name != 'nt':
        print(f"警告：当前非 Windows 环境，为 wxid='{wxid}' 返回模拟聊天数据。")
        mock_data = defaultdict(list)

        # 模拟与“文件传输助手”的聊天
        mock_data['filehelper'] = [
            {'type': 'text', 'sender': wxid, 'content': '这是一条我发送的测试消息', 'timestamp': int(time.time()) - 3600},
            {'type': 'text', 'sender': 'filehelper', 'content': '收到，这是一条来自文件助手的回复。', 'timestamp': int(time.time()) - 3500},
            {'type': 'image', 'sender': wxid, 'content': 'https://via.placeholder.com/150', 'timestamp': int(time.time()) - 3000},
        ]

        # 模拟与“张三”的聊天
        mock_data['zhangsan_wxid'] = [
            {'type': 'text', 'sender': 'zhangsan_wxid', 'content': '你好啊！', 'timestamp': int(time.time()) - 86400},
            {'type': 'text', 'sender': wxid, 'content': '你好，我是' + wxid, 'timestamp': int(time.time()) - 86300},
            {'type': 'text', 'sender': 'zhangsan_wxid', 'content': '这是一个长消息，用来测试气泡的换行效果。这是一个长消息，用来测试气泡的换行效果。这是一个长消息，用来测试气泡的换行效果。', 'timestamp': int(time.time()) - 86200},
        ]

        # 模拟一个群聊
        mock_data['123456789@chatroom'] = [
            {'type': 'text', 'sender': 'lisi_wxid', 'content': '大家好，我是李四', 'timestamp': int(time.time()) - 7200},
            {'type': 'text', 'sender': 'wangwu_wxid', 'content': '欢迎欢迎！', 'timestamp': int(time.time()) - 7100},
            {'type': 'text', 'sender': wxid, 'content': '大家好！', 'timestamp': int(time.time()) - 7000},
            {'type': 'image', 'sender': 'lisi_wxid', 'content': 'https://via.placeholder.com/200', 'timestamp': int(time.time()) - 6500},
        ]

        return mock_data

    # TODO: 在 Windows 环境下，将在这里调用 pywxdump 的真实代码来读取和解密数据库
    # from pywxdump import read_chat_history
    # chat_history = read_chat_history(wxid)
    # return chat_history
    return {}

def get_contact_list(wxid: str):
    """
    根据用户的 wxid 获取其联系人列表
    :param wxid: 用户的 wxid
    :return: 一个字典，key是联系人wxid，value是联系人信息（如昵称）
    """
    if os.name != 'nt':
        print(f"警告：当前非 Windows 环境，为 wxid='{wxid}' 返回模拟联系人列表。")
        return {
            'filehelper': {'name': '文件传输助手', 'remark': ''},
            'zhangsan_wxid': {'name': '张三', 'remark': '三儿'},
            'lisi_wxid': {'name': '李四', 'remark': ''},
            'wangwu_wxid': {'name': '王五', 'remark': ''},
            '123456789@chatroom': {'name': '家庭群', 'remark': '家庭群'},
        }

    # TODO: 在 Windows 环境下，将在这里调用 pywxdump 的真实代码来读取联系人数据库
    return {}