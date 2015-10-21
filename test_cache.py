import cache
from util import trace
from test_facebook import test_data, test_token
import facebook_dialy as facebook

def test_save():
    collection='graph_api'
    cache.save_cache(test_data['path'],test_data['request'],test_data['response'],collection)
    answer = cache.find_cache(test_data['path'],test_data['request'],collection)
    assert answer == test_data['response']
    print '-- request saved properly'

def test_find():
    collection='graph_api'
    answer = cache.find_cache(test_data['path'],test_data['request'],collection)
    assert answer == test_data['response']
    print '-- request found propertly'

def test_cache_requests():
    graph = facebook.GraphAPI(test_token)
    graph.request =  cache.CacheRequests(graph.request)
    graph.get_object('me')
    ares = graph.get_object('me')
    assert ares == cache.find_cache('v2.5/me',{})
    print 'read ',ares['id'],' successfully'

