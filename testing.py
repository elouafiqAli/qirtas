__TESTING__ = True
import facebook_dialy as facebook
import facebook as facebook_
import re, testdata
import sys
#from util import DotNotation, objectify
from collections import namedtuple

users = ['me']
test_token = 'CAACEdEose0cBACFVTFngOVlH3o1t2z7YksQQ9Us2fmHiZAojRk13gQWXgnVAMtW09lMwKq73pk5Vdi8HW9rxZBFRcZBUiZCuZBsZBvi352c97FihCrBf9o7lZAIAm86Q5l3cMEcFOU9w320twrSRq8HQsLLvuZAiRrmblc9ctxUyPZAOEAdDBKkV36VWcE14aV5qZCE0MAZB46n6AZDZD'

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
        post = Post(post_)
        print post.get_counters()

    return all_posts


class Post:
   # @objectify
    def get_counters(self):
        try:
            shares_response = graph.get_object(self.id, fields='shares')
            likes_response = graph.get_connections(self.id, 'likes', summary='true')
            comments_response = graph.get_connections(self.id, 'comments', summary='true')
        except Exception:
            return {}
        self.shares_count = shares_response['shares']['count'] if 'shares' in shares_response is True else 0
        self.likes_count = likes_response['summary']['total_count'] if 'summary' in likes_response is True else 0
        self.comments_count = comments_count['summary']['total_count'] if 'summary' in comments_count is True else 0

        counters = {'shares': self.shares_count, 'likes': self.likes_count, 'comments_count': self.comments_count}
        return counters

    def __init__(self, post):
        self.id = post['id']
        self.message = post['message']
        self.created_time = post['created_time']

        return None

    def __str__(self):
        return self.id

    #@objectify
    def get_contributors(self):

        comments, commenters, tagged, likers = [], [], [], []
        try:
            def get_likers():
                likers = []
                like_pages = graph.get_pages(self.id, 'likes')
                for like_list in like_pages:
                    likers.extend(like_list['data'])
                return likers
            likers = get_likers()
            comments_pages = graph.get_pages(
                self.id, 'comments', fields='like_count,message_tags,created_time,from')

            for comments_list in comments_pages:
                for comment in comments_list['data']:
                    # add comment to the list
                    comments.append(comment)

                    contributor = comment['from']

                    contributor['like_count'] = comment['like_count']
                    contributor['created_time'] = comment['created_time']
                    print contributor
                    # maps an id with a specific user
                    commenters.append(contributor)
                    try:
                        tagged.extend(comment['message_tags'])
                    except KeyError as e:
                        pass
        except Exception:
            return {}
        contributors = {'likers': likers,
                        'commenters': commenters,
                        'comments': comments,
                        'tagged': tagged
                        }
        return contributors


def test_cnt():
    all_posts = []
    posts = graph.get_pages('me', 'posts')
    for post_list in posts:
        for post_ in post_list['data']:
            post = Post(post_)
            print post.get_contributors()

        break

    return all_posts


if __name__ == '__main__':

    print test_cnt()
