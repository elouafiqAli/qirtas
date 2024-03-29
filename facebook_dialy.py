#!/usr/bin/python
# -*- coding: utf-8 -*-

import facebook_edge
from urlparse import urlparse, parse_qs
from cache import cache_request

__default_cache__ = 'cacheDB'

class GraphAPI(facebook_edge.GraphAPI):
    def __init__(self, access_token, caching = True, cache_database = __default_cache__):
        if caching == True:
            self.request = cache_request(self.request,cache_database)
        super(GraphAPI, self).__init__(access_token, version='2.5')

    def get_pages(self, id, connection_name, **args):

        response = self.request(
            "%s/%s/%s" % (self.version, id, connection_name), args)

        yield response
        while 'paging' in response:
            if 'next' in response['paging']:
                next = response['paging']['next']
                request = urlparse(next)
                response = self.request(request.path, parse_qs(request.query))
                yield response
            else:
                break


def CachedGraphAPI(token):

    cached_graph_api  = GraphAPI(token)
    cached_graph_api.request = cache_request(cached_graph_api.request)
    return cached_graph_api