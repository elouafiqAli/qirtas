import feedparser, facebook, urllib2

"""
	CONFIGURATION VARIABLES
"""

graph = facebook.GraphAPI(access_token='CAACEdEose0cBAFzdOZCGwb48LdLUY1oT2QyhJnTMdk6omPZA3L2mfRc4LPSXeKLt9qVhZBvTYmZBEDdjackQnEaKxOiZBlDfZAMbpVCTZA7TjfZAax2HBcBlZBHLNoeXIRBE3HgAsvCO9RR6WfWWthishjjYEFSmnN35qGyas9NnRaBorZB8KuurpRhXQBpMTbAJLj7RF9YRVxmwZDZD',version='2.3')
d = feedparser.parse('https://www.facebook.com/feeds/notifications.php?id=1449493666&viewer=1449493666&key=AWgvVg1Dzzn1bEDO&format=rss20')

_FQL_ = { 
	'base_url':'https://api.facebook.com/method/fql.query?query=',
	'link_stat': lambda link: "SELECT%20comment_count,%20share_count,%20like_count%20FROM%20link_stat%20WHERE%20url%20=\""+link+"\""
	#'link_stat': lambda link: "SELECT comment_count, share_count, like_count FROM link_stat WHERE url =\""+link+"\""
	
}

def has(origin,term): 
	#print origin,' ',term, ' ',len(origin.split(term))
	return len(origin.split(term)) == 2
def is_not(origin,terms): 
	for term in terms: 	
		if has(origin,term) is True: 
			return False 
	return True

__CHECKERS__ ={ 
	'has': has, 
	'is_not': is_not
}

__RULES__ ={
	'title':{
		'has': 'shared'
		},
	'link': {
		'is_not': ['groups','events']
	}

}

def is_new_post(post):
	_DEBUG_ = False
	#### CHECKER FUNCTIONS
	

	if _DEBUG_: print post.title

	for attribute in __RULES__:
		for rule in __RULES__[attribute]:
			if _DEBUG_ : 
				print "\t[",attribute,":",rule,str(__RULES__[attribute][rule]),"] "
				print "\t"+str(__CHECKERS__[rule](post[attribute],__RULES__[attribute][rule]))
			if __CHECKERS__[rule](post[attribute],__RULES__[attribute][rule]) is False:
				return False
			#_is_new_post = _is_new_post and __CHECKERS__[rule](post[attribute],__RULES__[attribute][rule])
	
	return True

def link_attr(link):
	_link = link.split('/n/')[1]
	POST = {}
	POST['source'] = _link.split('%2F')[0].split('?')[1]
	POST['post_id'] = _link.split('%2F')[2].split('&')[0]
	POST['aref']= _link.split('%2F')[2].split('&')[1].split('aref=')[1]
	return POST


def rss_links():
	feed_posts = {}
	for post in d.entries:
		if(is_new_post(post) == True):
			_link_attr = link_attr(post.link)
			_link_attr['published']=post.published
			feed_posts[_link_attr['post_id']] = _link_attr

	real_posts = graph.get_objects(feed_posts.keys())
	clean_posts = list()
	for post_id in feed_posts:	
		post = real_posts.get(post_id)
		if post is not None:
			link = post.get('link')
			if link is not None:
				print link
				clean_posts.append(link)
	return clean_posts
			
def facebook_meta_data(link):
	print link
	attributes_count = 3
	attributes_fields = ['comment_count','share_count', 'like_count']
		

	query_result = urllib2.urlopen(_FQL_['base_url']+_FQL_["link_stat"](link)) 
	response = query_result.readlines()
	
	link_data = dict()
	
	for i in range(attributes_count,attributes_count+len(attributes_fields)):
		link_data[attributes_fields[i-attributes_count]] = response[i].split('<')[1].split('>')[1]

	return link_data 
if __name__ == "__main__":
	links = rss_links()
	print links
	for link in links:
		print facebook_meta_data(link)


