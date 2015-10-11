import token, facebook
import sys
from urlparse import urlparse, parse_qs


users = ['me']
test_token = 'CAACEdEose0cBAPpZCp4PZA9lQSRqJQSsk4glIDCpfq0S4LbQTLVKHeuoGIZBQlVFcguuEniWpZAahUWoXdoaOUnLfrrDezSZCDRSpIE7TcXRq22f603wZAceGTE8g93hGK6NvOEImNYTCzdKPZAstNz6AVmSV5ny1qbaToItIE4vJUOXbPvoQ6yplGrQ9biJ57fkxi6q4tCCQZDZD'


_fb_api_version = '2.4'

def graph_request(url):
	path = url.split(_fb_api_version)[1].split('/') if len(url.split('/v2')) > 1 else url.split('/')
	
	node = path[1] 
	edge = path[2].split('?')[0]
	params = parse_qs(urlparse(url).query) if len(path) > 2 else {}
	
	try:
		del params['access_token']
	except:
		pass

	request =  { 'node':  node, 'edge' : edge, 	'params' : params }
	return request


class bennay:
	def __init__(self,oauth_token,api_version=_fb_api_version):
		self.graph = facebook.GraphAPI(access_token=oauth_token,version = api_version)
		self.all_posts = []

	def paging(self,path):
		request = graph_request(path)
		
		while True:
			try:
				print request
				response = self.graph.get_connections(request['node'],request['edge'],request['params'])
				yield response
				request = graph_request(response['paging']['next'])

			except KeyError:
				raise StopIteration

	def get_posts(self):
		all_posts = []
		posts = self.paging('/me/posts')
		while True:
			try:
				all_posts.extend(posts.next()['data'])
			except StopIteration:
				return all_posts

# --- used for interactive shell testing
def tee():
	reload(testing)
	ben = testing.bennay(testing.test_token)
	return ben.get_posts()
