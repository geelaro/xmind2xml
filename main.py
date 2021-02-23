#!/usr/bin/env python
# coding:utf-8

"""
转换程序
"""

from xmind_parser import xmind_to_suit
from testlink_parse import to_testlink_xml_file
import os


def xmind_to_testlink_xml(xmind):
    """转换xmind为testlink-xml格式"""
    xml_out = xmind[:-5]+'xml'
    suite = xmind_to_suit(xmind)
    to_testlink_xml_file(suite, xml_out)
    return xml_out


if __name__ == "__main__":
    # xmind文件目录
    xmind_dir = 'doc/'
    file_list = os.listdir(xmind_dir)

    # 把目录下所有xmind文件转为testlink格式的xml
    for f in file_list:
        if f.endswith('.xmind'):
            xmind_to_testlink_xml(xmind_dir+f)
