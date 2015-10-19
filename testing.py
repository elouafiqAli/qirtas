from __future__ import division
from math import sqrt, pow


__TESTING__ = False
import facebook_dialy as facebook
import facebook as facebook_
import re, testdata
import sys
#from util import DotNotation, objectify
from collections import namedtuple

users = ['me']
test_token = 'CAACEdEose0cBABoeXft8vsDJ8xaZBqrePCEAy98i70xLz9TevO6I99Jkakz5d8kfjx4YcZCttVb3HAZCZA5BLRExm8bZBcZAPmDsp2HaBfZCTrE2Iwn4HH1ZAzSmKlOWKEnqM6D87Rsm5S0mkwmVdgbAuWc506ScZCUdRv7uTnLrHUvLtgXtZB5kZBxEsyrdvYZAKQQM0gydOzkYkAZDZD'

class TestingFacebook(facebook.GraphAPI):

    def cached_paths(self,path):
        cache = {
                "%s/%s/%s" % (self.version, '(.*)','posts') : testdata.test_feed,
                "%s/%s/%s" % (self.version, '(.*)','comments') : testdata.test_comments
        }

        for test_path in cache:
            if re.match(test_path,path):
                return cache[test_path]
        raise Exception(path)

    def request(self,*args, **kargs):
        path = args[0]
        try:
            result = self.cached_paths(path)
            return result
        except Exception:
            return super(TestingFacebook,self).request(path,kargs)

_fb_api_version = '2.4'
if __TESTING__ is True:
    graph = TestingFacebook(test_token)
else:
    graph = facebook.GraphAPI(test_token)


def get_posts():
    all_posts = []
    posts = graph.get_pages('me', 'posts')

    for post_list in posts:
        all_posts.extend(post_list['data'])

    for post_ in all_posts[:10]:
        if 'message' in post_:
            post = Post(post_)
            print post.get_counters()

    return all_posts


class Post:
   # @objectify
    def __init__(self, post):
        print post
        self.id = post['id']

        if 'privacy' in post: self.__privacy = post['privacy']['value']
        if 'shares' in post: self.__shares = post['shares']['count']


    @property
    def likes(self):
        try:
            return self.__likes
        except AttributeError:
            self.__likes = Likes(self)
            return self.__likes

    @property
    def comments(self):
        try:
            return self.__comments
        except AttributeError:
            self.__comments = Comments(self)
            return self.__comments

    @property
    def shares(self):
        shares_response = graph.get_object(self.id, fields='shares')
        if 'shares' in shares_response:
            self.__shares = shares_response['shares']['count']
        else:
            self.__shares = 0
        return self.__shares

    @property
    def mentions(self):
        try:
            return self.__mentions
        except AttributeError:
            self.__mentions = self.comments.mentions

            mention_attributes = ['message_tags','story_tags']
            post_mentions = graph.get_object(self.id,fields=','.join(mention_attributes))
            for attribute in mention_attributes:
                if attribute in post_mentions:
                    self.__mentions.extend(post_mentions[attribute])
            return self.__mentions
    @property
    def privacy(self):
        try:
            return self.__privacy
        except AttributeError:
            self.__privacy = graph.get_object(self.id,fields='privacy')['privacy']['value']
            return self.__privacy

    @property
    def all_friends(self):
        try:
            return self.__friends
        except AttributeError:
            friends = graph.get_connections('me','friends',summary='true')
            self.__friends = friends['summary']['total_count']
            return self.__friends


    @property
    def reach(self):

        LIKES = len(self.likes)
        SHARES = self.shares
        UNIQUE_COMMENTS = len(self.comments.users)
        USERS_MENTIONED = len(self.mentions)
        FRIENDS = self.all_friends
        print 'UNIQUE_COMMENTS ',UNIQUE_COMMENTS,' USERS_MENTIONED ',USERS_MENTIONED,' LIKES ',LIKES, ' SHARES ',SHARES
        STICKINESS = sqrt( ( UNIQUE_COMMENTS + USERS_MENTIONED ) * LIKES / 7 )+ sqrt( SHARES * LIKES + SHARES ** 2 )
        REACH = 0

        if UNIQUE_COMMENTS is 0:
            REACH = (LIKES+USERS_MENTIONED)*16+ SHARES*33
        else:
            REACH = (LIKES+USERS_MENTIONED)*8 + (FRIENDS-LIKES) * pow(2, - 33 / STICKINESS )
        if self.privacy is 'EVERYONE':
            return REACH
        else:
            if REACH > FRIENDS: return FRIENDS
            else: return REACH



class Likes:
    def __init__(self,post):
        self.post = post

    @property
    def likes(self):

        def get_likers():
            likers = []
            like_pages = graph.get_pages(self.post.id, 'likes')
            for like_list in like_pages:
                likers.extend(like_list['data'])
            return likers

        self.__likes = get_likers()
        return self.__likes

    def __len__(self):
        try:
            return len(self.__likes)
        except AttributeError:
            likes = graph.get_connections(self.post.id, 'likes', summary='true')
            if 'summary' in likes:
                return likes['summary']['total_count']
            else:
                return 0


class Comments:
    def __init__(self,post):
        self.post = post
        comments, commenters, tagged = [], [], []
        comments_pages = graph.get_pages(
            self.post.id, 'comments', fields='like_count,message_tags,created_time,from')

        for comments_list in comments_pages:
            for comment in comments_list['data']:

                comments.append(comment)
                contributor = comment['from']
                contributor['like_count'] = comment['like_count']
                contributor['created_time'] = comment['created_time']
                commenters.append(contributor)

                try:
                    tagged.extend(comment['message_tags'])
                except KeyError:
                    pass

        users = {}
        for user in commenters:
            id = user['id']
            if id in users:
                users[id]['like_count'] += user['like_count']
                users[id]['comments'] += 1
            else:
                users[id] = user
                users[id]['comments'] = 1

        self.comments = comments
        self.users = users
        self.mentions = tagged



def test_cnt():
    all_posts = []
    print 'getting connection'
    posts = graph.get_pages('me', 'posts',fields='privacy,shares')
    print '--->>'
    for post_list in posts:
        for post_ in post_list['data']:
            post = Post(post_)
            print post.reach

        break

    return all_posts


if __name__ == '__main__':

    print test_cnt()
