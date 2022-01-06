import scrapy
import re
import json
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from instaparser.items import InstaparserItem
from copy import deepcopy


class InstacomSpider(scrapy.Spider):
    name = 'instacom'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = '#login#'
    inst_pwd = '#password#'

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.user = user

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.inst_login_link,
                                    method='POST',
                                    callback=self.login,
                                    formdata={'username': self.inst_login,
                                            'enc_password': self.inst_pwd},
                                    headers={'X-CSRFToken': csrf})

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data.get('authenticated'):
            yield response.follow(
                    f'/{self.user}',
                    callback=self.user_parse,
                    cb_kwargs={'username': self.user}
                )

    def user_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)

        url_following = f'https://i.instagram.com/api/v1/friendships/{user_id}/following/?count=12'

        yield response.follow(
            url_following,
            headers={'USER-AGENT': 'Instagram 155.0.0.37.107'},
            callback=self.following,
            cb_kwargs={'user_id': user_id,
                       'username': username})

        url_followers = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?count=12&search_surface=follow_list_page'

        yield response.follow(
            url_followers,
            headers={'USER-AGENT': 'Instagram 155.0.0.37.107'},
            callback=self.followers,
            cb_kwargs={'user_id': user_id,
                       'username': username})

    def following(self, response: HtmlResponse, user_id, username):
        j_data = response.json()
        if j_data.get('big_list'):
            variables = {'max_id': j_data.get('next_max_id')}
            url_following = f'https://i.instagram.com/api/v1/friendships/{user_id}/following/?count=12&{urlencode(variables)}'

            yield response.follow(
                url_following,
                headers={'USER-AGENT': 'Instagram 155.0.0.37.107'},
                callback=self.following,
                cb_kwargs={'user_id': user_id,
                           'username': username})

        posts = j_data.get('users')
        for post in posts:
            item = InstaparserItem(
                username_main=username,
                usertype='following',
                id_user=post.get('pk'),
                username=post.get('username'),
                userphoto=post.get('profile_pic_url')
            )
            yield item

    def followers(self, response: HtmlResponse, user_id, username):
        j_data = response.json()
        if j_data.get('big_list'):
            variables = {'max_id': j_data.get('next_max_id')}
            url_followers = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?count=12&{urlencode(variables)}&search_surface=follow_list_page'

            yield response.follow(
                url_followers,
                headers={'USER-AGENT': 'Instagram 155.0.0.37.107'},
                callback=self.followers,
                cb_kwargs={'user_id': user_id,
                           'username': username})

        posts = j_data.get('users')
        for post in posts:
            item = InstaparserItem(
                username_main=username,
                usertype='follower',
                id_user=post.get('pk'),
                username=post.get('username'),
                userphoto=post.get('profile_pic_url')
            )
            yield item

    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')