from nose.tools import eq_
import bueda

def test_split():
    b = bueda.BuedaApi()
    eq_(b.split(['newyorkcity']).split, ['new york city'])
    eq_(b.split(['new york city']).split, ['new york city'])
    eq_(b.split(['city']).split, ['city'])

