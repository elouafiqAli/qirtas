import token
import facebook_dialy as facebook
import facebook as facebook_
import re, testdata
import sys
from util import DotNotation, objectify
from collections import namedtuple

users = ['me']
test_token = 'CAACEdEose0cBAD4is3LUoiGCysrqFF4ljDZCTXPAuyVtQ4R6zMCdppLNs2IbaegmYtWFIXGSzEha4JEJGt49ullBYYeuxZAZCLTHTXEjlINIZBFHfGTv9BIL04ZCQRkpTjf4eFgAPnQgHy34ZCapD5VFwvfFZCNDkrFoNDZAjPGZBhgyrUVHARqi7ySpwFXK2IhJGfcUWLGCcjwZDZD'

class TestingFacebook(facebook.GraphAPI):

    def cached_paths(self,path):
        cache = {
                "%s/%s/%s" % (self.version, '(.*)','posts') : testdata.test_feed,
                "%s/%s/%s" % (self.version, '(.*)','comments') : testdata.test_comments,
            }[path]

        for test_path in cache:
            if re.match(test_path,path):
                return cache[test_path]
            raise Exception

    def request(self,*args, **kargs):
        path = args[0]
        def cached_paths(self,path):
            cache = {
                    "%s/%s/%s" % (self.version, '(.*)','posts') : testdata.test_feed,
                    "%s/%s/%s" % (self.version, '(.*)','comments') : testdata.test_comment
            }

            for test_path in cache:
                if re.match(test_path,path):
                    return cache[test_path]
            raise Exception(path)

        try:
            result = cached_paths(path)
            return result
        except Exception:
            return super(TestingFacebook,self).request(path,kargs)

_fb_api_version = '2.4'
graph = TestingFacebook(test_token)



def get_posts():
    all_posts = []
    posts = graph.get_pages('me', 'posts')

    for post_list in posts:
        all_posts.extend(post_list.data)

    for post_ in all_posts[:10]:
        post = Post(post_)
        print post.get_counters()

    return all_posts


class Post:
   # @objectify
    def get_counters(self):
        self.shares_count = graph.get_object(self.id, fields='shares').shares.count or 0
        self.likes_count = graph.get_connections(self.id, 'likes', summary='true').summary.total_count or 0
        self.comments_count = graph.get_connections(self.id, 'comments', summary='true').summary.total_count or 0

        counters = {'shares': self.shares_count, 'likes': self.likes_count, 'comments_count': self.comments_count}
        return counters

    def __init__(self, post):
        self.id = post.id
        self.message = post.message
        self.created_time = post.created_time

        return None

    def __str__(self):
        return self.id

    #@objectify
    def get_contributors(self):

        comments, commenters, tagged, likers = [], [], [], []

        def get_likers():
            likers = {}
            like_pages = graph.get_pages(self.id, 'likes')
            for like_list in like_pages:
                likers.extend(like_list.data)
            return likers

        comments_pages = graph.get_pages(
            self.id, 'comments', fields='like_count,message_tags,created_time,from')

        for comments_list in comments_pages:
            for comment in comments_list.data:
                # add comment to the list
                comments.append(comment)
                print comment
                contributor = comment.from_
                contributor.like_count = comment.like_count
                contributor.created_time = comment.created_time

                # maps an id with a specific user
                commenters.append(contributor)
            try:
                tagged.extend(comment.message_tags)
            except AttributeError as e:
                pass

        contributors = {'likers': get_likers(),
                        'commenters': commenters,
                        'comments': comments,
                        'tagged': tagged
                        }
        return contributors


def test_cnt():
    all_posts = []
    posts = graph.get_pages('me', 'posts')
    for post_list in posts:
        for post_ in post_list.data:
            post = Post(post_)
            #print dir(post)
            print post.get_contributors()

        break

    return all_posts


if __name__ == '__main__':

    print test_cnt()
