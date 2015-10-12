import token, facebook_dialy as facebook
import sys

from collections import namedtuple

users = ['me']
test_token = 'CAACEdEose0cBAHmEZCYPlE6NWSZA1PEw3kuObONUJic4PKP4xRcJMXOcsZCXHAIFHQwgyYY8ZCM7cLLWV1s3DQZBZAAs0CTkiRDKCOQvdyyWQCxi62y5ggERcCdZAAmVXGIjZAp4VIWjdwnHUiILZCau2p1ZCRVRuVg2K8a5kVERn6w9FqUZAIPlHiBPuttah0kcN2uFVvRO2qHHwZDZD'



_fb_api_version = '2.4'
graph = facebook.GraphAPI(test_token)


def get_posts():
	all_posts = []
	posts = graph.get_pages('me','posts')
	for post_list in posts: 
		all_posts.extend(post_list.data)
		
	return all_posts


"""
def get_post(id):
	
	UsersContributed = namedtuple('UsersContributed','likes comments tagged')
	User = namedtuple('User','id name type count')

	users_contributed = UsersContributed(likes=[],commenters=[],tagged=[])


	shares_ = graph.get_object(id,fields='shares')['shares']['count']
	likes_ 	= graph.get_connections_paging(id,'likes')['data']
	comments_ = graph.get_connections_paging(id,'comments')
	
	for like in likes_
		users_contributed.likes.extend(like['data'])

	
	for comment_list in comments_:
		for comment in comment_list['data']:

			contributor_ = comment['from']
			comment_ = graph.get_connections(comment['id'],fields='message_tags,likes_count,created_time')
			user = User(id = contributor_['id'])
			if contributor_ in users_contributed['commenters']:
				users_contributed['commenters'][contributor]["comments_count"]

			users_contributed[""]
	
"""


