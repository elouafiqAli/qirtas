import token, facebook
import sys
from urlparse import urlparse, parse_qs
from multiprocessing import Pool

users = ['me']
test_token = 'CAACEdEose0cBAEONElBEbR6MpnNE5fXprkpfDzakUMimIAbqu3NCc5C6SCLFZC6uySXgVdZBVYmGmp5o97a66eB9Sbwo0mcqnpFvZC3ZBDRHiYFBtFWka1n4e9U8NyaZAl35vcUpU0kZB62xZCZBImZC5SzHf8XiznrLCwZAI0PQB8bZAkZBkgEcyuNrgLzxIERRNv0FfSZAuIZBrJoAZDZD'


_fb_api_version = '2.4'
graph = facebook.GraphAPI(test_token,version =_fb_api_version )


def get_posts():
	all_posts = []
	posts = graph.get_connections_paging('me','posts',{})
	for post_list in posts: 
		all_posts.extend(post_list['data'])
		
	return all_posts

def get_post(id):
	shares = graph.get_object(id,fields='shares')
	likes = graph.get_conne
