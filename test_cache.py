import cache
from util import trace
from test_facebook import test_data, test_token
import facebook_dialy as facebook
from urlparse import urlparse, parse_qs
import users

_collection='graph_api'


def test_set_up(database_name =  'testing'):
    cache.database = getattr(cache.client,database_name)
    getattr(cache.database,_collection).drop()
    getattr(cache.database,_collection)


def test_save_find():

    cache.save_cache(test_data['path'],test_data['request'],test_data['response'],_collection)
    answer = cache.find_cache(test_data['path'],test_data['request'],_collection)
    assert answer == test_data['response']
    print '-- request saved properly'


def test_key():

    test_cases = [
            '/me/doing?name=ALLAH,AKBAR&prophet=Muhammad&attribute=SalaALLAHAleiyhiwaSalam',
            '/69/book?name=Quran&master=RassulALLAH&teacher=Jybryl',
            '/quran?book=77'
        ]

    for case in test_cases:
        parsed = urlparse(case)
        parsed2 =  urlparse(cache._key(parsed.path,parse_qs(parsed.query)))
        assert [parsed.path, parse_qs(parsed.query)] == [parsed2.path, parse_qs(parsed2.query)]
        print 'passing : ',test_cases.index(case)


def test_cache_requests():
    import time
    graph = facebook.GraphAPI(test_token)
    graph.request =  cache.cache_request(graph.request)

    graph.get_object('me')
    ares = graph.get_object('me')
    assert ares == cache.find_cache('v2.5/me',{})
    print 'read ',ares['id'],' successfully'

#behavior
def test_user_scenario():

    users.__caching__ = True
    users.__cache_database__ = 'testing_users'
    test_database = getattr(cache.client,users.__cache_database__)
    getattr(test_database,_collection).drop()
    test_user = users.User(test_token)
    print test_user.reach


if __name__ == '__main__':

    test_user_scenario()