from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
database = client.cacheDB


def _key(path,request):
        return '?'.join([path, '&'.join( [ '='.join([key, str(','.join(request[key])) if type(request[key]) is list else request[key]]) for key in request] ) ])


def find_cache(path, request, collection='graph_api'):
    if 'access_token' in request:
        del request['access_token']
    graph_api_cache = getattr(database, collection)

    response = graph_api_cache.find({'_id': _key(path,request)})

    if response.count() > 0:
        return response.__iter__().next()['response']
    else:
        raise Exception({'_id': _key(path,request)}, 'not found')


def save_cache(path, request, response, collection='graph_api'):
    if 'access_token' in request:
        del request['access_token']
    graph_api_cache = getattr(database, collection)

    saved = graph_api_cache.insert({
        '_id': _key(path,request),
        'path': path,
        'request': request,
        'timestamp': datetime.strptime("2014-10-01", "%Y-%m-%d"),
        'response': response
    })

    return saved


def cache_request(request_function, database_name = 'cacheDB'):
    global database
    database = getattr(client,database_name)

    def cachier(*args):

        # because the first element is 'self' thus the second is the actual path
        # request(self,path, arguments_dictionary)
        path = args[0]
        request = args[1]
        try:

            cache_data = find_cache(path, request)
            return cache_data
        except Exception as e:
            result = request_function(path, request)
            save_cache(path, request, result)
            return result

    return cachier

