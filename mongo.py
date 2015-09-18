from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
_db = client.zelda
LinksCollection = _db.links
MetricsCollection = _db.metrics

def show_links():
	curs = _db.links.find()
	for line in curs: print(line)

def save_links(links):
	for link in links:
		result = LinksCollection.update_one(
			{
				"url": link
				
			},{
				'$setOnInsert': {
					"date": datetime.strptime("2014-10-01", "%Y-%m-%d")
				}
			},
			True #upsert
		)

def meta_data_changes():
	all_links = _db.links.find()
	all_meta_data = []
	for link in all_links:
		meta_data = facebook_meta_data(link['url'])
		meta_data['url']=link['url']
		all_meta_data.append(meta_data)

def store_metrics_data(all_metrics_data):

	for metrics in all_metrics_data:
		measured_url = metrics['url']
		del metrics['url']

		result = MetricsCollection.update_one(
			{
				"url" : measured_url
			},{
				'$push' :
				{
					'stats.fb_stats': metrics
					
				}
			}, True)

		result = LinksCollection.update_one(
			{
				"url" : measured_url
			},{
				'$set' :
				{
					'stats.fb_stats': metrics
					
				}
			}, True)
	"""
	for meta_data in all_meta_data:
		result = _links.update_one(
			{
				"url" : meta_data['url']
			},{
				'$push' :
				{
					'metrics.fb_metrics': {
						
							"time_stamp": meta_data['time_stamp'],
							'comment_count'	: meta_data['comment_count'],
							'share_count'	: meta_data['share_count'] ,
							'like_count'	: meta_data['like_count']
						
					}
					
				}
			})
	"""
