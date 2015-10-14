import testdata
def cached_paths(self,path):
    cache = {
            "%s/%s/%s" % (self.version, '(.*)','posts') : testdata.test_feed,
            "%s/%s/%s" % (self.version, '(.*)','comments') : testdata.test_comments
        }
	for test_path in cache:
		if re.match(test_path,path):
		    return cache[test_path]
		raise Exception(path)

if __name__ == '__main__':
	try: 
		a = object()
		a.version = 'v2.4'
		print cached_paths(a,'v2.4/me/posts').keys()
		print cached_paths(a,'v2.4/010010001011/comments').keys()
		print cached_paths(a,'v2.4/django')
	except Exception as error:
		print error.message
