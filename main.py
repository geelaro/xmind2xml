#!/usr/bin/env python
# coding:utf-8

"""
转换程序
"""

from xmind_parser import xmind_to_suit
from testlink_parse import to_testlink_xml_file


def xmind_to_testlink_xml(xmind):
    """ """
    xml_out = xmind[:-5]+'xml'
    suite = xmind_to_suit(xmind)
    to_testlink_xml_file(suite, xml_out)
    return xml_out


if __name__ == "__main__":
    xmind_file = 'doc/v1.1学员池.xmind'

    xmind_to_testlink_xml(xmind_file)
