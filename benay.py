import fbworker as worker
import mongo as db
import util, sys

_VERBOSE_ =  False
if 'verbose' in sys.argv: _VERBOSE_ = True

if 'rss' in sys.argv :
	links = worker.rss_links()
	db.save_links(links)

if 'metrics' in sys.argv:
	links = db.get_links()
	for link in links:
		meta_data = worker.facebook_meta_data(link['url'])
		db.store_metrics_data([meta_data])