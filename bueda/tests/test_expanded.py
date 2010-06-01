import bueda

def test_expanded():
    expanded = bueda.expanded(['toyota','prius'])
    assert expanded
    assert type(expanded) is list

