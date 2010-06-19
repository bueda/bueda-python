# Copyright (c) 2010 Bueda Inc
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
'''
Bueda Python Library

Example Usage
-------------

::

    import bueda
    bueda.init('2EvC9SVR0Y5vBt48dA1xMwkAxv8XP15OZ7ulsw')
    enriched = bueda.enrich(['toyotaprius', 'hybrid'])
    print enriched.canonical

By default, the API library uses a demo key that is very limited in terms of
how many queries you can use it for. We recommend that you use your own key (by
calling `init()`). If you do not have one, get your
API key at http://www.bueda.com/
'''
import simplejson
import urllib2
from functools import partial

from bueda_version import __version__

DEMO_KEY = 'UlBuDaK5zeIAIRfBma2NtOSVSnHXplRIgMIPZQ'
API_URL = 'http://api.bueda.com/'

class BuedaApi(object):
    def __init__(self, api_key=None):
        self.api_key = api_key or DEMO_KEY
        if not api_key:
            demo_key_message = '''\
    You are using the Bueda demo key! Everything will work, but this key has a low
    priority and is only valid for a limited number of queries.

    Get your own key at http://www.bueda.com.

    '''
            import warnings
            warnings.warn(demo_key_message)

    def __getattr__(self, method, **kwargs):
        def call_method(self, *args, **kwargs):
            url = API_URL + method + '?apikey=' + self.api_key
            for arg in args:
                # Assume any non-keyword arg is just tags
                if hasattr(arg, '__iter__'):
                    arg = u','.join(arg)
                url += '&tags=%s' % urllib2.quote(arg.encode('utf-8'))
            for key_value in kwargs.iteritems():
                if hasattr(key_value, '__iter__'):
                    key_value = u','.join(key_value)
                url += '&%s=%s' % urllib2.quote(key_value.encode('utf-8'))
            return BuedaApiResponse(urllib2.urlopen(url))
        return call_method.__get__(self)

    def _prepare_tags(tags):
        def _to_utf8(s):
            if type(s) is unicode:
                return s.encode('utf8')
            return s
        tags = map(_to_utf8, tags)
        tags = map(urllib2.quote, tags)
        return ','.join(tags)

class BuedaApiResponse(object):
    def __init__(self, data):
        response = simplejson.load(data)
        self.query = response['query']
        result = response['result']
        self.success = result['success']
        result.pop('success')
        for key, value in result.iteritems():
            self.__setattr__(key, value)

    def __unicode__(self):
        return '<BuedaApiResponse %s>' % self.__dict__

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__unicode__()
