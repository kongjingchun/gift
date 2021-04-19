# coding:utf-8
# @Create time: 2021/4/19 3:44 下午
# @Author: KongJingchun
# @remark:

from base import Base
import os
import random
from common.utils import timestamp_to_string
from common.error import UserExistsError, UserActiveError, RoleError, CountError
import time


class User(Base):
    def __init__(self, username, user_json, gift_json):
        self.user_json = user_json
        self.username = username
        super(User, self).__init__(user_json, gift_json)
        self.gift_random = list(range(1, 101))
        self.get_user()

    def get_user(self):
        self.users = self._Base__read_users()
        if self.username not in self.users:
            raise UserExistsError('not user %s' % self.username)
        self.user = self.users.get(self.username)
        self.active = self.user.get('active')
        if self.active == False:
            raise UserActiveError('%s active is False' % self.username)
        self.role = self.user.get('role')
        if self.role != 'normal':
            raise RoleError('User role not noemal')
        self.gifts = self.user.get('gifts')
        self.create_time = self.user.get('create_time')

    # 获取所有奖品
    def get_gifts(self):
        gifts = self._Base__read_gifts()
        gift_lists = []
        for level_one, level_one_pool in gifts.items():
            for level_two, level_two_pool in level_one_pool.items():
                for name in level_two_pool.keys():
                    gift_lists.append(name)
        return gift_lists

    def choice_gift(self):
        level_one_number = random.choice(self.gift_random)
        if 1 <= level_one_number <= 50:
            first_level = 'level1'
        elif 51 <= level_one_number <= 80:
            first_level = 'level2'
        elif 81 <= level_one_number <= 95:
            first_level = 'level3'
        elif 96 <= level_one_number <= 100:
            first_level = 'level4'
        else:
            raise CountError('level_one_number need 0~100')
        gifts = self._Base__read_gifts()
        first_gifts = gifts.get(first_level)
        level_two_number = random.choice(self.gift_random)
        if 1 <= level_two_number <= 80:
            second_level = 'level1'
        elif 81 <= level_two_number <= 95:
            second_level = 'level2'
        elif 96 <= level_two_number <= 100:
            second_level = 'level3'
        else:
            raise CountError('level_two_number need 0~100')
        second_gifts = first_gifts.get(second_level)
        gift_names = []
        if len(second_gifts) == 0:
            print('很遗憾，您没有中奖')
            return
        for k, _ in second_gifts.items():
            gift_names.append(k)
        gift_name = random.choice(gift_names)
        print(gift_name)
        if second_gifts[gift_name] <= 0:
            print('很遗憾，您没有中奖')
            return
        self._Base__update_gift(first_level=first_level, second_level=second_level, gift_name=gift_name)
        self.user[gifts].append(gift_name)
        self.users[self.user] = self.user
        self._Base__save(path = self.user_json, data = self.users)


if __name__ == '__main__':
    user_json_path = os.path.join(os.getcwd(), 'storage', 'user.json')
    gift_json_path = os.path.join(os.getcwd(), 'storage', 'gift.json')
    user = User('lxq', user_json_path, gift_json_path)
    user.choice_gift()
