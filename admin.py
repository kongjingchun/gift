# coding:utf-8
# @Create time: 2021/4/6 3:13 下午
# @Author: KongJingchun
# @remark:
from base import Base
import os
from common.error import NotUserError, UserActiveError, NotAdminError, RoleError


class Admin(Base):
    def __init__(self, username, user_json, gift_json):
        self.username = username
        super().__init__(user_json, gift_json)
        self.get_user()

    # 获取用户信息
    def get_user(self):
        users = self._Base__read_users()
        current_user = users.get(self.username)
        if current_user is None:
            raise NotUserError('not user %s' % self.username)
        self.username = current_user.get('username')
        self.active = current_user.get('active')
        self.role = current_user.get('role')
        if self.active is False:
            raise UserActiveError('%s active is False' % self.username)
        if self.role != 'admin':
            raise RoleError('User role not admin')
        self.user = current_user

    # 添加用户
    def add_user(self, username, role):
        if self.role != 'admin':
            raise NotAdminError('%s role is not admin ' % self.username)
        self._Base__write_user(username=username, role=role)

    # 修改用户状态
    def update_user_active(self, username):
        if self.role != 'admin':
            raise NotAdminError('%s role is not admin ' % self.username)
        self._Base__change_active(username=username)

    # 修改用户权限
    def update_user_role(self, username, role):
        if self.role != 'admin':
            raise NotAdminError('%s role is not admin ' % self.username)
        self._Base__change_role(username=username, role=role)


if __name__ == '__main__':
    user_json_path = os.path.join(os.getcwd(), 'storage', 'user.json')
    gift_json_path = os.path.join(os.getcwd(), 'storage', 'gift.json')
    admin = Admin('kjc', user_json_path, gift_json_path)
    # print(admin.username, admin.role)
    admin.update_user_role(username='lxq', role='normal')
