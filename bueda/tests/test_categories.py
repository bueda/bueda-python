import bueda

def test_categories():
    cats = bueda.categories(['toyota','prius'])
    assert type(cats) is list
    assert cats
