# coding:utf-8
# @Create time: 2021/3/29 4:40 下午
# @Author: KongJingchun
# @remark: 工具类
import os
import time
from .error import NotPathError, FormatError, NotFileError


# 判断user和gift文件及路径是否正确
def check_json(path):
    # 判断能否找到路径
    if not os.path.exists(path):
        raise NotPathError('not found path %s' % path)
    # 判断文件是否是json格式
    if not path.endswith('.json'):
        raise FormatError('not json file: %s' % path)
    # 判断最终是否是文件
    if not os.path.isfile(path):
        raise NotFileError('not file: %s' % path)


# 获取时间字符串
def get_strtime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
