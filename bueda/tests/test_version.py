import bueda

def test_version():
    b = bueda.BuedaApi()
    assert type(b.version().version) is unicode

