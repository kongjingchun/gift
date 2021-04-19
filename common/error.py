# coding:utf-8
# @Create time: 2021/3/29 4:40 下午
# @Author: KongJingchun
# @remark: 错误类

# 文件路径错误
class NotPathError(Exception):
    def __init__(self, message):
        self.message = message


# 文件格式错误
class FormatError(Exception):
    def __init__(self, message):
        self.message = message


# 是否为文件错误
class NotFileError(Exception):
    def __init__(self, message):
        self.message = message

# 用户不存在错误
class UserExistsError(Exception):
    def __init__(self, message):
        self.message = message

# 角色错误
class RoleError(Exception):
    def __init__(self, message):
        self.message = message


class LevelError(Exception):
    def __init__(self, message):
        self.message = message


class NegativeNumberError(Exception):
    def __init__(self, message):
        self.message = message


class NotUserError(Exception):
    def __init__(self, message):
        self.message = message


class NotAdminError(Exception):
    def __init__(self, message):
        self.message = message

# 用户权限错误
class UserActiveError(Exception):
    def __init__(self, message):
        self.message = message

class CountError(Exception):
    def __init__(self, message):
        self.message = message
