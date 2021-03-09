#!/usr/bin/env python
# coding:utf-8

"""
Desc: 解析xmind文件
"""

from xmindparser import xmind_to_dict, config
from xmind.datatype import cache, TestCase, TestStep, TestSuit
import json
from config.logger_handler import logger


config['hideEmptyValue'] = False
_config = {
    'sep': ' ',
    'valid_sep': '/>-+',
    'precondition_sep': '\n----\n',
    'summary_sep': '\n----\n'
}


def ignore_filter(topics):
    """
    过滤掉"!"标识的用例
    """
    result = [t for t in topics if t['title']
              and not t['title'].startswith('!')]

    for topic in result:
        more_topic = topic.get('topics', [])
        topic['topics'] = ignore_filter(more_topic)

    return result


def open_and_cache_xmind(xmind_file):
    if not cache:
        cache['sheet'] = xmind_to_dict(xmind_file)
        cache['root'] = get_default_sheet(cache['sheet'])['topic']
        root_topics = cache['root'].get('topics', [])

        assert len(root_topics) > 0, '非法xmind文件，最少有一个主题节点'
        cache['root']['topics'] = ignore_filter(root_topics)
        cache['name'] = xmind_file
    logger.debug('cached xmind:{}'.format(xmind_file))


def get_default_sheet(sheets):
    """xmind文件第一个sheet就是默认的"""
    assert len(sheets) >= 0, '非法xmind文件，最少有一个画布'
    return sheets[0]


def xmind_to_suit(xmind_file):

    # First, clear数据
    cache.clear()
    open_and_cache_xmind(xmind_file)
    # print(json.dumps(cache))
    #
    root = cache['root']

    suite = TestSuit()
    suite.name = xmind_file[:-6]
    suite.sub_suits = []

    for _ in root['topics']:
        suite.sub_suits.append(parse_suit(_))

    return suite


def parse_suit(suite_dict):
    """解析用例模块"""
    suite = TestSuit()
    suite.name = suite_dict['title']
    suite.details = suite_dict['note'] if 'note' in suite_dict else None
    suite.testcase_list = []
    testcase_topics = suite_dict.get('topics', [])

    for _ in testcase_topics:
        t = parse_testcase(_)
        suite.testcase_list.append(t)

    return suite


def parse_testcase(testcase_dict, parent=None):
    """解析用例"""
    testcase = TestCase()
    nodes = parent+[testcase_dict] if parent else [testcase_dict]

    testcase.name = build_testcase_title(nodes)
    testcase.summary = build_testcase_summary(nodes)
    testcase.importance = get_priority(testcase_dict)
    testcase.preconditions = build_testcase_preconditions(nodes)
    testcase.execution_type = get_execution_type(testcase_dict)
    steps_node = testcase_dict.get('topics', None)

    if steps_node:
        testcase.steps = parse_steps(steps_node)

    return testcase


def parse_steps(steps_dict):
    """ 解析用例步骤 """
    steps = []

    for step_number, step_node in enumerate(steps_dict, 1):
        step = parse_step(step_node)
        step.number = step_number

        steps.append(step)
    return steps


def parse_step(step_dict):
    """ 解析用例每一个步骤 """
    step = TestStep()
    step.action = step_dict['title']
    expected_node = step_dict.get('topics', None)
    if expected_node:
        step.expectedresults = expected_node[0]['title']

    return step


"""-------------下方为工具方法-----------------"""


def build_testcase_preconditions(nodes):
    """ """
    values = [n['comment'] for n in nodes if n.get('comment', None)]
    return ''


def build_testcase_summary(nodes):
    """" 获取用例summary """
    values = [n['note'] for n in nodes]
    values = _filter_empty_value(values)
    return _config['summary_sep'].join(values)


def build_testcase_title(nodes):
    """" 获取用例标题 """
    values = [n['title'] for n in nodes]
    values = _filter_empty_value(values)

    sep = cache.get('sep', ' -')

    if sep != ' ':
        sep = ' {} '.format(sep)

    return sep.join(values)


def _filter_empty_value(values):
    result = [v for v in values if v]
    for r in result:
        if not isinstance(r, str):
            assert '期望的类型应是str: {}'.format(r)
    return [v.strip() for v in result]


def get_priority(d):
    """
    获取此用例的优先级
    """
    if isinstance(d['makers'], list):
        for m in d['makers']:
            if m.startswith('priority'):
                return int(m[-1])


def get_execution_type(d):
    """
    获取用例执行方式。
    1代表手动，2代表自动化。其中以标记中的绿色旗帜（flag-green）代表自动化
    """
    if isinstance(d['makers'], list):
        if 'flag-green' in d['makers']:
            return 2
    return 1
