#!/usr/bin/env python
# coding:utf-8

import logging


LOG_FORMAT = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s'

config = {
    'name': 'xmind2xml',
    'level': 'DEBUG',
    'file': 'logs/all.log',
    'format': LOG_FORMAT
}


class LoggerHandler(logging.Logger):

    def __init__(self, name='root', level='DEBUG', file=None, format=None):
        super().__init__(name)
        #
        self.setLevel(level)
        #
        fmt = logging.Formatter(format)
        # fmt.asctime_format()
        #
        if file:
            file_handler = logging.FileHandler(file, encoding='utf-8')
            file_handler.setLevel(level)
            file_handler.setFormatter(fmt)
            self.addHandler(file_handler)
        # 如果没有日志文件，打印到控制台
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(fmt)
        self.addHandler(stream_handler)


logger = LoggerHandler(config['name'], config['level'],
                       config['file'], config['format'])
