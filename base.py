# coding:utf-8
# @Create time: 2021/3/29 4:40 下午
# @Author: KongJingchun
# @remark:


import os
import json
from common.consts import ROLES, FIRSTLEVELS, SECONDLEVELS
from common.utils import check_json, get_strtime
from common.error import UserExistsError, RoleError, LevelError, NegativeNumberError


class Base(object):
    def __init__(self, user_json, gift_json):
        self.user_json = user_json
        self.gift_json = gift_json
        check_json(self.user_json)
        check_json(self.gift_json)
        self.__init_gift()

    # 读取user.json文件获取用户信息
    def __read_users(self):
        with open(self.user_json, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
        return data

    # 写入新的用户啊到user.json
    def __write_user(self, **user):
        if not 'username' in user:
            raise ValueError('missing username')
        if not 'role' in user:
            raise ValueError('missing role')
        user['active'] = True
        now_time = get_strtime()
        user['createtime'] = now_time
        user['updatetime'] = now_time
        user['gifts'] = []

        users = self.__read_users()
        # 判断用户名是否已经存在
        if user['username'] in users:
            raise UserExistsError('username had  exists:%s' % user['username'])

        users.update(
            {user['username']: user}
        )
        self.__save(self.user_json, users)

    # 修改用户role信息
    def __change_role(self, username, role):
        users = self.__read_users()
        user = users.get(username)
        if not user:
            return False
        if role not in ROLES:
            raise RoleError('not use role %s' % role)
        user['role'] = role
        user['updatetime'] = get_strtime()
        users[username] = user
        self.__save(self.user_json, users)
        return True

    # 修改用户active信息
    def __change_active(self, username):
        users = self.__read_users()
        user = users.get(username)
        if not user:
            return False
        user['active'] = not user['active']
        user['updatetime'] = get_strtime()
        users[username] = user
        self.__save(self.user_json, users)
        return True

    # 删除用户
    def __delete_user(self, username):
        users = self.__read_users()
        user = users.get(username)
        if not user:
            return False
        delete_user = users.pop(username)
        self.__save(self.user_json, users)
        return delete_user

    # 读取奖品列表
    def __read_gifts(self):
        with open(self.gift_json, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
        return data

    # 初始化奖品列表
    def __init_gift(self):
        gifts = self.__read_gifts()
        if len(gifts) != 0:
            return
        print('初始化奖品列表')
        data = {
            'level1': {
                'level1': {

                },
                'level2': {},
                'level3': {}
            },
            'level2': {
                'level1': {},
                'level2': {},
                'level3': {}
            },
            'level3': {
                'level1': {},
                'level2': {},
                'level3': {}
            },
            'level4': {
                'level1': {},
                'level2': {},
                'level3': {}
            }
        }
        self.__save(self.gift_json, data)

    # 添加奖品
    def __write_gift(self, first_level, second_level, gift_name, gift_count):
        if first_level not in FIRSTLEVELS:
            raise LevelError('%s not in FIRSTLEVELS ' % first_level)
        if second_level not in SECONDLEVELS:
            raise LevelError('%s not in SECONDLEVELS' % second_level)
        gifts = self.__read_gifts()
        first_gift_pool = gifts[first_level]
        second_gift_pool = first_gift_pool[second_level]
        if gift_count <= 0:
            gift_count = 1
        # print(gift_name)
        # print(second_gift_pool)
        if gift_name in second_gift_pool:
            # print('存在')
            second_gift_pool[gift_name] = second_gift_pool[gift_name] + gift_count
        else:
            # print('不存在')
            second_gift_pool[gift_name] = gift_count
        first_gift_pool[second_level] = second_gift_pool
        gifts[first_level] = first_gift_pool
        self.__save(self.gift_json, gifts)

    # 删除奖品
    def delete_gift(self, first_level, second_level, gift_name):
        data = self.__check_level_and_giftname(first_level, second_level, gift_name)
        if not data:
            return False
        gifts, first_gift_pool, second_gift_pool = data[0], data[1], data[2]
        del_gift = second_gift_pool.pop(gift_name)
        first_gift_pool[second_level] = second_gift_pool
        gifts[first_level] = first_gift_pool
        self.__save(self.gift_json, gifts)
        return del_gift

    # 减少奖品数量
    def reduce_gift(self, first_level, second_level, gift_name, gift_count):
        data = self.__check_level_and_giftname(first_level, second_level, gift_name)
        if not data:
            return False
        gifts, first_gift_pool, second_gift_pool = data[0], data[1], data[2]
        if second_gift_pool[gift_name] - gift_count < 0:
            raise NegativeNumberError('It is negative after calculation')
        second_gift_pool[gift_name] -= gift_count
        first_gift_pool[second_level] = second_gift_pool
        gifts[first_level] = first_gift_pool
        self.__save(self.gift_json, gifts)

    # 检查登记和奖品名称是否正确
    def __check_level_and_giftname(self, first_level, second_level, gift_name):
        if first_level not in FIRSTLEVELS:
            raise LevelError('%s not in FIRSTLEVELS ' % first_level)
        if second_level not in SECONDLEVELS:
            raise LevelError('%s not in SECONDLEVELS' % second_level)
        gifts = self.__read_gifts()
        first_gift_pool = gifts[first_level]
        second_gift_pool = first_gift_pool[second_level]
        if gift_name not in second_gift_pool:
            return False
        return gifts, first_gift_pool, second_gift_pool

    # 修改file文件
    def __save(self, path, data):
        with open(path, 'w', encoding='utf-8')as f:
            f.write(json.dumps(data))


if __name__ == '__main__':
    user_path = os.path.join(os.getcwd(), 'storage', 'user.json')
    gift_path = os.path.join(os.getcwd(), 'storage', 'gift.json')
    base = Base(user_json=user_path, gift_json=gift_path)
    # base.write_user(username='kjc', role='admin')
    # result = base.change_role('wy', 'normal')
    # print(result)
    # result = base.change_active('wy')
    # print(result)
    # result = base.delete_user('wy')
    # print(result)
    # print(base.read_gifts())
    # base.init_gift()
    base.reduce_gift(first_level='level1', second_level='level1', gift_name='mac book pro', gift_count=1)
