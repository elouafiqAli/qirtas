#!/usr/bin/python
# -*- coding: utf-8 -*-

import facebook
from urlparse import urlparse, parse_qs
from cache import CacheRequests


class GraphAPI(facebook.GraphAPI):
    def __init__(self, access_token):
        self.request = CacheRequests(self.request)
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

