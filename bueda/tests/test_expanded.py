import bueda

def test_expanded():
    b = bueda.BuedaApi()
    expanded = b.expanded(['toyota','prius']).expanded
    assert expanded
    assert type(expanded) is list

