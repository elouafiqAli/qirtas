__TESTING__ = False
import facebook_dialy as facebook
import facebook as facebook_
import re, testdata
import sys
#from util import DotNotation, objectify
from collections import namedtuple

users = ['me']
test_token = 'CAACEdEose0cBAPWpUmQS7z8w1jcGjKsGcE4r7qVsLS4UmZCOA2Ofx2KRZCEsJmXkwKmSx9iszFrrLhb9Vz3VfjB4mYi4Uqt1OZAkfqrI2ZBatC6Mi7v16yH7680zdBsJVUj9QFTJfGZAZAHSSu5cpETX8IE9lON2ITs9B9P4N6JmZBC1W2hdWKafpMzTH1MEVTF4qrtVZAdsVgZDZD'

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
        self.message = post['message']
        self.created_time = post['created_time']

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
            self.__shares = shares_response
        else:
            self.__shares = 0
        return self.__shares


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
        self.mentioned = tagged




def test_cnt():
    all_posts = []
    print 'getting connection'
    posts = graph.get_pages('me', 'posts')
    print '--->>'
    for post_list in posts:
        for post_ in post_list['data']:
            if 'message' in post_:
                post = Post(post_)
                #likes = post.likes
                comments = post.comments
                print comments.__dict__
        break

    return all_posts


if __name__ == '__main__':

    print test_cnt()
