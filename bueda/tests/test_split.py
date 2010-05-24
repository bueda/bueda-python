import bueda

def test_split():
    assert bueda.split(['newyorkcity']) == ['new york city']
    assert bueda.split(['newyorkcity']) != ['newyorkcity']
    assert bueda.split(['new york city']) == ['new york city']
    assert bueda.split(['city']) == ['city']

