import random, names
import mongo, prawn

random_link =  lambda : 'http://'+names.get_last_name()+'.com'
random_links = lambda list_size: [ random_link() for i in range(list_size)]
meta_data = lambda link : {
					'comment_count'	:	random.randrange(20),
					'share_count'	:	random.randrange(20),
					'like_count'	:	random.randrange(20),
					'time_stamp'	: 	random.randrange(1000),
					'url'	:	link
				}
ramdom_metadata = lambda links: map(meta_data, links )


class StoringDataTests:
	def __init__(self):
 		self.SAMPLE = {}
		self.SAMPLE.LINKS =  random_links(SAMPLE.SIZE)
		self.SAMPLE.METADATA = ramdom_metadata(SAMPLE.LINKS)

    def test_saving_links_in_mongo(self):

    	#if flush == True: mongo._db.links.delete_many({})
    	# The function we are testing
    	mongo.save_links(self.SAMPLE.LINKS)
        cursor = mongo._db.links.find()
       	fetched_links = [ line['url'] for line in cursor]
        for line in self.SAMPLE.LINKS:
        	assert line in fetched_links
    """
    def test_facebook_meta_data(self)
        db_content_list = [ line for line in db_content ]
        for i in range(len(db_content_list)):
        	self.assertEqual(SAMPLE_LINKS[i],)
        for line in db_content:
        	self.assertEqual(SAMPLE_LINKS,)
	"""
 



