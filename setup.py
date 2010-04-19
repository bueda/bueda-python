from distutils.core import setup
execfile('bueda/bueda_version.py')

long_description = '''\
Bueda API Wrapper
-----------------

Makes it easier to call the Bueda API from within Python.

Using it is a simple as::

    import bueda
    enriched = bueda.enrich(['toyotaprius', 'hybrid']) 
    print enriched.canonical

To use it, get your API key at `http://www.bueda.com/ <http://www.bueda.com>`_
'''

classifiers = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development',
]

setup(name = 'bueda',
      version = __version__,
      description = 'Wrapper for Bueda API',
      long_description = long_description,
      author = 'Bueda',
      author_email = 'support@bueda.com',
      license = 'MIT',
      platforms = ['Any'],
      classifiers = classifiers,
      url = 'http://www.bueda.com',
      packages = ['bueda'],
      )


