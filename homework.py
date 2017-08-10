#!/usr/bin/env python3

import vk
import requests
import time

class VKUser(object):

    def __init__(self, vk_id):
        while True: # limit requests per second
            try:
                res = vkapi.users.get(user_ids=(vk_id,))[0]
                self.vk_id = vk_id
                self.first_name = res['first_name']
                self.last_name = res['last_name']
                self.friends = set(vkapi.friends.get(user_id=vk_id))
                self.common_friends = {}
            except vk.exceptions.VkAPIError as e:
                if 'Too many requests per second' in e.message:
                    time.sleep(0.5)
                    continue
                elif 'User was deleted or banned' in e.message:
                    self.vk_id = 0
                    self.first_name = 'DELETED'
                    self.last_name = 'DELETED'
                    self.friends = set()
                    self.common_friends = {}
                    break
            except requests.exceptions.ReadTimeout:
                time.sleep(0.5)
                continue
            break


def get_vkuser(vk_id):
    return VKUser(vk_id)

# name = input('VK login: ')
# password = input('VK password: ')
session = vk.AuthSession('3387347', 'doubletrouble-sk@yandex.ru', 'vk_T2claw')
vkapi = vk.API(session)
current_uid = vkapi.users.get()[0]['uid']

friends = []

for friend_id in vkapi.friends.get():
    try:
        friends.append(VKUser(friend_id))
    except vk.exceptions.VkAPIError as e:
        if 'User was deleted or banned' in e.message:
            pass
        else:
            raise

for idx, friend in enumerate(friends):
    for another_friend in friends[idx+1:]:
        common_friends = friend.friends & another_friend.friends
        if common_friends and common_friends != set((current_uid,)):
            friend.common_friends[another_friend] = map(get_vkuser, common_friends)

friends.sort(key=lambda x: len(x.common_friends), reverse=True)

print('5 друзей с наибольшим количеством общих связей')
print('==============================================')
print()
for friend in friends[:5]:
    for user, cfriends in friend.common_friends.items():
        print('Общие друзья {0.first_name} {0.last_name} ↔  {1.first_name} {1.last_name}:'.format(friend, user))
        for cfriend in cfriends:
            print('\t - {0.first_name} {0.last_name}'.format(cfriend))