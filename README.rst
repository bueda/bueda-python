Bueda API Wrapper
-----------------

Makes it easier to call the Bueda API from within Python.

Using it is a simple as::

    import bueda
    bueda.API_KEY = 'vImIEj5T0n7ldfjl8TO0ADTIRdRcvbRkvagiEw'
    enriched = bueda.enrich(['toyotaprius', 'hybrid']) 
    print enriched.canonical

To use it, get your API key at `http://www.bueda.com/ <http://www.bueda.com>`_

