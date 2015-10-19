from __future__ import division
from math import sqrt, pow
import facebook_dialy as facebook

all_friends = 0

class User:
    def __init__(self,session_token):
        global graph, all_friends
        graph = facebook.GraphAPI(session_token)
        all_friends = graph.get_connections('me','friends',summary='true')['summary']['total_count']

    @property
    def posts(self):
        try:
            return self.__posts
        except AttributeError:
            self.__posts = []
            posts = graph.get_pages('me', 'posts',fields='privacy,shares')
            for post_list in posts:
                for post in post_list['data']:
                    self.__posts.append(Post(post))
                break
            return self.__posts


class Post:
    def __init__(self, post):
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
    def reach(self):

        LIKES = len(self.likes)
        SHARES = self.shares
        UNIQUE_COMMENTS = len(self.comments.users)
        USERS_MENTIONED = len(self.mentions)
        FRIENDS = all_friends
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



