from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
database = client.cacheDB


def find_cache(path, request, collection='graph_api'):
    if 'access_token' in request:
        del request['access_token']
    graph_api_cache = getattr(database, collection)
    response = graph_api_cache.find({'path': path, 'request': request})
    if response.count() > 0:
        return response.__iter__().next()['response']
    else:
        raise Exception({'path': path, 'request': request}, 'not found')


def save_cache(path, request, response, collection='graph_api'):
    if 'access_token' in request:
        del request['access_token']
    graph_api_cache = getattr(database, collection)

    saved = graph_api_cache.insert({
        'path': path,
        'request': request,
        'timestamp': datetime.strptime("2014-10-01", "%Y-%m-%d"),
        'response': response
    })

    return saved


def CacheRequests(request_function):
    def cachier(*args, **kargs):

        # because the first element is 'self' thus the second is the actual path
        # request(self,path, arguments_dictionary)
        path = args[0]
        try:
            cache_data = find_cache(path, kargs)
            return cache_data
        except Exception as e:

            result = request_function(path, kargs)
            save_cache(path, kargs, result)
            return result

    return cachier

