import requests
from pprint import pprint

token = input("input token: ")
# with open('token.txt', 'r') as f:
#     token = f.read().strip()

url = 'http://api.vk.com/method/'
version = '5.126'


class VkUser:
    def __init__(self, owner_id=None):
        self.token = token
        self.url = url
        self.owner_id = owner_id
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version,
            'fields': 'photo_id, status'
        }
        if owner_id is None:
            self.owner_id = requests.get(self.url+'users.get', self.params).json()['response'][0]['id']

    def __str__(self):
        return str(f'https://vk.com/id{self.owner_id}')

    def user_info(self, user=None):
        if user is None:
            user = self.owner_id
        info_params = {
            'user_id': user,
            'fields': 'first-name, last_name, status'
        }
        owner = requests.get(self.url + 'users.get', params={**self.params, **info_params}).json()
        user_id = owner['response'][0]['id']
        user_name = owner['response'][0]['first_name']
        user_status = owner['response'][0]['status']
        print(f"{str(user_id)} \n {str(user_name)} \n {str(user_status)}")

    def get_friends(self, owner_id=None):
        if owner_id is None:
            owner_id = self.owner_id
        friend_url = self.url + 'friends.get'
        friend_params = {
            'count': 1000,
            'user_id': owner_id,
            'fields': 'first-name, last_name'
        }
        result = requests.get(friend_url, params={**self.params, **friend_params})
        friends = result.json()
        friends_data = friends['response']['items']
        all_friends = {}
        for item in friends_data:
            all_friends[str(item['first_name'] + ' ' + item['last_name'])] = item['id']
        print(f"Мои {len(all_friends)} друзей: ", all_friends)

    def get_albums(self, owner_id=None):
        if id is None:
            owner_id = self.owner_id
        album_url = self.url + 'photos.getAlbums'
        album_params = {
            'user_id': owner_id,
            'photo_sizes': 1
        }
        response = requests.get(album_url, params={**self.params, **album_params}).json()['response']
        count_albums = response['count']
        print("Количество альбомов = ", count_albums)
        albums_list = {}
        for items in response['items']:
            albums_list[str(items['id'])] = items['title']
        print(albums_list)

    def __and__(self, source_id=None, other_id=None):
        if source_id is None:
            source_id = self.owner_id
        self.other_id = other_id
        common_url = self.url + 'friends.getMutual'
        common_params = {
            'source_uid': source_id,
            'target_uid': self.other_id
        }
        resp = requests.get(common_url, params={**self.params, **common_params}).json()
        pprint(resp)
        for value in resp['response']:
            return value['common_friends']


user_1 = VkUser()
user_2 = VkUser(76065479)

# user_1.get_friends()
# user_2.get_friends()
#
# user_1.user_info()
user_1.get_albums()
# user_2.user_info(76065479)
# common_users = user_1 & user_2
