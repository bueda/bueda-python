import bueda

def test_canonical():
    assert bueda.canonical(['new york city']) == ['New York City']
    assert bueda.canonical(['newyorkcity']) == ['New York City']
    assert bueda.canonical(['nyc']) == ['New York City']

