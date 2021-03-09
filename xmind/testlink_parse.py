#!/usr/bin/env python
# coding:utf-8

"""
Desc: 解析xmind dict数据为testlink所需的xml
Date: 2021-1-20
"""

import os
from io import BytesIO
from os.path import exists
from xmind.datatype import TestCase, TestStep, TestSuit, cache
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.sax.saxutils import escape
import json


class Tags():
    xml = 'xml'
    testsuit = 'testsuite'
    details = 'details'
    testcase = 'testcase'
    summary = 'summary'
    preconditions = 'preconditions'
    steps = 'steps'
    step = 'step'
    step_number = 'step_number'
    actions = 'actions'
    expectedresults = 'expectedresults'
    execution_type = 'execution_type'
    importance = 'importance'


class Attributes():
    name = 'name'


def to_testlink_xml_file(testsuite, path_to_xml):
    """保存testsuit为xml文件"""
    content = to_testlink_xml_content(testsuite)
    # print(content)
    if exists(path_to_xml):
        os.remove(path_to_xml)

    with open(path_to_xml, 'w', encoding='utf-8') as f:
        f.write(prettify_xml(content))


def to_testlink_xml_content(testsuite):
    """ 转testlink suit为xml字符串 """
    assert isinstance(testsuite, TestSuit)
    root_suite = Element(Tags.testsuit)
    root_suite.set(Attributes.name, testsuite.name)

    cache['testcase_count'] = 0

    for suite in testsuite.sub_suits:
        assert isinstance(suite, TestSuit)

        if should_skip(suite.name):
            continue

        suite_element = SubElement(root_suite, Tags.testsuit)
        suite_element.set(Attributes.name, suite.name)
        build_text_field(suite_element, Tags.details, suite.details)
        build_testcase_xml(suite, suite_element)

    tree = ElementTree.ElementTree(root_suite)
    f = BytesIO()
    tree.write(f, encoding='utf-8', xml_declaration=True)
    return f.getvalue().decode('utf-8')


def build_text_field(element, tag, value):
    if should_parse(value):
        e = SubElement(element, tag)
        set_text(e, value)


def build_testcase_xml(suite, suite_element):
    """ 转换用例dict为xml格式 """
    for testcase in suite.testcase_list:
        assert isinstance(testcase, TestCase)

        if should_skip(testcase.name):
            continue

        cache['testcase_count'] += 1

        testcase_element = SubElement(suite_element, Tags.testcase)
        testcase_element.set(Attributes.name, testcase.name)

        build_text_field(testcase_element, Tags.summary, testcase.summary)
        build_text_field(testcase_element, Tags.preconditions,
                         testcase.preconditions)
        build_text_field(testcase_element, Tags.execution_type,
                         testcase.execution_type)

        # build_text_field(testcase_element, Tags.importance,
        #                  _convert_importance(testcase.importance))
        e = SubElement(testcase_element, Tags.importance)
        e.text = _convert_importance(testcase.importance)

        build_step_xml(testcase, testcase_element)


def build_step_xml(testcase, testcase_element):
    """ 转换用例步骤dict为xml """
    if testcase.steps:
        setps_element = SubElement(testcase_element, Tags.steps)

        for step in testcase.steps:
            assert isinstance(step, TestStep)

            if should_skip(step.action):
                continue
            else:
                step_element = SubElement(setps_element, Tags.step)

            build_text_field(step_element, Tags.actions, step.action)
            build_text_field(step_element, Tags.expectedresults,
                             step.expectedresults)
            build_text_field(
                setps_element, Tags.execution_type, step.execution_type)

            # build_text_field(step_element, Tags.step_number, str(step.number))
            e = SubElement(step_element, Tags.step_number)
            e.text = str(step.number)


def set_text(element, value):
    if isinstance(value, int):
        element.text = str(value)
    elif value:
        value = escape(value, entities={'\r\n': '<br />'})
        value = value.replace('\n', '<br />')
        value = value.replace('<br />', '<br />\n')

        # ![CDATA[]]
        element.append(
            Comment('--><![CDATA['+value.replace(']]>', ']]]]><![CDATA[>')+']]><!--'))


def should_skip(item):
    """ 判断是否跳过此部分 """
    return item is None or not isinstance(item, str) or item.strip() == "" or item.startswith('!')


def should_parse(item):
    """
    判断是否需要解析：不以！开头的字符串或数字
    """
    return (isinstance(item, str) and not item.startswith('!') or isinstance(item, int))


def _convert_importance(value):
    mapping = {1: '3', 2: '2', 3: '1'}

    if value in mapping.keys():
        return mapping[value]
    else:
        return '2'


def prettify_xml(xml_string):
    """ pretty xml """
    # 去掉comment
    xml_string = xml_string.replace('<!---->', '')
    parsed = minidom.parseString(xml_string)
    return parsed.toprettyxml(indent='\t', encoding='utf-8').decode('utf-8')
