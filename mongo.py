from pymongo import MongoClient
from prawn	import *
from datetime import datetime

client = MongoClient()
_db = client.zelda
_links = _db.links

def show_links():
	curs = _db.links.find()
	for line in curs: print(line)
def save_links(links):
	for link in links:
		result = _links.update_one(
			{
				"link": link
				
			},{
				'$setOnInsert': {
					"date": datetime.strptime("2014-10-01", "%Y-%m-%d")
				}
			},
			True #upsert
		)

if __name__ == "__main__":
	fetched_links = rss_links()
	save_links(fetched_links)
	show_links()

