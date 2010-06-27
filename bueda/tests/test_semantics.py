import bueda

def test_semantics():
    b = bueda.BuedaApi()
    sems = b.semantics(['toyota','prius']).semantic
    assert type(sems) is list
    assert sems
