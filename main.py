#!/usr/bin/env python
# coding:utf-8

"""
转换程序
"""

from xmind.xmind_parser import xmind_to_suit
from xmind.testlink_parse import to_testlink_xml_file
import os


def xmind_to_testlink_xml(xmind):
    """转换xmind为testlink-xml格式"""
    xml_out = xmind[:-5]+'xml'
    suite = xmind_to_suit(xmind)
    to_testlink_xml_file(suite, xml_out)
    return xml_out


def excel_to_testlink_xml(excel): a 
    """ Excel格式的用例转为testlink-xml格式 """
    pass


if __name__ == "__main__":
    # xmind文件目录
    case_path = 'doc/'
    file_list = os.listdir(case_path)

    # 把目录下所有xmind或Excel文件转为testlink格式的xml
    for f in file_list:
        if f.endswith('.xmind'):
            xmind_to_testlink_xml(case_path + f)
        if f.endswith('.xlsx') or f.endswith('.xls'):
            excel_to_testlink_xml(case_path + f)
