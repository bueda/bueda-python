Bueda API Wrapper
-----------------

Makes it easier to call the Bueda API from within Python.

Using it is a simple as::

    import bueda
    b = bueda.BuedaApi('2EvC9SVR0Y5vBt48dA1xMwkAxv8XP15OZ7ulsw')
    enriched = b.enriched(['toyotaprius', 'hybrid'])
    print enriched.canonical

To use it, get your API key at `http://www.bueda.com/ <http://www.bueda.com>`_

