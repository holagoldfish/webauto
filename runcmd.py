# coding=utf-8
__author__ = 'Administrator'
import os

def execute():
    # 跳转到要执行cmd命令的路径
    os.chdir(r"D:\Project\Keyword\data")
    # cmd命令

    comment = 'python all_test.py'
    # 执行命令
    os.system(comment)