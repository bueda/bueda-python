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
    enriched = bueda.enrich(['toyotaprius', 'hybrid'])
    print enriched.canonical
'''
import simplejson
import urllib
import urllib2

API_KEY = 'vImIEj5T0n7ldfjl8TO0ADTIRdRcvbRkvagiEw'
API_URL = 'http://api.bueda.com/'

class Semantic(object):
    '''
    Semantic(types, concept_id, original)

    '''
    def __init__(self, types, concept_id, original):
        self.types = types
        self.concept_id = concept_id
        self.original = original
    def __str__(self):
        return '<Semantic %s>' % self.concept_id

    def __repr__(self):
        return 'Semantic(%s, %s, %s)' % (
                self.types,
                self.concept_id,
                self.original)

class Category(object):
    '''
    Represents a category result.

    Fields
    ------
      name : Name (as a string)
      confidence : confidence value (floating point number between 0 and 1)
    '''
    def __init__(self, name, confidence):
        self.name = name
        self.confidence = float(confidence)

    def __str__(self):
        return '<Category %s (conf: %s)>' % (self.name, self.confidence)
    def __repr__(self):
        return 'Category(%s, %s)' % (self.name, self.confidence)

class Enriched(object):
    '''
    Represents the results of a Bueda API call.

    Fields
    ------
      split_tags : split tags as list of strings
      canonical : canonical string representations (list of string)
      categories : list of Category objects
      semantic : list of Semantic objects
    '''
    def __init__(self, split_tags, canonical, categories, semantic):
        self.split_tags = split_tags
        self.canonical = canonical
        self.categories = categories
        self.semantic = semantic
    def __str__(self):
        return '<Enriched %s>' % self.canonical

    def __repr__(self):
        return 'Enriched(%s, %s, %s, %s)' % (
                        self.split_tags,
                        self.canonical,
                        self.categories,
                        self.semantic)


def init(api_key):
    '''
    init(api_key)

    Set the API key to be `api_key`.

    If you do not have one, get your API key at http://www.bueda.com/

    By default, the API library uses a demo key that is limited.
    '''
    global API_KEY
    API_KEY = api_key

def enrich(tags, api_key=None):
    '''
    enriched = enrich([tag0, tag1, tag2, ...], api_key={bueda.API_KEY})

    Parameters
    ----------
      tags :    List of tags as strings
      api_key : API key to use. If None, it uses bueda.API_KEY
    Returns
    -------
      enriched : Enriched
    '''
    tags = map(urllib2.quote, tags)
    url = API_URL + ('enriched?callback=&tags=%s&apikey=%s' % (','.join(tags), API_KEY))
    data = simplejson.load( urllib2.urlopen(url))
    result = data['result']
    return Enriched(
            split_tags=result['split_tags'],
            canonical=result['canonical'],
            categories=[Category(c['name'], c['confidence']) for c in result['categories']],
            semantic=[Semantic(s['types'], s['concept_id'], s['original']) for s in result['semantic']],
            )

