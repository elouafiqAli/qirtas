import feedparser
d = feedparser.parse('https://www.facebook.com/feeds/notifications.php?id=1449493666&viewer=1449493666&key=AWgvVg1Dzzn1bEDO&format=rss20')

def is_new_post(post):
	_DEBUG_ = False
	#### CHECKER FUNCTIONS
	def has(origin,term): 
		#print origin,' ',term, ' ',len(origin.split(term))
		return len(origin.split(term)) == 2
	def is_not(origin,terms): 
		for term in terms: 	
			if has(origin,term) is True: 
				return False 
		return True

	__CHECKERS__ ={ 'has': has, 'is_not': is_not}

	__RULES__ ={
		'title':{
			'has': 'posted'
			},
		'link': {
			'is_not': ['groups','events']
		}

	}
	


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


def run():
	_posts = []
	for post in d.entries:
		if(is_new_post(post) == True):
			_link_attr = link_attr(post.link)
			_link_attr['published']=post.published
			_posts.append(_link_attr)

	print _posts
			

run()

