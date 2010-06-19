# -*- coding: utf-8 -*-
import bueda

def test_unicode():
    b = bueda.BuedaApi()
    assert b.enriched([u'Luís Pedro Coelho'])
