from nose.tools import eq_
import bueda

def test_canonical():
    b = bueda.BuedaApi()
    eq_(b.canonical(['new york city']).canonical, ['New York City'])
    eq_(b.canonical(['newyorkcity']).canonical, ['New York City'])
    eq_(b.canonical(['nyc']).canonical, ['New York City'])

