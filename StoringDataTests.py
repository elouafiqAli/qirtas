import random, names, unittest
import mongo
from util import *

random_link =  lambda : 'http://'+names.get_last_name()+'.com'
random_links = lambda list_size: [ random_link() for i in range(list_size)]
meta_data = lambda link : {
                    'comment_count' :   random.randrange(20),
                    'share_count'   :   random.randrange(20),
                    'like_count'    :   random.randrange(20),
                    'time_stamp'    :   random.randrange(1000),
                    'url'   :   link
                }
ramdom_metadata = lambda links: map(meta_data, links )


class StoringDataTests(unittest.TestCase):

    SAMPLE_SIZE = 20
    SAMPLE_LINKS =  random_links(SAMPLE_SIZE)
    SAMPLE_METADATA = ramdom_metadata(SAMPLE_LINKS)
          

    def setUp(self):
        mongo.LinksCollection.delete_many({})
        mongo.MetricsCollection.delete_many({})
        #print self.SAMPLE_METADATA


    def test_saving_links_in_mongo(self):

        #if flush == True: mongo._db.links.delete_many({})
        # The function we are testing
        

        mongo.save_links(self.SAMPLE_LINKS)
        cursor = mongo.LinksCollection.find()
        self.fetched_links = [ line['url'] for line in cursor]

        for line in self.SAMPLE_LINKS:
            self.assertIn(line, self.fetched_links, msg='checking : '+line)
        

    def test_facebook_meta_data(self):
        
        #the function we are testing
        mongo.store_metrics_data(self.SAMPLE_METADATA)
        fetched_data = fetch(mongo.LinksCollection)
        #building the comparator to compare with our actual data
        comparator = dict()
        for m in fetched_data: 
            url = m['url']
            comparator[url] = clean(m,['url','stats.fb_stats.time_stamp'])
            m['url'] = url
        
        for line in fetched_data:
            self.assertEqual(line['stats']['fb_stats'], comparator[line['url']]['stats']['fb_stats'] )
            
    

if __name__ == '__main__':
    unittest.main()
    print self.SAMPLE_LINKS



