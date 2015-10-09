import token, facebook
import sys
from urlparse import urlparse, parse_qs


users = ['me']
test_token = 'CAACEdEose0cBALWl8S9PRAzTZAEIyvvbwtDO0fueDuHbmbVZBGckgivpSZCxyZAJYBT3BZCdXimCS5sDCTuqEWBWL3MHe30BSFxL8n87YJ7lZAf7kDacRmN2JCucvvwjIA43EWwQbedEghF7ZBJVHtfZA4z0pVwsZBfpbA6HFif1PbR32MBZArhVQraBCuGR1ZCtZAFc7gTYuOxkNwZDZD'
def get_graph(oauth_token):
	return facebook.GraphAPI(access_token=oauth_token)

def run_test():
	_graph = get_graph(test_token)
	all_posts = []

	#initilaizing the request --> /me/posts
	_a = {
		'id':'me',
		'edge':'posts',
		'args': {}
	}
	i=0
	while(True):
		try:
			#getting the list of posts
			response = _graph.get_connections(_a['id'],_a['edge'],_a['args'])
			#storing the posts
			all_posts.extend(response['data'])

			"""
				Getting the next url if available, if not it throws an exception to exit the loop
				We parse the next url to transform in into a valide get_connections request


			"""

			#the next url
			next = response['paging']['next']
			#we parse the url to 
			parsed_url = urlparse(next)		
			get_arguments =  parse_qs(parsed_url.query)
			print parsed_url
			print '--------'
			print get_arguments
			for key in get_arguments: 
				print get_arguments[key]
				get_arguments[key] = get_arguments[key][0]
			del get_arguments['access_token']

			"""
				The url:
				/v2.4/{id}/{edge}/access_token?={access_token}&arguments=value&cursor=value....
					the cursors are passed as parameters

			"""
			if i > 8 :
				break 
			_a = {

				'id': parsed_url.path.split('/')[2],
				'edge': parsed_url.path.split('/')[3],
				'args' : get_arguments
			}
			i = i + 1


		except KeyError:
			break


	

	return all_posts
if __name__ == "__main__":
	oauth_token = sys.argv[1]  if len(sys.argv) > 1 else token.get_token()
	_graph = get_graph(oauth_token)