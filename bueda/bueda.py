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
import urllib
import urllib2

from bueda_version import __version__

DEMO_KEY = 'UlBuDaK5zeIAIRfBma2NtOSVSnHXplRIgMIPZQ'
API_KEY = DEMO_KEY
API_URL = 'http://api.bueda.com/'

class Semantic(object):
    '''
    Semantic(name, types, concept_id, original)

    Represents the returned semantic concepts from Bueda API.

    Fields
    ------
      types : A list of types (as strings)
      concept_id : A unique id for this concept
      original : The list of inputs that led to this result
    '''
    def __init__(self, name, types, concept_id, original):
        self.name = name
        self.types = [typ['name'] for typ in types]
        self.concept_id = concept_id
        self.original = original
    def __str__(self):
        return '<Semantic %s>' % self.concept_id

    def __repr__(self):
        return 'Semantic(%s, %s, %s, %s)' % (
                self.name,
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
      split : split tags as list of strings
      canonical : canonical string representations (list of string)
      categories : list of Category objects
      semantic : list of Semantic objects
    '''
    def __init__(self, split, canonical, categories, semantic):
        self.split = split
        self.canonical = canonical
        self.categories = categories
        self.semantic = semantic
    def __str__(self):
        return '<Enriched %s>' % self.canonical

    def __repr__(self):
        return 'Enriched(%s, %s, %s, %s)' % (
                        self.split,
                        self.canonical,
                        self.categories,
                        self.semantic)


def init(api_key):
    '''
    init(api_key)

    Set the API key to be `api_key`.

    By default, the API library uses a demo key that is very limited in terms
    of how many queries you can use it for. We recommend that you use your own
    key (by calling `init()`). If you do not have one,
    get your API key at http://www.bueda.com/

    Parameters
    ----------
      api_key : API KEY as a string
    '''
    global API_KEY
    API_KEY = api_key


def _get_api_key(api_key):
    if api_key is not None:
        return api_key
    if API_KEY == DEMO_KEY:
        demo_key_message = '''\
You are using the Bueda demo key! Everything will work, but this key has a low
priority and is only valid for a limited number of queries.

Get your own key at http://www.bueda.com.

'''
        import warnings
        warnings.warn(demo_key_message)
    return API_KEY


def _call_method(method, api_key, **kwargs):
    url = API_URL + method + '?apikey=' + _get_api_key(api_key)
    for key_value in kwargs.iteritems():
        url += ('&%s=%s' % key_value)
    return simplejson.load( urllib2.urlopen(url))

def _prepare_tags(tags):
    def _to_utf8(s):
        if type(s) is unicode:
            return s.encode('utf8')
        return s
    tags = map(_to_utf8, tags)
    tags = map(urllib2.quote, tags)
    return ','.join(tags)

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
    data = _call_method('enriched', api_key, tags=_prepare_tags(tags))
    result = data['result']
    return Enriched(
            split=result['split'],
            canonical=result['canonical'],
            categories=[Category(c['name'], c['confidence']) for c in result['categories']],
            semantic=[Semantic(s['name'], s['types'], s['uri'], s['original']) for s in result['semantic']],
            )


def version(api_key=None):
    '''
    version = bueda.version(api_key={bueda.API_KEY})

    Returns the bueda API version

    Note that this is the API version, *not* the library version. Check
    `__version__` for that.
    Parameters
    ----------
      api_key : API key (default: bueda.API_KEY)
    Returns
    -------
      version : API version (as a string)
    '''
    api_key = _get_api_key(api_key)
    data = _call_method('version', api_key)
    return data['result']['version']


def split(tags, api_key=None):
    '''
    split_tags = split([tag0, tag1, tag2, ...], api_key={bueda.API_KEY})

    Splits multi-word tags into words.

    The the tag already contains spaces or if it is composed of a single word,
    the original tag is returned.

    Parameters
    ----------
      tags :    List of tags as strings
      api_key : API key to use. If None, it uses bueda.API_KEY
    Returns
    -------
      split_tags : A list of split tags
    '''
    data = _call_method('split', api_key, tags=_prepare_tags(tags))
    result = data['result']
    return result['split']


def expanded(tags, api_key=None):
    '''
    expanded_tags = expanded([tag0, tag1, tag2, ...], api_key={bueda.API_KEY})

    Expands the submitted tags to aliases, categories and terms. This is
    especially useful for expanding coverage when searching.

    Parameters
    ----------
      tags :    List of tags as strings
      api_key : API key to use. If None, it uses bueda.API_KEY
    Returns
    -------
      expanded_tags : A list of split tags
    '''
    data = _call_method('expanded', api_key, tags=_prepare_tags(tags))
    result = data['result']
    return result['expanded']


def categories(tags, api_key=None):
    '''
    tag_categories = categories([tag0, tag1, tag2, ...], api_key={bueda.API_KEY})

    Returns the categories associated with a tag as a list of `Category`
    objects.

    Parameters
    ----------
      tags :    List of tags as strings
      api_key : API key to use. If None, it uses bueda.API_KEY
    Returns
    -------
      tag_categories : A list of `Category` objects
    '''
    data = _call_method('categories', api_key, tags=_prepare_tags(tags))
    result = data['result']
    return [Category(c['name'], c['confidence']) for c in result['categories']]


def semantics(tags, api_key=None):
    '''
    tag_semantics = semantics([tag0, tag1, tag2, ...], api_key={bueda.API_KEY})

    Returns the semantic meaning of each tag as a list of `semantic` objects.

    Parameters
    ----------
      tags :    List of tags as strings
      api_key : API key to use. If None, it uses bueda.API_KEY
    Returns
    -------
      tag_semantics : A list of `Semantic` objects
    '''
    data = _call_method('categories', api_key, tags=_prepare_tags(tags))
    result = data['result']
    return [Semantic(s['name'], s['types'], s['uri'], s['original']) for s in result['semantic']]


def canonical(tags, api_key=None):
    '''
    canonical_tags = canonical([tag0, tag1, tag2, ...], api_key={bueda.API_KEY})

    Returns a canonical human-readible tag for each input tag.

    Parameters
    ----------
      tags :    List of tags as strings
      api_key : API key to use. If None, it uses bueda.API_KEY
    Returns
    -------
      canonical_tags : List of canonical tags as strings
    '''
    data = _call_method('canonical', api_key, tags=_prepare_tags(tags))
    result = data['result']
    return result['canonical']


