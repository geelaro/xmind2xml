#!/usr/bin/env python
# coding:utf-8

"""
Desc: 用例的data类型
"""


class TestSuit():
    name = ''
    details = ''
    sub_suits = None
    testcase_list = None

    def to_dict(self):
        me = {
            'name': self.name,
            'details': self.details,
            'testcase_list': [],
            'sub_suits': []
        }

        if self.testcase_list:
            for t in self.testcase_list:
                me['testcase_list'].append(t.to_dict())

        if self.sub_suits:
            for s in self.sub_suits:
                me['sub_suits'].append(s.to_dict())

        return me


class TestCase():
    name = ''
    summary = ''
    # 前提
    preconditions = ''
    # 重要性：1高、2中、3低，默认中
    importance = 2
    # 执行方式：1手动、2自动，默认为手动
    execution_type = 1
    steps = None

    def to_dict(self):
        me = {
            'name': self.name,
            'summary': self.summary,
            'preconditions': self.preconditions,
            'importance': self.importance,
            'execution_type': self.execution_type,
            'steps': []
        }

        if self.steps:
            for s in self.steps:
                me['steps'].append(s.to_dict())

        return me


class TestStep():
    number = 1
    action = ''
    expectedresults = ''
    execution_type = 1

    def to_dict(self):
        me = {
            'number': self.number,
            'action': self.action,
            'expectedresults': self.expectedresults,
            'execution_type': self.execution_type
        }

        return me


cache = {}
