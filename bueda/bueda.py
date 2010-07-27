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
    b = bueda.BuedaApi('2EvC9SVR0Y5vBt48dA1xMwkAxv8XP15OZ7ulsw')
    enriched = b.enriched(['toyotaprius', 'hybrid'])
    print enriched.canonical

By default, the API library uses a demo key that is very limited in terms of
how many queries you can use it for. We recommend that you use your own key (by
calling `BuedaApi(api_key=<your key>`). If you do not have one, get your
API key at http://www.bueda.com/
'''
import simplejson
import urllib2
from functools import partial

from bueda_version import __version__

DEMO_KEY = 'UlBuDaK5zeIAIRfBma2NtOSVSnHXplRIgMIPZQ'
API_URL = 'http://api.bueda.com/'

class BuedaApi(object):
    def __init__(self, api_key=None, api_url=None):
        self.api_key = api_key or DEMO_KEY
        self.api_url = api_url or API_URL
        if not api_key:
            import warnings
            warnings.warn('You are using the Bueda demo key! '
                'Everything will work, but this key has a low priority and is '
                'only valid for a limited number of queries. '
                'Get your own key at http://www.bueda.com.')

    def __getattr__(self, method, **kwargs):
        def call_method(self, *args, **kwargs):
            url = self.api_url + method + '?apikey=' + self.api_key
            for arg in args:
                # Assume any non-keyword arg is just tags
                if hasattr(arg, '__iter__'):
                    arg = u','.join(arg)
                url += '&tags=%s' % urllib2.quote(arg.encode('utf-8'))
            for key, value in kwargs.items():
                if hasattr(value, '__iter__'):
                    for item in value:
                        url += u'&%s=%s' % (key, item)
                else:
                    url += ('&%s=%s'
                            % (key, urllib2.quote(value.encode('utf-8'))))
            return BuedaApiResponse(urllib2.urlopen(url).read())
        return call_method.__get__(self)

class BuedaApiResponse(object):
    def __init__(self, data):
        response = simplejson.loads(unicode(data))
        self.query = response['query']
        for key, value in response['result'].iteritems():
            self.__setattr__(key, value)

    def __unicode__(self):
        return '<BuedaApiResponse %s>' % self.__dict__

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__unicode__()
