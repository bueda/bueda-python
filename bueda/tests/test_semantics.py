import bueda

def test_semantics():
    sems = bueda.categories(['toyota','prius'])
    assert type(sems) is list
    assert sems
