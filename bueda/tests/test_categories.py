import bueda

def test_categories():
    b = bueda.BuedaApi()
    cats = b.categories(['toyota','prius']).categories
    assert type(cats) is list
    assert cats
