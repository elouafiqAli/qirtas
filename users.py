import facebook_dialy as facebook
from analysis import reach_estimation, reach_ratio

__caching__ = True
__cache_database__ = 'cacheDB'


class User:
    def __init__(self, session_token):
        self.graph = facebook.GraphAPI(session_token, caching = __caching__, cache_database=__cache_database__)
        me =  self.graph.get_object('me')
        self.id,self.name = me['id'], me['name']
        self.all_friends = self.graph.get_connections(self.id, 'friends', summary='true')['summary']['total_count']

    def counted_posts(self, ran = 0):
        try:
            ran_ = len(self.__posts) if ran == -1 else ran
            return self.__posts[:ran_]
        except:
            self.__posts = []
            ran_counter = 0
            posts = self.graph.get_pages(self.id, 'posts', fields='privacy,shares')
            for post_list in posts:
                for post in post_list['data']:
                    self.__posts.append(Post(post,self))
                    if ran == ran_counter:
                        break
                    ran_counter += 1
            return self.__posts

    @property
    def posts(self):
        try:
            return self.__posts
        except AttributeError:
            self.__posts = []
            posts = self.graph.get_pages(self.id, 'posts', fields='privacy,shares')
            for post_list in posts:
                for post in post_list['data']:
                    self.__posts.append(Post(post,self))
                #break
            return self.__posts

    @property
    def reach(self):
        sorted_posts = sorted(self.posts, key = Post.reach, reverse =  True)
        top_elements = [post.reach() for post in sorted_posts[:7]]
        ratio = reach_ratio(top_elements)
        return ratio

    def top_posts(self, limit = 0):
        _top_posts = sorted(self.counted_posts(limit), key = Post.reach, reverse =  True)
        return _top_posts

    def first_posts(self, limit = 0):
        sorted_posts = sorted(self.posts, key = Post.reach, reverse = True)
        _first_posts = sorted_posts[:limit]
        return _first_posts


class Post:
    def __init__(self, post, parent):
        self.graph = parent.graph
        self.parent = parent
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
        shares_response = self.graph.get_object(self.id, fields='shares')
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

            mention_attributes = ['message_tags', 'story_tags']
            post_mentions = self.graph.get_object(self.id, fields=','.join(mention_attributes))
            for attribute in mention_attributes:
                if attribute in post_mentions:
                    self.__mentions.extend(post_mentions[attribute])
            return self.__mentions

    @property
    def privacy(self):
        try:
            return self.__privacy
        except AttributeError:
            answer = self.graph.get_object(self.id, fields='privacy')
            print answer
            self.__privacy = answer['privacy']['value']
            return self.__privacy


    def reach(self):
        estimation =  reach_estimation(unique_comments = len(self.comments.users), users_mentioned=len(self.mentions),
                                friends = self.parent.all_friends, likes = len(self.likes), shares=self.shares,
                                privacy = self.privacy)
        return estimation


class Likes:
    def __init__(self, post):
        self.post = post
        self.graph = post.graph

    @property
    def likes(self):

        def get_likers():
            likers = []
            like_pages = self.graph.get_pages(self.post.id, 'likes')
            for like_list in like_pages:
                likers.extend(like_list['data'])
            return likers

        self.__likes = get_likers()
        return self.__likes

    def __len__(self):
        try:
            return len(self.__likes)
        except AttributeError:
            likes = self.graph.get_connections(self.post.id, 'likes', summary='true')
            if 'summary' in likes:
                return likes['summary']['total_count']
            else:
                return 0


class Comments:
    def __init__(self, post):
        self.post = post
        self.graph = post.graph
        comments, commenters, tagged = [], [], []
        comments_pages = self.graph.get_pages(
            self.post.id, 'comments', fields='like_count,message_tags,created_time,from')

        for comments_list in comments_pages:
            for comment in comments_list['data']:

                comments.append(comment)
                contributor = comment['from']
                if 'like_count' in contributor:
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
                if 'like_count' in user:
                    users[id]['like_count'] += user['like_count']
                users[id]['comments'] += 1
            else:
                users[id] = user
                users[id]['comments'] = 1
                users[id]['like_count'] = 0

        self.comments = comments
        self.users = users
        self.mentions = tagged
