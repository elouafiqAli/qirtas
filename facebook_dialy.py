#!/usr/bin/python
# -*- coding: utf-8 -*-

import facebook
from util import objectify
from urlparse import urlparse, parse_qs


class GraphAPI(facebook.GraphAPI):

    def __init__(self, access_token):
        self.request = objectify(self.request)
        super(GraphAPI, self).__init__(access_token, version='2.5')

    def get_pages(self, id, connection_name, **args):
        """
            Gets paging of a connections

        """

        response = self.request(
            "%s/%s/%s" % (self.version, id, connection_name), args)

        yield response
        print '🚀'
        while 'paging' in response.__dict__:
        	
        	print '🚀'
        	next = response.paging.next
        	request = urlparse(next)
        	response = self.request(request.path, parse_qs(request.query))
        	yield response
