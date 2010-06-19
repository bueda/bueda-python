import bueda

def test_semantics():
    b = bueda.BuedaApi()
    sems = b.categories(['toyota','prius']).categories
    assert type(sems) is list
    assert sems
