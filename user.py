# coding:utf-8
# @Create time: 2021/4/19 3:44 下午
# @Author: KongJingchun
# @remark:

from base import Base
import os
from common.utils import timestamp_to_string
from common.error import UserExistsError, UserActiveError, RoleError


class User(Base):
    def __init__(self, username, user_json, gift_json):
        self.username = username
        super(User, self).__init__(user_json, gift_json)
        self.get_user()

    def get_user(self):
        users = self._Base__read_users()
        if self.username not in users:
            raise UserExistsError('not user %s' % self.username)
        self.user = users.get(self.username)
        self.active = self.user.get('active')
        if self.active == False:
            raise UserActiveError('%s active is False' % self.username)
        self.role = self.user.get('role')
        if self.role != 'normal':
            raise RoleError('User role not noemal')
        self.gifts = self.user.get('gifts')
        self.create_time = self.user.get('create_time')

    def get_gifts(self):
        gifts = self._Base__read_gifts()
        gift_lists = []
        for level_one,level_one_pool in gifts.items():
            for level_two,level_two_pool in level_one_pool.items():
                for name in level_two_pool.keys():
                    gift_lists.append(name)
        return gift_lists

if __name__ == '__main__':
    user_json_path = os.path.join(os.getcwd(), 'storage', 'user.json')
    gift_json_path = os.path.join(os.getcwd(), 'storage', 'gift.json')
    user = User('lxq', user_json_path, gift_json_path)
    result = user.get_gifts()
    print(result)
